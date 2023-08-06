#define b(alpha) (q * (fanAngle - 2.0f * (alpha) + overscan))

float S(float beta);
float weight(float beta, float alpha, float fanAngle, float overscan, float q);


// regularizer kernel - with no additional arguments
kernel void filter( read_only image3d_t oldProj,
                    global float* newProj,
                    uint view,
                    float fanAngle,
                    float overscan,
                    float q,
                    int rotDirection,
                    global float* _fx,
                    global float* _px,
                    global float* _beta)
{
    // get IDs
    const int u = get_global_id(0);
    const int v = get_global_id(1);

    const int M = get_image_depth(oldProj);

    const float fx = _fx[view];
    const float px = _px[view];
    const float beta = _beta[view];
    const float alpha = (float)rotDirection * atan((px - u) / fx);

    // single module version
    const int4 pix = (int4)(u, v, 0, 0);
    const float refVal = read_imagef(oldProj, pix).x;

    float wgt = 0.0f;

    if(beta >= 0.0f && beta < fanAngle - 2.0f * alpha + overscan)
        wgt = weight(beta, alpha, fanAngle, overscan, q);
    else if(beta < M_PI_F - 2.0f * alpha)
        wgt = 1.0f;
    else if(beta <= M_PI_F + fanAngle + overscan)
        wgt = 1.0f - weight(beta - M_PI_F + 2.0f * alpha, -alpha, fanAngle, overscan, q);

    write_bufferf(newProj, pix, wgt*refVal, oldProj);
}

inline float S(float beta)
{
    return (beta <= -0.5f) ? 0
           : (beta >= 0.5) ? 1.0f
           : 0.5f * (1.0f + sin(M_PI_F * beta));
}

inline float weight(float beta, float alpha, float fanAngle, float overscan, float q)
{
    return 0.5f * (S((beta) / b((alpha)) - 0.5f)
                   + S(((beta) - fanAngle + 2.0f*(alpha) - overscan) / b((alpha)) + 0.5f));
}

