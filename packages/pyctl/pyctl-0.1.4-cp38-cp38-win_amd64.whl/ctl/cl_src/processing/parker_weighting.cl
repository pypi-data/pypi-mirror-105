#pragma OPENCL EXTENSION cl_khr_3d_image_writes : enable

// regularizer kernel - with no additional arguments
kernel void filter( read_only  image3d_t oldProj,
                    write_only image3d_t newProj,
                    uint view,
                    float fanAngle,
                    int flipCS,
                    global float* _fx,
                    global float* _px,
                    global float* _alpha)
{
    // get IDs
    const int u = get_global_id(0);
    const int v = get_global_id(1);

    const int M = get_image_depth(oldProj);

    const float fx = _fx[view];
    const float px = _px[view];
    const float alpha = _alpha[view];
    const float beta = flipCS ? -atan((u - px) / fx)
                              : atan((u - px) / fx);

    // single module version
    const int4 pix = (int4)(u, v, 0, 0);
    const float refVal = read_imagef(oldProj, pix).x;

    float weight;
    if(0 <= alpha && alpha <= (fanAngle - 2.0f*beta))
        weight = pown(sin(M_PI_4_F * alpha / (0.5f * fanAngle - beta)), 2);
    else if((fanAngle - 2.0f*beta) <= alpha && alpha <= (M_PI_F - 2.0f * beta))
        weight = 1.0f;
    else if((M_PI_F - 2.0f * beta) <= alpha && alpha <= M_PI_F + fanAngle)
        weight = pown(sin(M_PI_4_F * (M_PI_F + fanAngle - alpha) / (0.5f * fanAngle + beta)), 2);
    else
        weight = 0.0f;

    write_imagef(newProj, pix, (float4)(weight * refVal));

}
