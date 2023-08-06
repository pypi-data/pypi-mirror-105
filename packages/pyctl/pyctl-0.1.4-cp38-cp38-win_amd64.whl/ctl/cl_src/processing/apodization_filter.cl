constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP | CLK_FILTER_NEAREST;

// regularizer kernel - with no additional arguments
kernel void filter( read_only image3d_t oldProj,
                    global float* newProj,
                    uint view,
                    float postScaling,
                    constant float* filterElements)
{
    // get IDs
    const int u = get_global_id(0);
    const int v = get_global_id(1);

    const int halfFilterSize = get_image_width(oldProj);

    // single module case (using auto combine in host code)
    const int4 pix = (int4)(u, v, 0, 0);

    float sum = 0.f;

    for(int shift = 0; shift < halfFilterSize - u; ++shift)
    {
        sum += filterElements[shift] * read_imagef(oldProj, sampler, pix + (int4)(shift, 0, 0, 0)).x;
    }
    for(int shift = 1; shift <= u; ++shift)
    {
        sum += filterElements[2*halfFilterSize-shift] * read_imagef(oldProj, sampler, pix - (int4)(shift, 0, 0, 0)).x;
    }

    write_bufferf(newProj, pix, postScaling * sum, oldProj);
}
