void minmax(float4* const xi);
void sort(float4* const tau);
float gammaCT_f(const float p, const float4 coords);
float gamma2(const float2 b);
float gamma13(const float4 b);
float4 projCorner4F1(float4 rCenter, float tRef, const float16* const P, constant float3* voxelSize_mm);
float4 projCorner4F2(float4 rCenter, const float16* const P_loc, constant float3* voxelSize_mm);
float slopeOfEdge(float4 rworld, const float16* const P, constant float3* voxelSize_mm);
float zForEqualT(float t, float4 edge, const float16* const P);

#define F1_SIZE 128

// the backsmear kernel - with TR footprint
kernel void backprojector_sfp( uint z,
                               uint viewNb,
                               uint nbModules,
                               constant float3* restrict volCorner_mm,
                               constant float3* restrict voxelSize_mm,
                               global const float4* restrict pMatsGlobal,
                               local float4* restrict pMatsLoc,
                               global float* restrict sliceBuf,
                               read_only image3d_t proj,
                               global const float* restrict angleCorrAzi,
                               global const float* restrict angleCorrPol)
{
    // copy required projection matrices from global to local memory
    event_t cpyToLocalEvent = async_work_group_copy(pMatsLoc,
                                                    pMatsGlobal + 3 * nbModules * viewNb,
                                                    3 * nbModules, 0);
    // get IDs
    const int x = get_global_id(0);
    const int y = get_global_id(1);
    // get dimensions
    const int X = get_global_size(0);
    const int Y = get_global_size(1);   
    const float4 projDim = convert_float4(get_image_dim(proj));

    // world coordinate vector of voxel (center) position
    const float4 rCenter = (float4)( x * (*voxelSize_mm).x + (*volCorner_mm).x,
                                     y * (*voxelSize_mm).y + (*volCorner_mm).y,
                                     z * (*voxelSize_mm).z + (*volCorner_mm).z,
                                     1.0f);

    float totalCorr = 0.0f;
    float sShiftPerT, sPos, sShift, floorOfShift, fractOfShift, tRef;
    float4 pMatRow0, pMatRow1, pMatRow2, rEdge, tau;
    float2 t_plusMinus;
    int2 sRange, tRange;
    int s, t;

    // wait for copy process of projection matrices to local memory
    wait_group_events(1, &cpyToLocalEvent);

    // loop over all detector sub-modules
    for(uint module = 0; module < nbModules; ++module)
    {
        const uint angleAziCorrOffSet = (viewNb * nbModules + module) * (uint)(projDim.x);
        const uint anglePolCorrOffSet = (viewNb * nbModules + module) * (uint)(projDim.y);

        pMatRow0 = pMatsLoc[module * 3 + 0];
        pMatRow1 = pMatsLoc[module * 3 + 1];
        pMatRow2 = pMatsLoc[module * 3 + 2];

        float16 P_loc = (float16)(pMatRow0,
                                  pMatRow1,
                                  pMatRow2,
                                  (float4)0.0f);

        // +++ calculate footprint function F1 +++
        // compute reference t value
        tRef = dot(pMatRow1, rCenter) / dot(pMatRow2, rCenter);
        sShiftPerT = slopeOfEdge(rCenter, &P_loc, voxelSize_mm);

        // calculate intersections for footprint function F1 (s direction)
        tau = projCorner4F1(rCenter, tRef, &P_loc, voxelSize_mm);
        // check if voxel is projected outside detector
        if(tau.s0 + 0.5f >= projDim.x || tau.s3 + 0.5f < 0.0f)
            continue;

        // determine ranges for s
        sRange.s0 = max((int)(tau.s0 + 0.5f - 1.0f), 0);
        sRange.s1 = min((int)(tau.s3 + 0.5f + 1.0f), (int)(projDim.x));
        const int sLength = sRange.s1 - sRange.s0;

        // +++ calculate footprint function F2 +++
        // determine supporting points of footprint (t direction) - trapezoidal shape
        float4 xi = projCorner4F2(rCenter, &P_loc, voxelSize_mm);
        xi = projCorner4F2(rCenter, &P_loc, voxelSize_mm);
         // check if voxel is projected outside detector
        if(xi.s0 + 0.5f >= projDim.y || xi.s3 + 0.5f < 0.0f)
            continue;

        // clamp range to detector size [0, projDim.y-1]
        tRange.s0 = max((int)(xi.s0 + 0.5f), 0);
        tRange.s1 = min((int)(xi.s3 + 0.5f), (int)(projDim.y) - 1);
        const int tLength = tRange.s1 - tRange.s0;

        // accumulate backprojected values
        for (t = 0; t <= tLength; t++)
        {
            // shift of s footprint (F1)
            sShift = ((float)(tRange.s0 + t) - tRef) * sShiftPerT;
            fractOfShift = fract(sShift, &floorOfShift);

            const float F2 = gammaCT_f((float)(tRange.s0 + t), xi)
                    * angleCorrPol[anglePolCorrOffSet + tRange.s0 + t];

            for (s = 0; s <= sLength; s++)
            {
                if(s + sRange.s0 + (int)floorOfShift < 0 ||
                   s + sRange.s0 + (int)floorOfShift >= (int)(projDim.x))
                    continue;

                const int4 pixelIndex = (int4)(sRange.s0 + s + (int)floorOfShift,
                                               tRange.s0 + t,
                                               module + viewNb*nbModules, 0);

                const float F1 = gammaCT_f((float)(sRange.s0 + s) - fractOfShift, tau)
                        * angleCorrAzi[angleAziCorrOffSet + pixelIndex.x];
                totalCorr += F1 * F2 * read_imagef(proj, pixelIndex).x;
            }
        }
    }

    // write accumulated value to z-slice buffer (result)
    const size_t bufIdx = x + y*X; // 1D lookup index
    sliceBuf[bufIdx] += totalCorr * (*voxelSize_mm).x;
}

inline void minmax(float4* const xi)
{
    float temp = min(xi[0].s0,xi[0].s1);
    temp = min(temp,xi[0].s2);
    temp = min(temp,xi[0].s3);
    xi[0].s3 = max(xi[0].s3,xi[0].s0);
    xi[0].s3 = max(xi[0].s3,xi[0].s1);
    xi[0].s3 = max(xi[0].s3,xi[0].s2);
    xi[0].s0 = temp;
}

inline void sort(float4* const xi)
{
    float temp;
    temp = xi[0].s0 < xi[0].s1;
    xi[0].s01 = mad(temp,xi[0].s01,mad(-temp,xi[0].s10,xi[0].s10));
    temp = xi[0].s1 < xi[0].s2;
    xi[0].s12 = mad(temp,xi[0].s12,mad(-temp,xi[0].s21,xi[0].s21));
    temp = xi[0].s2 < xi[0].s3;
    xi[0].s23 = mad(temp,xi[0].s23,mad(-temp,xi[0].s32,xi[0].s32));
    temp = xi[0].s0 < xi[0].s1;
    xi[0].s01 = mad(temp,xi[0].s01,mad(-temp,xi[0].s10,xi[0].s10));
    temp = xi[0].s1 < xi[0].s2;
    xi[0].s12 = mad(temp,xi[0].s12,mad(-temp,xi[0].s21,xi[0].s21));
    temp = xi[0].s0 < xi[0].s1;
    xi[0].s01 = mad(temp,xi[0].s01,mad(-temp,xi[0].s10,xi[0].s10));
}

inline float gammaCT_f(const float p, const float4 coords)
{
    float2 s = p + (float2)(-0.5f,0.5f);

    return gamma13((float4)(max(s.x, coords.s0), min(s.y, coords.s1), coords.s01)) +
           gamma2( (float2)(max(s.x, coords.s1), min(s.y, coords.s2))) +
           gamma13((float4)(max(s.x, coords.s2), min(s.y, coords.s3), coords.s32));
}

inline float gamma13(const float4 b)
{
    if(b.s1 > b.s0)
    {
        float2 temp = (b.s01 - b.s22);
        temp = temp * temp;
        return (temp.s1 - temp.s0) / (2.0f * (b.s3 - b.s2));
    }
    else
        return 0.0f;
}

inline float gamma2(const float2 b)
{
    if(b.s1 > b.s0)
        return b.s1 - b.s0;
    else
        return 0.0f;
}

inline float4 projCorner4F1(float4 rCenter, float tRef, const float16* const P, constant float3* voxSize)
{
    float4 tau,rEdge;

    // first edge
    rEdge 	  = rCenter + (float4)(+0.5f * (*voxSize).x, +0.5f * (*voxSize).y, 0.0f, 0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s0 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // second edge
    rEdge 	  = rCenter + (float4)(+0.5f * (*voxSize).x, -0.5f * (*voxSize).y, 0.0f, 0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s1 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // third edge
    rEdge 	  = rCenter + (float4)(-0.5f * (*voxSize).x, +0.5f * (*voxSize).y, 0.0f, 0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s2 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // fourth edge
    rEdge 	  = rCenter + (float4)(-0.5f * (*voxSize).x, -0.5f * (*voxSize).y, 0.0f, 0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s3 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);
    sort(&tau);

    return tau;
}

inline float4 projCorner4F2(float4 rCenter, const float16* const P_loc, constant float3* voxSize)
{
    float4 xi, xiTemp, rEdge;

    // lower corner
    rEdge	  = rCenter + (float4)(+0.5f * (*voxSize).x, +0.5f * (*voxSize).y, 0.5f * (*voxSize).z, 0.0f);
    xiTemp.s0 = dot(P_loc[0].s4567, rEdge) / dot(P_loc[0].s89ab,rEdge);
    rEdge	  = rCenter + (float4)(-0.5f * (*voxSize).x, +0.5f * (*voxSize).y, 0.5f * (*voxSize).z, 0.0f);
    xiTemp.s1 = dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab,rEdge);
    rEdge	  = rCenter + (float4)(+0.5f * (*voxSize).x, -0.5f * (*voxSize).y, 0.5f * (*voxSize).z, 0.0f);
    xiTemp.s2 = dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab,rEdge);
    rEdge	  = rCenter + (float4)(-0.5f * (*voxSize).x, -0.5f * (*voxSize).y, 0.5f * (*voxSize).z, 0.0f);
    xiTemp.s3 = dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
    minmax(&xiTemp);
    xi.s01 		= xiTemp.s03;

    // upper corner
    rEdge 	  	= rCenter + (float4)(+0.5f * (*voxSize).x, +0.5f * (*voxSize).y, -0.5f * (*voxSize).z, 0.0f);
    xiTemp.s0	= dot(P_loc[0].s4567, rEdge) / dot(P_loc[0].s89ab, rEdge);
    rEdge 	  	= rCenter + (float4)(-0.5f * (*voxSize).x, +0.5f * (*voxSize).y, -0.5f * (*voxSize).z, 0.0f);
    xiTemp.s1	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
    rEdge		= rCenter + (float4)(+0.5f * (*voxSize).x, -0.5f * (*voxSize).y, -0.5f * (*voxSize).z, 0.0f);
    xiTemp.s2	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
    rEdge		= rCenter + (float4)(-0.5f * (*voxSize).x, -0.5f * (*voxSize).y, -0.5f * (*voxSize).z, 0.0f);
    xiTemp.s3	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
    minmax(&xiTemp);
    xi.s23  = xiTemp.s03;

    return xi;
}

inline float slopeOfEdge(float4 rworld, const float16* const P, constant float3* voxSize)
{
    rworld.s2 -= 0.5f * (*voxSize).z;
    float lowerS = dot(P[0].s0123, rworld) / dot(P[0].s89ab,rworld);
    float lowerT = dot(P[0].s4567, rworld) / dot(P[0].s89ab,rworld);
    rworld.s2 += 0.5f * (*voxSize).z;
    float upperS = dot(P[0].s0123, rworld) / dot(P[0].s89ab,rworld);
    float upperT = dot(P[0].s4567, rworld) / dot(P[0].s89ab,rworld);

    return (upperS - lowerS) / (upperT - lowerT);
}

inline float zForEqualT(float t, float4 edge, const float16* const P)
{
    // very small t values
    if(fabs(t) < 1.0e-6f)
    {
        // singular case (return arbitrary z)
        if(fabs(P[0].s6) < 1.0e-6f)
            return 0.0f;
        return -1.0f * (P[0].s4 * edge.x + P[0].s5 * edge.y + P[0].s7) / P[0].s6;
    }

    // singular case (return arbitrary z)
    if(fabs((P[0].sa - P[0].s6 / t)) < 1.0e-6f)
        return 0.0f;

    // regular cases
    return (1.0f / t * (P[0].s4 * edge.x + P[0].s5 * edge.y + P[0].s7)
            - (P[0].s8 * edge.x + P[0].s9 * edge.y + P[0].sb) ) / (P[0].sa - P[0].s6 / t);
}

