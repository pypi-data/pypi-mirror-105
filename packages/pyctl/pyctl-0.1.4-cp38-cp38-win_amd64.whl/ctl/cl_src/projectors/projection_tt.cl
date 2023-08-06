void 	sort(			float4* const tau);
void 	minmax(			float4* const xi);
float 	gammaCT(		const int p, 	const float4 coord);
float 	gamma2(			const float2 b);
float 	gamma13(		const float4 b);
float4 	projCorner4F2(	float4 rworld, 	const float16* const P_loc, const float16* const par);

kernel void proj( global float* restrict projData,
                  global float* restrict angleCorrAzi,
                  global float* restrict angleCorrPol,
                  global float16* restrict P,
                  global float16* restrict par,
                  read_only image3d_t cube,
                  int localBufferSize,
                  local int* restrict localMemArray)
{
    int xWorkerID = get_local_id(0);
    int projID 	  = get_group_id(1);
    int areaID 	  = get_group_id(2);
    const float16 P_loc           = P[projID];
    const float16 par_loc 		  = par[0];
    const int8    par_locI 		  = convert_int8(par[0].s0129abcd);
    const float   intConverter 	  = 1.0e7f / par_loc.se;
    const float	  invIntConverter = 1.0f / intConverter;

    const int angleAziCorrOffSet = projID * par_locI.s3;
    const int anglePolCorrOffSet = projID * par_locI.s4;
    const int tRowsInLocMem = localBufferSize / par_locI.s3;
    const int detectOffSet = localBufferSize * areaID;
    const int nbPixels     = par_locI.s3 * par_locI.s4;
    const int projOffSet   = detectOffSet + projID * nbPixels;
    const int boundary 	   = min(localBufferSize, nbPixels - detectOffSet);

    const float4 shift = (float4)(par_loc.s6 + par_loc.s3/2.0f,
                                  par_loc.s7 + par_loc.s4/2.0f,
                                  par_loc.s8 + par_loc.s5/2.0f,
                                  0.0f);
    float4 rworld 	   = (float4)(0.0f, 0.0f, 0.0f, 1.0f);
	float4 weight, tau, xi, rEdge;
	float F1[128], F2;
	int2 sRange, tRange;
	int4 voxel = (int4)0;
	int s,t,z,pix;
	int sLength, sOffSet, tempLU, tempTRange;

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
        for(voxel.s1 = 0; voxel.s1 < par_locI.s1; ++voxel.s1)
		{
			rworld.s1 = mad((float)voxel.s1,par_loc.s4,shift.y);
			// calculate footprint function F1
			tau.s0 	  = dot(P_loc.s0123,rworld) / dot(P_loc.s89ab,rworld);
			rEdge 	  = rworld + (float4)(-par_loc.s3, 0.0f,0.0f,0.0f);
			tau.s1 	  = dot(P_loc.s0123,rEdge)  / dot(P_loc.s89ab,rEdge);
			rEdge 	  = rworld + (float4)(0.0f, -par_loc.s4, 0.0f,0.0f);
			tau.s2 	  = dot(P_loc.s0123,rEdge)  / dot(P_loc.s89ab,rEdge);
			rEdge 	  = rworld + (float4)(-par_loc.s3, -par_loc.s4, 0.0f,0.0f);
			tau.s3 	  = dot(P_loc.s0123,rEdge)  / dot(P_loc.s89ab,rEdge);
			sort(&tau);

            if(tau.s0 + 0.5f >= par_loc.s9 || tau.s3 + 0.5f < 0.0f)
                continue;

            sRange.s0  = max((int)(tau.s0 + 0.5f),0);
            sRange.s1  = min((int)(tau.s3 + 0.5f),par_locI.s3-1);
            sLength	= clamp(sRange.s1 - sRange.s0, 0, 127);
            for (s = 0; s <= sLength; ++s)
                F1[s] = gammaCT(sRange.s0 + s,tau);
            sOffSet = sRange.s0 - detectOffSet;

			// ++++ Z-LOOP ++++
            for(z = 0; z < par_locI.s2; ++z)
			{
				// +++++ PROJ 0 +++++
				rworld.s2 = mad((float)z,par_loc.s5,shift.z);
				xi = projCorner4F2(rworld, &P_loc, &par_loc);
				if(xi.s3 < (float)tStart-0.5f)
					break;
					
				if(xi.s0 < (float)tEnd+0.5f)
				{
					// read absorption value
					voxel.s2   = z;
                    weight     = intConverter * read_imagef(cube, voxel);
					tRange.s0  = max((int)(xi.s0 + 0.5f), tStart);
					tRange.s1  = min((int)(xi.s3 + 0.5f), tEnd);
					tempTRange = sOffSet + tRange.s0*par_locI.s3;
					for(t = 0; t <= tRange.s1 - tRange.s0; ++t)
					{
						F2 = gammaCT(tRange.s0 + t, xi) * weight.s0;
                        tempLU = t * par_locI.s3 + tempTRange;
                        for (s = 0; s <= sLength; ++s)
                            atomic_add(&localMemArray[ tempLU + s ], (int)round(F1[s] * F2));
					}
				}
			}
			rworld.s2 = 0.0f;
		}
	}

	barrier(CLK_LOCAL_MEM_FENCE);

    // copy result from local memory array into global buffer
    if(xWorkerID == 0)
		for(int pix = 0; pix < boundary; ++pix)
            projData[pix + projOffSet] =  (float)localMemArray[pix] * invIntConverter * angleCorrAzi[angleAziCorrOffSet + pix%par_locI.s3]
                                                                                      * angleCorrPol[anglePolCorrOffSet + pix/par_locI.s3 + tStart]
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

float gammaCT(const int p, const float4 coords)
{
	float2 s  = (float2)p + (float2)(-0.5f,0.5f);

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
float4 projCorner4F2(float4 rworld, const float16* const P_loc, const float16* const par)
{
	float4 xi, xiTemp, rEdge;
	
	// lower corner
	xiTemp.s0	= dot(P_loc[0].s4567, rworld) / dot(P_loc[0].s89ab,rworld);	
	if(rworld.w)
		rEdge	= rworld + (float4)(-par[0].s3, 0.0f, 0.0f, 0.0f);
	xiTemp.s1	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab,rEdge);
	rEdge		= rworld + (float4)(0.0f, -par[0].s4, 0.0f, 0.0f);
	xiTemp.s2	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab,rEdge);
	rEdge		= rworld + (float4)(-par[0].s3, -par[0].s4, 0.0f, 0.0f);
	xiTemp.s3	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
	minmax(&xiTemp);
	xi.s01 		= xiTemp.s03;

	// upper corner
	rworld.s2	= rworld.s2 - par[0].s5;
	xiTemp.s0	= dot(P_loc[0].s4567, rworld) / dot(P_loc[0].s89ab, rworld);
	rEdge 	  	= rworld + (float4)(-par[0].s3, 0.0f, 0.0f, 0.0f);
	xiTemp.s1	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
	rEdge		= rworld + (float4)(0.0f, -par[0].s4, 0.0f, 0.0f);
	xiTemp.s2	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
	rEdge		= rworld + (float4)(-par[0].s3, -par[0].s4, 0.0f, 0.0f);
	xiTemp.s3	= dot(P_loc[0].s4567, rEdge)  / dot(P_loc[0].s89ab, rEdge);
	minmax(&xiTemp);
	xi.s23  = xiTemp.s03;

	return xi;
}
