// the nullifier kernel
kernel void nullify_buffer( global float* sliceBuf )
{
    const int X = get_global_size(0);
    const size_t idx = get_global_id(0) + get_global_id(1)*X;

    sliceBuf[idx] = 0.0f;
}
