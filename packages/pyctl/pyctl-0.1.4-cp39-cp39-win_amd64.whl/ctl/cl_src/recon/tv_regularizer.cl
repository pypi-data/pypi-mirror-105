constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP_TO_EDGE | CLK_FILTER_NEAREST;

void readNeighbors(read_only image3d_t oldVol, int x, int y, int z,
                   float8* nb1, float16* nb2, float8* nb3);
float computeGradient(float refVal, float8 nb1, float16 nb2, float8 nb3);

// regularizer kernel - with one additional argument
kernel void filter( read_only image3d_t oldVol,
                    global float* newVol,
                    uint z,
                    float param)
{
    // get IDs
    const int x = get_global_id(0);
    const int y = get_global_id(1);
    const int4 vox = (int4)(x, y, z, 0);

    // get neighbors
    float8  nb1, nb3;
    float16 nb2;
    readNeighbors(oldVol, x, y, z, &nb1, &nb2, &nb3);

    // compute gradient
    const float refVal = read_imagef(oldVol, vox).x;
    const float grad = computeGradient(refVal, nb1, nb2, nb3); // gradient will be [-1, 1] HU

    write_bufferf(newVol, vox, refVal + param * grad, oldVol);
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

inline float computeGradient(float refVal,
                             float8  nb1,
                             float16 nb2,
                             float8  nb3)
{
    // maximum gradient of 1HU (at 50 keV); scaled later by parameter 'regul'
    const float normalize = 0.02269f / 1000.0f / (6.0f * 1.0f + 12.0f * 1.0f/sqrt(2.0f) + 8.0f * 1.0f/sqrt(3.0f));

    const float4 weightsNb1 = (float4)(normalize);              // order1 neighbors: 1.0
    const float4 weightsNb2 = (float4)(normalize / sqrt(2.0f)); // order2 neighbors: sqrt(2.0)
    const float4 weightsNb3 = (float4)(normalize / sqrt(3.0f)); // order3 neighbors: sqrt(3.0)

    const float8  signNb1 = sign(nb1 - (float8)(refVal));
    const float16 signNb2 = sign(nb2 - (float16)(refVal));
    const float8  signNb3 = sign(nb3 - (float8)(refVal));

    const float grad = dot(signNb1.s0123, weightsNb1) + dot(signNb1.s45,   weightsNb1.s01) +
                       dot(signNb2.s0123, weightsNb2) + dot(signNb2.s4567, weightsNb2) + dot(signNb2.s89ab, weightsNb2) +
                       dot(signNb3.s0123, weightsNb3) + dot(signNb3.s4567, weightsNb3);

    return grad;
}
