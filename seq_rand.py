import numpy
import time
import random as rn

a = numpy.array(range(0,10240*50))
start = time.time()
R_chosen = rn.sample(range(0,10240*50), 10240*50)
end = time.time()


print(end-start)