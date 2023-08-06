 // interpolating sampler with `0` as boundary color
constant sampler_t samp = CLK_NORMALIZED_COORDS_FALSE | CLK_ADDRESS_CLAMP | CLK_FILTER_LINEAR;

// the backsmear kernel - with only distance weights
kernel void simple_backprojector( uint z,
                                       uint viewNb,
                                       uint nbModules,
                                       constant float3* restrict volCorner_mm,
                                       constant float3* restrict voxelSize_mm,
                                       global const float4* restrict pMatsGlobal,
                                       local float4* restrict pMatsLoc,
                                       global float* restrict sliceBuf,
                                       read_only image3d_t proj,
                                       uint subSamplingFactor)
{
    event_t cpyToLocalEvent = async_work_group_copy(pMatsLoc,
                                                    pMatsGlobal + 3 * nbModules * viewNb,
                                                    3 * nbModules, 0);
    // get IDs
    const int x = get_global_id(0);
    const int y = get_global_id(1);
    // get dimensions
    const int X = get_global_size(0);
    const int Y = get_global_size(1);
    const size_t bufIdx = x + y*X; // 1D lookup index for z-slice buffer (result)
    const float4 projDim = convert_float4(get_image_dim(proj));

    const float4 subSampleStep_mm = (float4)((*voxelSize_mm), 0.0f) / (float)subSamplingFactor;

    // world coordinate vector of voxel (center) position for first subsample
    const float4 rCorner = (float4)( x * (*voxelSize_mm).x + (*volCorner_mm).x - (subSamplingFactor-1) * 0.5f * subSampleStep_mm.x,
                                     y * (*voxelSize_mm).y + (*volCorner_mm).y - (subSamplingFactor-1) * 0.5f * subSampleStep_mm.y,
                                     z * (*voxelSize_mm).z + (*volCorner_mm).z - (subSamplingFactor-1) * 0.5f * subSampleStep_mm.z,
                                     1.0f);

    uint xSub, ySub, zSub;
    float distWeight, totalCorr = 0.0f;
    float4 pMatRow0, pMatRow1, pMatRow2, projVal, r, p = (float4)0.0f;

    wait_group_events(1, &cpyToLocalEvent);

    // loop over all detector sub-modules
    for(zSub = 0; zSub < subSamplingFactor; ++zSub)
        for(ySub = 0; ySub < subSamplingFactor; ++ySub)
            for(xSub = 0; xSub < subSamplingFactor; ++xSub)
            {
                // shift to center of subsampled voxel
                r = rCorner + (float4)(xSub, ySub, zSub, 0.0f) * subSampleStep_mm;

                for(uint module = 0; module < nbModules; ++module)
                {
                    pMatRow0 = pMatsLoc[module * 3 + 0];
                    pMatRow1 = pMatsLoc[module * 3 + 1];
                    pMatRow2 = pMatsLoc[module * 3 + 2];

                    p.z = dot(pMatRow2, r);

                    p.x = dot(pMatRow0, r) / p.z;
                    if(p.x < -1.0f || p.x > projDim.x)
                        continue;

                    p.y = dot(pMatRow1, r) / p.z;
                    if(p.y < -1.0f || p.y > projDim.y)
                        continue;

                    // assume proper normalization of projection matrices for distance weighting
                    distWeight = p.z * p.z;
                    p.z = module + viewNb*nbModules; // module index

                    p += 0.5f;

                    projVal = read_imagef(proj, samp, p);

                    totalCorr += projVal.x / distWeight;
                }

            }

    sliceBuf[bufIdx] += totalCorr / pown((float)subSamplingFactor, 3);
}
