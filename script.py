from crs2_shared_memory import CRS2_multi
from crs3_shared_memory import CRS3_multi
from crs2_local_memory import CRS2_local
from crs3_local_memory import CRS3_local
from crs2 import CRS2
from crs3 import CRS3

if __name__ == '__main__':
    ns = [2, 3]
    cpus = [2, 3]
    ex_num = 2
    func_nums = [1, 2]

    #  For CRS2 sequential:
    # for fun_num in func_nums:
    #     for n in ns:
    #         result_file = open("CRS2_{}_{}.txt".format(fun_num, n), "a")
    #         for ex in range(ex_num):
    #             iter_time, rand_time, full_time, result = CRS2(FUNCTION_NUMBER=fun_num, vec_len=n)
    #             result_str = 'Experiment: {} \n' \
    #                          'Function number: {} \n' \
    #                          'Vector dimensionality: {}\n' \
    #                          'Iteration time: \n{:.4f} s\n' \
    #                          'Randomization time: \n{:.4f} s\n' \
    #                          'Full time: \n{:.4f} s\n' \
    #                          'Result: \n{} \n\n\n'.format(ex + 1, fun_num, n, iter_time,  rand_time, full_time, result)
    #
    #             result_file.write(result_str)
    #         result_file.close()
    #
    #
    # #  For CRS3 sequential:
    # for fun_num in func_nums:
    #     for n in ns:
    #         result_file = open("CRS3_{}_{}.txt".format(fun_num, n), "a")
    #         for ex in range(ex_num):
    #             iter_time, rand_time, full_time, result = CRS3(FUNCTION_NUMBER=fun_num, vec_len=n)
    #             result_str = 'Experiment: {} \n' \
    #                          'Function number: {} \n' \
    #                          'Vector dimensionality: {}\n' \
    #                          'Iteration time: \n{:.4f} s\n' \
    #                          'Randomization time: \n{:.4f} s\n' \
    #                          'Full time: \n{:.4f} s\n' \
    #                          'Result: \n{} \n\n\n'.format(ex + 1, fun_num, n, iter_time,  rand_time, full_time, result)
    #
    #             result_file.write(result_str)
    #         result_file.close()
    #
    #
    #
    # # For CRS2 shared memory:
    # for fun_num in func_nums:
    #     for n in ns:
    #         for cpu in cpus:
    #             result_file = open("CRS2SM_{}_{}_{}.txt".format(fun_num, n, cpu), "a")
    #             for ex in range(ex_num):
    #                 iter_time, rand_time, full_time, result = CRS2_multi(cpu_num=cpu,
    #                                                                      FUNCTION_NUMBER=fun_num,
    #                                                                      vec_len=n)
    #                 result_str = 'Experiment: {} \n' \
    #                              'Function number: {} \n' \
    #                              'Vector dimensionality: {}\n' \
    #                              'CPU number: {} \n' \
    #                              'Iteration time: \n{:.4f} s\n' \
    #                              'Randomization time: \n{:.4f} s\n' \
    #                              'Full time: \n{:.4f} s\n' \
    #                              'Result: \n{:.4f} \n\n\n'.format(ex+1, fun_num, n, cpu, iter_time,
    #                                                                                 rand_time, full_time, result)
    #
    #                 result_file.write(result_str)
    #             result_file.close()
    #
    #
    # #  For CRS3 shared memory:
    # for fun_num in func_nums:
    #     for n in ns:
    #         for cpu in cpus:
    #             result_file = open("CRS3SM_{}_{}_{}.txt".format(fun_num, n, cpu), "a")
    #             for ex in range(ex_num):
    #                 iter_time, rand_time, full_time, result = CRS3_multi(cpu_num=cpu,
    #                                                                      FUNCTION_NUMBER=fun_num,
    #                                                                      vec_len=n)
    #                 result_str = 'Experiment: {} \n' \
    #                              'Function number: {} \n' \
    #                              'Vector dimensionality: {}\n' \
    #                              'CPU number: {} \n' \
    #                              'Iteration time: \n{:.4f} s\n' \
    #                              'Randomization time: \n{:.4f} s\n' \
    #                              'Full time: \n{:.4f} s\n' \
    #                              'Result: \n{} \n\n\n'.format(ex + 1, fun_num, n, cpu, iter_time,
    #                                                                               rand_time, full_time, result)
    #
    #                 result_file.write(result_str)
    #             result_file.close()
    #

# For CRS2 local memory:
    for fun_num in func_nums:
        for n in ns:
            for cpu in cpus:
                result_file = open("CRS2LM_{}_{}_{}.txt".format(fun_num, n, cpu), "a")
                for ex in range(ex_num):
                    iter_time, rand_time, full_time, result = CRS2_local(cpu_num=cpu,
                                                                         FUNCTION_NUMBER=fun_num,
                                                                         vec_len=n)
                    result_str = 'Experiment: {} \n' \
                                 'Function number: {} \n' \
                                 'Vector dimensionality: {}\n' \
                                 'CPU number: {} \n' \
                                 'Iteration time: \n{:.4f} s\n' \
                                 'Randomization time: \n{:.4f} s\n' \
                                 'Full time: \n{:.4f} s\n' \
                                 'Result: \n{:.4f} \n\n\n'.format(ex+1, fun_num, n, cpu, iter_time,
                                                                                    rand_time, full_time, result)

                    result_file.write(result_str)
                result_file.close()


# For CRS3 local memory:
    for fun_num in func_nums:
        for n in ns:
            for cpu in cpus:
                result_file = open("CRS3LM_{}_{}_{}.txt".format(fun_num, n, cpu), "a")
                for ex in range(ex_num):
                    iter_time, rand_time, full_time, result = CRS3_local(cpu_num=cpu,
                                                                         FUNCTION_NUMBER=fun_num,
                                                                         vec_len=n)
                    result_str = 'Experiment: {} \n' \
                                 'Function number: {} \n' \
                                 'Vector dimensionality: {}\n' \
                                 'CPU number: {} \n' \
                                 'Iteration time: \n{:.4f} s\n' \
                                 'Randomization time: \n{:.4f} s\n' \
                                 'Full time: \n{:.4f} s\n' \
                                 'Result: \n{:.4f} \n\n\n'.format(ex+1, fun_num, n, cpu, iter_time,
                                                                                    rand_time, full_time, result)

                    result_file.write(result_str)
                result_file.close()
	

