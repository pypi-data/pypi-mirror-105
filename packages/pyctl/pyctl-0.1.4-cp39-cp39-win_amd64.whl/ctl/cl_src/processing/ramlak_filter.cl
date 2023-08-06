constant sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP | CLK_FILTER_NEAREST;

// regularizer kernel - with no additional arguments
kernel void filter( read_only image3d_t oldProj,
                    global float* newProj,
                    uint view,
                    float scaling)
{
    // get IDs
    const int u = get_global_id(0);
    const int v = get_global_id(1);

    const int halfFilterSize = get_image_width(oldProj);

    // single module case (using auto combine in host code)
    const int4 pix = (int4)(u, v, 0, 0);

    float sum = 0.25f * read_imagef(oldProj, pix).x;

    for(int shift = 1; shift < halfFilterSize; shift += 2)
    {
        const float filterElement = -1.0f / pown((float)(shift) * M_PI_F, 2);
        sum += filterElement * read_imagef(oldProj, sampler, pix + (int4)(shift, 0, 0, 0)).x +
               filterElement * read_imagef(oldProj, sampler, pix - (int4)(shift, 0, 0, 0)).x;
    }

    write_bufferf(newProj, pix, scaling*sum, oldProj);
}
