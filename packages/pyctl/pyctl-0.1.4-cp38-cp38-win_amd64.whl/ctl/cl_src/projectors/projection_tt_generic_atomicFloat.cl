void 	sort(float4* const tau);
void 	minmax(float4* const xi);
float   gammaCT_f(const float p, const float4 coords);
float 	gamma2(const float2 b);
float 	gamma13(const float4 b);
float   interpF1(const float* F1, int sLength, float sPos);
float4 	projCorner4F2(float4 rworld, const float16* const P, const float16* const par);
float4  projCorner4F1_corr(float4 rworld, float tRef, const float16* const P, const float16* const par);
float   slopeOfEdge(float4 rworld, const float16* const P, const float16* const par);
float   zForEqualT(float t, float4 edge, const float16* const P);

kernel void proj( global float* restrict projData,
                  global float* restrict angleCorrAzi,
                  global float* restrict angleCorrPol,
                  global float16* restrict P,
                  global float16* restrict par,
                  read_only image3d_t cube,
                  int localBufferSize,
                  local float* restrict localMemArray )
{
    int xWorkerID = get_local_id(0);
    int projID 	  = get_group_id(1);
    int areaID 	  = get_group_id(2);
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
    const float4 shift = (float4)(par_loc.s6 + par_loc.s3/2.0f,
                                  par_loc.s7 + par_loc.s4/2.0f,
                                  par_loc.s8 + par_loc.s5/2.0f,
                                  0.0f);
    // variable declarations
    float4 rworld 	   = (float4)(0.0f, 0.0f, 0.0f, 1.0f);
    float4 tau, xi, rEdge, voxelCenter;
    int4 voxel = (int4)0;
    int2 sRange, tRange;
    float F2, sOffsetPerT, sPos, sShift, floorOfShift, fractOfShift, tRef, voxelValue;
    int s, t, z, pix, sLength, sOffset, tempLU;

    // determine x range processed by thread
    int xStart, xEnd;
    int xPerWorker = (int)par_loc.sf;
    int rest = par_locI.s0 % get_local_size(0);
    if(!xPerWorker)
        rest = par_locI.s0;
    if(xWorkerID < rest)
    {
        ++xPerWorker;
        xStart =  xWorkerID   *xPerWorker;
        xEnd   = (xWorkerID+1)*xPerWorker;
    }
    else
    {
        xStart = rest*(xPerWorker+1) + (xWorkerID-rest)*xPerWorker;
        xEnd   = xStart + xPerWorker;
    }
    xEnd = clamp(xEnd, 0, par_locI.s0);

    // determine t range (detector rows) processed by thread
    const int tStart = areaID * tRowsInLocMem;
    const int tEnd   = min( (areaID + 1) * tRowsInLocMem - 1, par_locI.s4 - 1);

    // initialize local memory array with zeros
    if(xWorkerID == 0)
        for(pix = 0; pix<localBufferSize; ++pix)
            localMemArray[pix] = 0;

	barrier(CLK_LOCAL_MEM_FENCE);

    for(voxel.s0 = xStart; voxel.s0 < xEnd; ++voxel.s0)
	{
		rworld.s0 = mad((float)voxel.s0,par_loc.s3,shift.x);
		for(voxel.s1 = 0; voxel.s1<par_locI.s1; ++voxel.s1)
		{
			rworld.s1 = mad((float)voxel.s1,par_loc.s4,shift.y);
			// ++++ Z-LOOP ++++
            for(z = 0; z < par_locI.s2; ++z)
			{
				// +++++ PROJ 0 +++++
				rworld.s2 = mad((float)z, par_loc.s5, shift.z);

                // calculate intersections for footprint function F2 (t direction)
                xi = projCorner4F2(rworld, &P_loc, &par_loc);
				if(xi.s3 < (float)tStart-0.5f)
					break;		
                if(xi.s0 >= (float)tEnd+0.5f)
                    continue;

                voxelCenter = rworld - 0.5f * (float4)(par_loc.s3, par_loc.s4, par_loc.s5, 0.0f);
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

                // read absorption value
                voxel.s2   = z;
                voxelValue = read_imagef(cube, voxel).s0;

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
                        if(s + sRange.s0 + (int)floorOfShift < 0.0 ||
                           s + sRange.s0 + (int)floorOfShift >= par_locI.s3)
                            continue;

                        sPos = (float)s - fractOfShift;
                        atomic_addf_l(&localMemArray[ tempLU + s ], gammaCT_f((float)sRange.s0 + sPos,tau) * F2);
                    }
                }
			}
		}
	}

	barrier(CLK_LOCAL_MEM_FENCE);

 if(xWorkerID == 0)
     for(int pix = 0; pix < boundary; ++pix)
         projData[pix + projOffset] = localMemArray[pix] * angleCorrAzi[aziCorrOffset + pix%par_locI.s3]
                                                         * angleCorrPol[polCorrOffset + pix/par_locI.s3 + tStart]
                                                         * par_loc.s3;
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

float interpF1(const float* F1, int sLength, float sPos)
{
    int leftIdx  = (int)floor(sPos);
    int rightIdx = (int)ceil(sPos);

    bool leftIdxOutside = (leftIdx < 0) || (leftIdx > sLength);
    bool rightIdxOutside = (rightIdx < 0) || (rightIdx > sLength);

    float leftVal  = leftIdxOutside  ? 0.0f : F1[leftIdx];
    float rightVal = rightIdxOutside ? 0.0f : F1[rightIdx];

    float weight = (float)rightIdx - sPos;
    return leftVal * weight + rightVal * (1.0 - weight);
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
