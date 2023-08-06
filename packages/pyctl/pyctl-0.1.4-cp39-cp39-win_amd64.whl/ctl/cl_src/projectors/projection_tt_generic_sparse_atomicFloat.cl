void 	sort(float4* const tau);
void 	minmax(float4* const xi);
float   gammaCT_f(const float p, const float4 coords);
float 	gamma2(const float2 b);
float 	gamma13(const float4 b);
float4 	projCorner4F2(float4 rworld, const float16* const P, const float16* const par);
float4  projCorner4F1_corr(float4 rworld, float tRef, const float16* const P, const float16* const par);
float   slopeOfEdge(float4 rworld, const float16* const P, const float16* const par);
float   zForEqualT(float t, float4 edge, const float16* const P);

kernel void proj( global float* restrict projData,
                  global float* restrict angleCorrAzi,
                  global float* restrict angleCorrPol,
                  global float16* restrict P,
                  global float16* restrict par,
                  read_only image1d_buffer_t voxelList,
                  int localBufferSize,
                  local float* restrict localMemArray )
{
    const int localID = get_local_id(0);
    const int projID  = get_group_id(1);
    const int areaID  = get_group_id(2);
    const float16 P_loc    = P[projID];
    const float16 par_loc  = par[0];
    const int8    par_locI = convert_int8(par[0].s0129abcd);

    // precompute some constants
    const int aziCorrOffset = projID * par_locI.s3;
    const int polCorrOffset = projID * par_locI.s4;
    const int tRowsInLocMem = localBufferSize / par_locI.s3;
    const int detectOffset  = localBufferSize * areaID;
    const int nbPixels      = par_locI.s3 * par_locI.s4;
    const int projOffset    = detectOffset + projID * nbPixels;
    const int boundary 	    = min(localBufferSize, nbPixels - detectOffset);

    // variable declarations
    float4 rworld = (float4)(0.0f, 0.0f, 0.0f, 1.0f);
    float4 tau, xi, voxelCenter;
    int2 sRange, tRange;
    float F2, sOffsetPerT, sPos, sShift, floorOfShift, fractOfShift, tRef, voxelValue;
    int s, t, z, pix, sLength, sOffset, tempLU;


    // determine voxel range processed by thread
    int voxStart, voxEnd;
    int voxelPerWorker = (int)par_loc.sf;
    int rest = get_image_width(voxelList) % get_local_size(0);

    if(!voxelPerWorker)
        rest = get_image_width(voxelList);
    if(localID < rest)
    {
        ++voxelPerWorker;
        voxStart =  localID   *voxelPerWorker;
        voxEnd   = (localID+1)*voxelPerWorker;
    }
    else
    {
        voxStart = rest*(voxelPerWorker+1) + (localID-rest)*voxelPerWorker;
        voxEnd   = voxStart + voxelPerWorker;
    }
    voxEnd = clamp(voxEnd, 0, get_image_width(voxelList));


    // determine t range (detector rows) processed by thread
    const int tStart = areaID * tRowsInLocMem;
    const int tEnd   = min( (areaID + 1) * tRowsInLocMem - 1, par_locI.s4 - 1);

    // initialize local memory array with zeros
    if(localID == 0)
        for(pix = 0; pix<localBufferSize; ++pix)
            localMemArray[pix] = 0;

    barrier(CLK_LOCAL_MEM_FENCE);

    for(int vox = voxStart; vox < voxEnd; ++vox)
    {
        // read voxel data: RGB are voxel coordinates, A is its (attenuation) value
        const float4 voxelData = read_imagef(voxelList, vox);
        rworld.x = voxelData.x + 0.5f * par_loc.s3;
        rworld.y = voxelData.y + 0.5f * par_loc.s4;
        rworld.z = voxelData.z + 0.5f * par_loc.s5;
        voxelValue = voxelData.s3;

        // calculate intersections for footprint function F2 (t direction)
        xi = projCorner4F2(rworld, &P_loc, &par_loc);
        if(xi.s3 < (float)tStart-0.5f)
            continue;
        if(xi.s0 >= (float)tEnd+0.5f)
            continue;

        voxelCenter = (float4)(voxelData.x, voxelData.y, voxelData.z, 1.0f);
        tRef = dot(P_loc.s4567, voxelCenter) / dot(P_loc.s89ab, voxelCenter);

        // calculate intersections for footprint function F1 (s direction)
        tau = projCorner4F1_corr(rworld, tRef, &P_loc, &par_loc);
        if(tau.s0 + 0.5f >= par_loc.s9 || tau.s3 + 0.5f < 0.0f)
            continue;

        // determine ranges for s
        sRange.s0 = max((int)(tau.s0 + 0.5f - 1.0f), 0);
        sRange.s1 = min((int)(tau.s3 + 0.5f + 1.0f), par_locI.s3);
        sLength	= sRange.s1 - sRange.s0;
        sOffset = sRange.s0 - detectOffset;
        sOffsetPerT = slopeOfEdge(rworld, &P_loc, &par_loc);

        // determine ranges for t
        tRange.s0  = max((int)(xi.s0 + 0.5f), tStart);
        tRange.s1  = min((int)(xi.s3 + 0.5f), tEnd);
        for(t = 0; t <= tRange.s1 - tRange.s0; ++t)
        {
            // compute shift of s footprint (due to potential angulation of voxel)
            sShift = ((float)tRange.s0 + (float)t - tRef) * sOffsetPerT;
            fractOfShift = fract(sShift, &floorOfShift);
            tempLU = (tRange.s0 + t)*par_locI.s3 + sOffset + (int)floorOfShift;

            F2 = gammaCT_f((float)(tRange.s0 + t), xi) * voxelValue;

            // s loop with on-the-fly recomputation of F1 footprint values (req. due
            // to potential fractional shifts in s-direction)
            for (s = 0; s <= sLength; ++s)
            {
                if(s + sRange.s0 + (int)floorOfShift < 0 ||
                   s + sRange.s0 + (int)floorOfShift >= par_locI.s3)
                    continue;

                sPos = (float)s - fractOfShift;
                atomic_addf_l(&localMemArray[ tempLU + s ], gammaCT_f((float)sRange.s0 + sPos, tau) * F2);
            }
        }
    }

    barrier(CLK_LOCAL_MEM_FENCE);

    if(localID == 0)
        for(int pix = 0; pix < boundary; ++pix)
            if(localMemArray[pix])
                projData[pix + projOffset] = localMemArray[pix]
                        * angleCorrAzi[aziCorrOffset + pix%par_locI.s3]
                        * angleCorrPol[polCorrOffset + pix/par_locI.s3 + tStart] * par_loc.s3;
            else
                projData[pix + projOffset] = 0.0f;
}

void minmax(float4* const xi)
{
    float temp = min(xi[0].s0,xi[0].s1);
    temp = min(temp,xi[0].s2);
    temp = min(temp,xi[0].s3);
    xi[0].s3 = max(xi[0].s3,xi[0].s0);
    xi[0].s3 = max(xi[0].s3,xi[0].s1);
    xi[0].s3 = max(xi[0].s3,xi[0].s2);
    xi[0].s0 = temp;
}

void sort(float4* const xi)
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

float gammaCT_f(const float p, const float4 coords)
{
    float2 s = p + (float2)(-0.5f,0.5f);

    return gamma13((float4)(max(s.x, coords.s0), min(s.y, coords.s1), coords.s01)) +
           gamma2( (float2)(max(s.x, coords.s1), min(s.y, coords.s2))) +
           gamma13((float4)(max(s.x, coords.s2), min(s.y, coords.s3), coords.s32));
}

float gamma13(const float4 b)
{
    if(b.s1 > b.s0)
    {
        float2 temp = (b.s01 - b.s22);
        temp = temp*temp;
        return (temp.s1 - temp.s0) / (2*(b.s3-b.s2));
    }
    else
        return 0.0f;
}

float gamma2(const float2 b)
{
    if(b.s1 > b.s0)
        return b.s1-b.s0;
    else
        return 0.0f;
}

// GPU (normal) VERSION
float4 projCorner4F2(float4 rworld, const float16* const P, const float16* const par)
{
    float4 xi, xiTemp, rEdge;

    // lower corner
    xiTemp.s0	= dot(P[0].s4567, rworld) / dot(P[0].s89ab,rworld);
    if(rworld.w)
        rEdge	= rworld + (float4)(-par[0].s3, 0.0f, 0.0f, 0.0f);
    xiTemp.s1	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab,rEdge);
    rEdge		= rworld + (float4)(0.0f, -par[0].s4, 0.0f, 0.0f);
    xiTemp.s2	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab,rEdge);
    rEdge		= rworld + (float4)(-par[0].s3, -par[0].s4, 0.0f, 0.0f);
    xiTemp.s3	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab, rEdge);
    minmax(&xiTemp);
    xi.s01 		= xiTemp.s03;

    // upper corner
    rworld.s2	= rworld.s2 - par[0].s5;
    xiTemp.s0	= dot(P[0].s4567, rworld) / dot(P[0].s89ab, rworld);
    rEdge 	  	= rworld + (float4)(-par[0].s3, 0.0f, 0.0f, 0.0f);
    xiTemp.s1	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab, rEdge);
    rEdge		= rworld + (float4)(0.0f, -par[0].s4, 0.0f, 0.0f);
    xiTemp.s2	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab, rEdge);
    rEdge		= rworld + (float4)(-par[0].s3, -par[0].s4, 0.0f, 0.0f);
    xiTemp.s3	= dot(P[0].s4567, rEdge)  / dot(P[0].s89ab, rEdge);
    minmax(&xiTemp);
    xi.s23  = xiTemp.s03;

    return xi;
}

float4  projCorner4F1_corr(float4 rworld, float tRef, const float16* const P, const float16* const par)
{
    float4 tau,rEdge;

    // first edge (reference for t line)
    rEdge 	  = rworld;
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s0 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // second edge
    rEdge 	  = rworld + (float4)(-par[0].s3, 0.0f,0.0f,0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s1 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // third edge
    rEdge 	  = rworld + (float4)(0.0f, -par[0].s4, 0.0f,0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s2 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);

    // fourth edge
    rEdge 	  = rworld + (float4)(-par[0].s3, -par[0].s4, 0.0f,0.0f);
    rEdge.z   = zForEqualT(tRef, rEdge, P);
    tau.s3 	  = dot(P[0].s0123,rEdge)  / dot(P[0].s89ab,rEdge);
    sort(&tau);

    return tau;
}

float slopeOfEdge(float4 rworld, const float16* const P, const float16* const par)
{
    rworld.s2 -= par[0].s5;
    float lowerS = dot(P[0].s0123, rworld) / dot(P[0].s89ab,rworld);
    float lowerT = dot(P[0].s4567, rworld) / dot(P[0].s89ab,rworld);
    rworld.s2 += par[0].s5;
    float upperS = dot(P[0].s0123, rworld) / dot(P[0].s89ab,rworld);
    float upperT = dot(P[0].s4567, rworld) / dot(P[0].s89ab,rworld);

    return (upperS - lowerS) / (upperT - lowerT);
}

float zForEqualT(float t, float4 edge, const float16* const P)
{
    return (1.0f / t * (P[0].s4 * edge.x + P[0].s5 * edge.y + P[0].s7)
            - (P[0].s8 * edge.x + P[0].s9 * edge.y + P[0].sb) ) / (P[0].sa - P[0].s6 / t);
}
