void  sort(float4* const tau);
float gammaCT(const int p, const float4 coord);
float gamma13(const float4 b);

inline float gamma2(const float2 b) {return (b.s1 > b.s0) ? b.s1-b.s0 : 0.0f;}

kernel void proj( global float* restrict projData,
                  global float* restrict angleCorrAzi,
                  global float* restrict angleCorrPol,
                  global float16* restrict P,
                  global float16* restrict par,
                  read_only image3d_t cube,
                  int localBufferSize,
                  local float* restrict localMemArray)
{
    int x_worker = get_local_id(0);
    int projID 	 = get_group_id(1);
    int areaID 	 = get_group_id(2);
    const float16 P_loc           = P[projID];
    const float16 par_loc 		  = par[0];
    const int8    par_locI 		  = convert_int8(par[0].s0129abcd);

    const int angleAziCorrOffSet  = projID * par_locI.s3;
    const int anglePolCorrOffSet  = projID * par_locI.s4;
    const int tRowsInLocMem = localBufferSize / par_locI.s3;
    const int detectOffSet  = localBufferSize * areaID;
    const int nbPixels      = par_locI.s3 * par_locI.s4;
    const int projOffSet    = detectOffSet + projID * nbPixels;
    const int boundary 	    = min(localBufferSize, nbPixels - detectOffSet);

    const float4 shift  = (float4)(par_loc.s6 + par_loc.s3/2.0f,
                                   par_loc.s7 + par_loc.s4/2.0f,
                                   par_loc.s8 + par_loc.s5/2.0f,
                                   0.0f);
    const float4 shift2 = (float4)(- par_loc.s3/2.0f,
                                   - par_loc.s4/2.0f,
                                   0.0f,
                                   0.0f);
    const float  tShift = par_loc.s5 * P_loc.s6;
    const float  pShift = par_loc.s5 * P_loc.sa;
    const float  zShift = shift.z - par_loc.s5;
    float4 rworld = (float4)(0.0f, 0.0f, 0.0f, 1.0f);
    float4 weight, tauTemp, divTemp;
    float2 t_plusMinus, rEdge;
    float F1[128];
    int2 sRange;
    int4 voxel = (int4)0;
    int sLength, sOffSet;

    // determine x range processed by thread
    int xStart, xEnd;
    int xPerWorker = (int)par_loc.sf;
    int rest = par_locI.s0 % get_local_size(0);
    if(!xPerWorker)
        rest = par_locI.s0;
    if(x_worker < rest)
    {
        ++xPerWorker;
        xStart =  x_worker   *xPerWorker;
        xEnd   = (x_worker+1)*xPerWorker;
    }
    else
    {
        xStart = rest*(xPerWorker+1) + (x_worker-rest)*xPerWorker;
        xEnd   = xStart + xPerWorker;
    }
    xEnd = clamp(xEnd, 0, par_locI.s0);

    // determine t range (detector rows) processed by thread
    const int tStart = areaID * tRowsInLocMem;
    const int tEnd   = min( (areaID + 1) * tRowsInLocMem - 1, par_locI.s4 - 1);
    const float2 limit  = (float2)((float)tStart - 0.5f, (float)tEnd + 0.5f);

    // initialize local memory array with zeros
    if(x_worker == 0)
        for(int pix = 0; pix<localBufferSize; ++pix)
            localMemArray[pix] = 0.0f;

    barrier(CLK_LOCAL_MEM_FENCE);

    for(voxel.s0 = xStart; voxel.s0 < xEnd; ++voxel.s0)
    {
        rworld.s0 = (float)voxel.s0 * par_loc.s3 + shift.x;

        rEdge   = (float2)(rworld.s0, rworld.s0 - par_loc.s3);
        tauTemp = P_loc.s0*rEdge.s0101 + P_loc.s3;
        divTemp = P_loc.s8*rEdge.s0101 + P_loc.sb;

        for(voxel.s1 = 0; voxel.s1 < par_locI.s1; ++voxel.s1)
        {

            rworld.s1 = (float)voxel.s1 * par_loc.s4 + shift.y;

            rEdge = (float2)(rworld.s1, rworld.s1 - par_loc.s4);
            float4 mult = P_loc.s1199*rEdge.s0101;
            float4 tau  = (tauTemp + mult.s0011) / (divTemp + mult.s2233);

            sort(&tau);

            if(tau.s0 + 0.5f >= par_loc.s9 || tau.s3 + 0.5f < 0.0f)
                continue;

            sRange.s0  = max((int)(tau.s0 + 0.5f), 0);
            sRange.s1  = min((int)(tau.s3 + 0.5f), par_locI.s3 - 1);
            sLength	= clamp(sRange.s1 - sRange.s0, 0, 127);
            for(int s = 0; s <= sLength; ++s)
                F1[s] = gammaCT(sRange.s0 + s, tau);

            sOffSet = sRange.s0 - detectOffSet;

            // ++++ Z-LOOP ++++
            // initiate z-loop...
            float4 rworldZ 	     = rworld + shift2;
            float  divisorXY 	 = P_loc.s8*rworldZ.s0 + P_loc.s9*rworldZ.s1 + P_loc.sb;
            float  t_plusMinusXY = P_loc.s4*rworldZ.s0 + P_loc.s5*rworldZ.s1 + P_loc.s7;
            // start z-loop...
            for(int z = 0; z < par_locI.s2; ++z)
            {
                rworldZ.s2 		= (float)z * par_loc.s5 + zShift;

                float divisor 	= mad(P_loc.sa, rworldZ.s2, divisorXY);
                t_plusMinus.s1  = mad(P_loc.s6, rworldZ.s2, t_plusMinusXY) / divisor;

                if(t_plusMinus.s1 < limit.s0)
                    break;

                t_plusMinus.s0 = t_plusMinus.s1 + tShift / (pShift + divisor);
                if(t_plusMinus.s0 >= limit.s1)
                    continue;

                // read absorption value
                voxel.s2 = z;
                weight   = read_imagef(cube, voxel);

                int2 tRange = (int2)(max((int)(t_plusMinus.s0 + 0.5f), tStart), min((int)(t_plusMinus.s1 + 0.5f), tEnd));
                int tempLU = sOffSet + tRange.s0*par_locI.s3;
                for (int t = 0; t <= tRange.s1 - tRange.s0; ++t)
                {
                    float F2 = (min((float)(tRange.s0+t) + 0.5f, t_plusMinus.s1) - max((float)(tRange.s0+t) - 0.5f, t_plusMinus.s0))*weight.s0;
                    for(int s = 0; s <= sLength; ++s)
                        atomic_addf_l(&localMemArray[ tempLU + s ], F1[s] * F2);
                    tempLU += par_locI.s3;
                }
            }
        }
    }

    barrier(CLK_LOCAL_MEM_FENCE);

    // copy result from local memory array into global buffer
    if(x_worker == 0)
        for(int pix = 0; pix < boundary; ++pix)
            projData[pix + projOffSet] =  (float)localMemArray[pix] * angleCorrAzi[angleAziCorrOffSet + pix%par_locI.s3]
                                                                    * angleCorrPol[anglePolCorrOffSet + pix/par_locI.s3 + tStart]
                                                                    * par_loc.s3;
}

void sort(float4* const xi)
{
	(*xi).s01 = ((*xi).s0 < (*xi).s1) ? (*xi).s01 : (*xi).s10;
	(*xi).s12 = ((*xi).s1 < (*xi).s2) ? (*xi).s12 : (*xi).s21;
	(*xi).s23 = ((*xi).s2 < (*xi).s3) ? (*xi).s23 : (*xi).s32;
	(*xi).s01 = ((*xi).s0 < (*xi).s1) ? (*xi).s01 : (*xi).s10;
	(*xi).s12 = ((*xi).s1 < (*xi).s2) ? (*xi).s12 : (*xi).s21;
	(*xi).s01 = ((*xi).s0 < (*xi).s1) ? (*xi).s01 : (*xi).s10;
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
		return (temp.s1 - temp.s0) / (2.0f*(b.s3-b.s2));
	}
	else
		return 0.0f;
} 
