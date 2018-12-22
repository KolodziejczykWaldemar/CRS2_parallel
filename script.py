import random as rn
import time
import numpy as np
import helpers as hp
import functions as f
import crs2
import crs2_shared_memory as crs2SM
import crs3
import crs3_shared_memory as crs3SM



number_of_experiments=[1,2,3,4]
ns=[2,3,4,5,6]
cpus=[2,3,4,5,6,7,8]
for n in ns:
	f.n=n
	for i in number_of_experiments:
		crs2.crs2()
		crs3.crs3()
		for cpu in cpus:
			crs2SM.crs2SM(cpu)
			crs3SM.crs3SM(cpu)

	

