kernel
void
ArrayMult( global const float *dA, global const float *dB, global float *dC )
{
    int gid = get_global_id( 0 );

    dC[gid] = dA[gid] * dB[gid];
}

kernel
void
ArrayMultAdd( global const float *dA, global const float *dB, global const float *dC, global  float *dD )
{
    int gid = get_global_id( 0 );

    dD[gid] = dA[gid] * dB[gid] + dC[gid];
}

kernel
void ArrayMultRec(global const float *dA, global const float *dB, global float *dC, 
        global float *dD, local float *part)
{
    int gid = get_global_id( 0 );
    int tid = get_local_id( 0 ); 
    int wgid = get_group_id( 0 ); // work-group number
    int numItems = get_local_size( 0 );
    int gs = get_num_groups(0);

    part[tid] = dA[gid] * dB[gid];

    /* local partial sum */
    barrier(CLK_LOCAL_MEM_FENCE);
    for (int d = numItems >> 1; d > 0; d >>= 1) {
        if (tid < d) part[tid] += part[tid + d];
        barrier(CLK_LOCAL_MEM_FENCE);
    }

    if (tid == 0) {
        dC[wgid] = part[0];
        dD[wgid] = part[0];
    }

    /* global reduction */
    barrier(CLK_GLOBAL_MEM_FENCE);

    if (wgid == 0) {
        float rec = dC[0];

        for (int i = 1; i < gs; i++) rec += dC[i];

        dC[0] = rec;
    }
}
