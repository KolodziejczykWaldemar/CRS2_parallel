import numpy as np
import time
import pycuda.driver as drv
import pycuda.autoinit
from pycuda.compiler import SourceModule
from pycuda import gpuarray

code = """
    #include <curand_kernel.h>
    #include <math.h>  

    const int nstates = %(NGENERATORS)s;
    const int number = %(NUMBERS)s;
    const int maxNumber = %(MAXNUMBER)s;
    __device__ curandState_t* states[nstates*number];
extern "C"{
    __global__ void initkernel(int seed)
    {
        int tidx = threadIdx.x + blockIdx.x * blockDim.x;

        if (tidx < nstates*number) {
            curandState_t* s = new curandState_t;
            if (s != 0) {
                curand_init(seed, tidx, 0, s);
            }

            states[tidx] = s;
        }
    }

    __global__ void randfillkernel(float *values,float *sometable, int N)
    {
        int tidx = threadIdx.x + blockIdx.x * blockDim.x;

        if (tidx < nstates*number) {
            curandState_t s = *states[(tidx)];
            for(int i=tidx; i < N; i += blockDim.x * gridDim.x) {
                values[i]= sometable[(int)(trunc(maxNumber*curand_uniform(&s)))];
                
            }
            *states[tidx] = s;
        }
    }
    }
"""

N = 1024
numbers=50
nvalues = 1024*numbers
mod = SourceModule(code % { "NGENERATORS" : N,"NUMBERS" : numbers,"MAXNUMBER" :nvalues}, no_extern_c=True)
init_func = mod.get_function("initkernel")
fill_func = mod.get_function("randfillkernel")

seed = np.int32(127362363)

init_func(drv.In(seed), block=(32,1,1), grid=(50,1,1))
gdata = gpuarray.zeros(nvalues, dtype=np.float32)
data = np.array(range(0,nvalues), dtype=np.float32)

start = time.time()
fill_func(gdata,drv.In(data),drv.In(np.int32(nvalues)), block=(32,1,1), grid=(50,1,1))
end = time.time()

print(end-start)



