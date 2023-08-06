// filter kernel - with an additional buffer
kernel void filter( read_only image3d_t oldProj,
                    global float* newProj,
                    uint view,
                    global const float* Kmats)
{
    // get IDs
    const int u = get_global_id(0);
    const int v = get_global_id(1);
    const int m = get_global_id(2);

    const int M = get_image_depth(oldProj);

    const int4 pix = (int4)(u, v, m, 0);
    const float refVal = read_imagef(oldProj, pix).x;
    const int kOffset = 9 * (view*M + m);

    // back substitution to find 'd' in K*d = [x,y,1]^t
    float3 direction;
    direction.z = 1.0;
    direction.y = (v - Kmats[5 + kOffset]) / Kmats[4 + kOffset];
    direction.x = (u - direction.y * Kmats[1 + kOffset] - Kmats[2 + kOffset]) / Kmats[0 + kOffset];

    // cosine to z-axis = <unitDirection, [0 0 1]^t>
    float cosine = direction.z / length(direction);

    write_bufferf(newProj, pix, cosine*refVal, oldProj);
}
