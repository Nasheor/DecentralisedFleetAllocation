# --------------------------------------------------------
#
# PYTHON PROGRAM DEFINITION
#
# The knowledge a computer has of Python can be specified in 3 levels:
# (1) Prelude knowledge --> The computer has it by default.
# (2) Borrowed knowledge --> The computer gets this knowledge from 3rd party libraries defined by others
#                            (but imported by us in this program).
# (3) Generated knowledge --> The computer gets this knowledge from the new functions defined by us in this program.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer first processes this PYTHON PROGRAM DEFINITION section of the file.
# On it, our computer enhances its Python knowledge from levels (2) and (3) with the imports and new functions
# defined in the program. However, it still does not execute anything.
#
# --------------------------------------------------------


# ------------------------------------------
# IMPORTS
# ------------------------------------------
import misc
import mip_models
#
import sys
import os
import shutil
import codecs


# ---------------------------------------------------
# FUNCTION 01 - compute_optimal_EV_2_SEC_allocation
# ---------------------------------------------------
def compute_optimal_EV_2_SEC_allocation(input_file_name,
                                        output_folder,
                                        solution_file_name,
                                        time_limit
                                       ):

    # 1. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We parse the instance subproblem solutions file
    (num_SECs,
     num_EVs,
     ub_TPs,
     array_values
     ) = misc.parse_in_instance_subproblem_solutions(input_file_name)

    # 3. We try to improve the solution using MIP
    succeed = -1

    # 3.1. We run our algorithm
    (succeed,
     best_value,
     EV_per_SEC
     ) = mip_models.solve_compute_optimal_EV_2_SEC_allocation(ub_TPs,
                                                              num_SECs,
                                                              num_EVs,
                                                              array_values,
                                                              time_limit
                                                             )

    # 3.2. If we found a new solution, we update the result
    if (succeed >= 0):
        misc.parse_out_EV_2_SEC_allocation(output_folder + solution_file_name,
                                           best_value,
                                           EV_per_SEC,
                                           array_values,
                                           num_SECs,
                                           num_EVs
                                          )


# --------------------------------------------------------
#
# PYTHON PROGRAM EXECUTION
#
# Once our computer has finished processing the PYTHON PROGRAM DEFINITION section its knowledge is set.
# Now it is time to apply this knowledge.
#
# When launching in a terminal the command:
# user:~$ python3 this_file.py
# our computer finally processes this PYTHON PROGRAM EXECUTION section, which:
# (i) Specifies the function F to be executed.
# (ii) Define any input parameter such this function F has to be called with.
#
# --------------------------------------------------------
if __name__ == '__main__':
    # 1. We get the input parameters
    # input_file_name = "../../4_Solutions/Metropolis/2_Instance_Subproblem_Solutions/subproblem_solutions.csv"
    # output_folder = "../../4_Solutions/Metropolis/3_Instance_Optimal_EV_2_SEC_Allocation/"
    solution_file_name = "optimal_EV_2_SEC_allocation.csv"
    time_limit = 60

    input_file_name = "../../4_Solutions/NYC/Instance_261_connections/2_Instance_Subproblem_Solutions/subproblem_solutions.csv"
    output_folder = "../../4_Solutions/NYC/3_Instance_Optimal_EV_2_SEC_Allocation/"

    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        output_folder = sys.argv[2]
        solution_file_name = sys.argv[3]
        time_limit = int(sys.argv[4])

    # 2. We call to the function my_main
    compute_optimal_EV_2_SEC_allocation(input_file_name,
                                        output_folder,
                                        solution_file_name,
                                        time_limit
                                       )

