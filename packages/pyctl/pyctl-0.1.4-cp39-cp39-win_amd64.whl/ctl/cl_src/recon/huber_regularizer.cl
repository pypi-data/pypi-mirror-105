constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

void readNeighbors(read_only image3d_t oldVol, int x, int y, int z,
                   float8* nb1, float16* nb2, float8* nb3);
float computeGradient(float refVal, float8 nb1, float16 nb2, float8 nb3,
                      float b, float betaZ, float betaXY, float directZ);

// regularizer kernel - with five additional arguments
kernel void filter( read_only image3d_t oldVol,
                    global float* newVol,
                    uint z,
                    float param,
                    float huberEdgeHU,
                    float betaZ,
                    float betaXY,
                    float	directZ)
{
    // get IDs
    const int x = get_global_id(0);
    const int y = get_global_id(1);
    const int4 vox = (int4)(x, y, z, 0);

    // #### PARAMETERS ####
    const float b = huberEdgeHU * 0.02269f/1000.0f; // +- huberEdgeHU HU (at 50 keV)
    // #### 			####

    // get neighbors
    float8  nb1, nb3;
    float16 nb2;
    readNeighbors(oldVol, x, y, z, &nb1, &nb2, &nb3);

    // compute gradient
    const float refVal = read_imagef(oldVol, vox).x;
    const float grad = computeGradient(refVal, nb1, nb2, nb3,
                                       b, betaZ, betaXY, directZ);

    write_bufferf(newVol, vox, refVal - param * grad, oldVol);
}


// neighbors
inline void readNeighbors(read_only image3d_t oldVol,
                          int x,
                          int y,
                          int z,
                          float8*  nb1,
                          float16* nb2,
                          float8*  nb3)
{
    float4 value;
    // order1 - nearest
    value = read_imagef(oldVol, sampler, (float4)(x, y, z - 1, 0));
    nb1[0].s0 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y, z + 1, 0));
    nb1[0].s1 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y - 1, z, 0));
    nb1[0].s2 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y + 1, z, 0));
    nb1[0].s3 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y, z, 0));
    nb1[0].s4 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y, z, 0));
    nb1[0].s5 = value.x;

    // order2 - sqrt(2)
    value = read_imagef(oldVol, sampler, (float4)(x, y - 1, z - 1, 0));
    nb2[0].s0 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y + 1, z - 1, 0));
    nb2[0].s1 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y - 1, z + 1, 0));
    nb2[0].s2 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x, y + 1, z + 1, 0));
    nb2[0].s3 = value.x;

    value = read_imagef(oldVol, sampler, (float4)(x - 1, y, z - 1, 0));
    nb2[0].s4 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y, z - 1, 0));
    nb2[0].s5 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y, z + 1, 0));
    nb2[0].s6 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y, z + 1, 0));
    nb2[0].s7 = value.x;

    value = read_imagef(oldVol, sampler, (float4)(x - 1, y - 1, z, 0));
    nb2[0].s8 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y + 1, z, 0));
    nb2[0].s9 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y - 1, z, 0));
    nb2[0].sa = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y + 1, z, 0));
    nb2[0].sb = value.x;

    // order3 - sqrt(3)
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y - 1, z - 1, 0));
    nb3[0].s0 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y + 1, z - 1, 0));
    nb3[0].s1 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y - 1, z + 1, 0));
    nb3[0].s2 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x - 1, y + 1, z + 1, 0));
    nb3[0].s3 = value.x;

    value = read_imagef(oldVol, sampler, (float4)(x + 1, y - 1, z - 1, 0));
    nb3[0].s4 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y + 1, z - 1, 0));
    nb3[0].s5 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y - 1, z + 1, 0));
    nb3[0].s6 = value.x;
    value = read_imagef(oldVol, sampler, (float4)(x + 1, y + 1, z + 1, 0));
    nb3[0].s7 = value.x;
}

inline float computeGradient(float refVal, float8 nb1, float16 nb2, float8 nb3,
                             float b, float betaZ, float betaXY, float directZ)
{
    const float8 wTmp1 = (float8)(M_SQRT1_2_F*betaZ);
    const float4 wTmp2 = (float4)(M_SQRT1_2_F*betaXY);

    const float8  weightsNb1 = (float8)(betaZ*directZ,betaZ*directZ,betaXY,betaXY,betaXY,betaXY,0.0f,0.0f);
    const float16 weightsNb2 = (float16)(wTmp1, wTmp2, (float4)(0.0f));
    const float8  weightsNb3 = (float8)(betaZ / sqrt(3.0f));

    const float8  diffNb1 = (float8)(refVal)  - nb1;
    const float16 diffNb2 = (float16)(refVal) - nb2;
    const float8  diffNb3 = (float8)(refVal)  - nb3;

    // Huber edge
    const float8  potV1	= clamp(diffNb1, -b, b);
    const float16 potV2	= clamp(diffNb2, -b, b);
    const float8  potV3	= clamp(diffNb3, -b, b);

    const float grad = dot(potV1.s0123, weightsNb1.s0123) + dot(potV1.s45,   weightsNb1.s45) +
                       dot(potV2.s0123, weightsNb2.s0123) + dot(potV2.s4567, weightsNb2.s4567) + dot(potV2.s89ab, weightsNb2.s89ab) +
                       dot(potV3.s0123, weightsNb3.s0123) + dot(potV3.s4567, weightsNb3.s4567);

    return grad;
}
