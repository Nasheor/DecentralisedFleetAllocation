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
import sys
import time
#
import step_1_generate_and_solve_instance_subproblems
import step_2_compute_optimal_EV_2_SEC_allocation
import step_3_compute_optimal_SEC_negotiation_schedule
import step_4_compute_SEC_negotiation_solution


# ------------------------------------------
# FUNCTION 01 - my_main
# ------------------------------------------
def my_main(input_file_name,
            step_1_folder_1,
            step_1_folder_2,
            step_1_file_name,
            step_2_folder,
            step_2_file_name,
            step_2_mip_time_limit,
            step_3_folder,
            step_3_file_name,
            step_3_mip_time_limit,
            step_4_folder,
            step_4_file_name_1,
            step_4_file_name_2
           ):

    # 0. We start the timer
    start_time = time.time()

    # 1. Step 1 => We generate and solve the instance subproblems
    new_step_start_time = time.time()

    step_1_generate_and_solve_instance_subproblems.generate_and_solve_instance_subproblems(input_file_name,
                                                                                           step_1_folder_1,
                                                                                           step_1_folder_2,
                                                                                           step_1_file_name
                                                                                          )

    new_step_total_time = time.time() - new_step_start_time
    print("Step 1 total time = " + str(new_step_total_time))

    # 2. Step 2 => We compute the optimal EV_2_SEC allocation
    new_step_start_time = time.time()

    step_2_compute_optimal_EV_2_SEC_allocation.compute_optimal_EV_2_SEC_allocation(step_1_folder_2 + step_1_file_name,
                                                                                   step_2_folder,
                                                                                   step_2_file_name,
                                                                                   step_2_mip_time_limit
                                                                                  )

    new_step_total_time = time.time() - new_step_start_time
    print("Step 2 total time = " + str(new_step_total_time))

    # 3. Step 3 => We compute the optimal SEC negotiation schedule
    new_step_start_time = time.time()

    step_3_compute_optimal_SEC_negotiation_schedule.compute_optimal_SEC_negotiation_schedule(input_file_name,
                                                                                             step_3_folder,
                                                                                             step_3_file_name,
                                                                                             step_3_mip_time_limit
                                                                                            )

    new_step_total_time = time.time() - new_step_start_time
    print("Step 3 total time = " + str(new_step_total_time))

    # 4. Step 4 => We perform the negotiation simulation
    new_step_start_time = time.time()

    step_4_compute_SEC_negotiation_solution.compute_negotiation_EV_2_SEC_allocation(step_1_folder_2 + step_1_file_name,
                                                                                    step_3_folder + step_3_file_name,
                                                                                    step_4_folder,
                                                                                    step_4_file_name_1,
                                                                                    step_4_file_name_2,
                                                                                    step_2_mip_time_limit
                                                                                   )

    new_step_total_time = time.time() - new_step_start_time
    print("Step 4 total time = " + str(new_step_total_time))

    # 6. We compute the total time
    total_time = time.time() - start_time
    print("Total time = " + str(total_time))


# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We read the instance content
    # input_file_name = "../../2_Instances/Metropolis/Instance_to_solve/input.in"
    input_file_name = "../../1_Instance_Generator/instances/Instance_to_solve/input.in"
    # step_1_folder_1 = "../../4_Solutions/Metropolis/1_Instance_Subproblems/"
    step_1_folder_1 = "../../4_Solutions/NYC/1_Instance_Subproblems/"
    # step_1_folder_2 = "../../4_Solutions/Metropolis/2_Instance_Subproblem_Solutions/"
    step_1_folder_2 = "../../4_Solutions/NYC/2_Instance_Subproblem_Solutions"
    step_1_file_name = "subproblem_solutions.csv"
    # step_2_folder = "../../4_Solutions/Metropolis/3_Instance_Optimal_EV_2_SEC_Allocation/"
    step_2_folder = "../../4_Solutions/NYC/3_Instance_Optimal_EV_2_SEC_Allocation/"
    step_2_file_name = "optimal_EV_2_SEC_allocation.csv"
    step_2_mip_time_limit = 60
    # step_3_folder = "../../4_Solutions/Metropolis/4_Instance_Optimal_SEC_Negotiation_Schedule/"
    step_3_folder = "../../4_Solutions/NYC/4_Instance_Optimal_SEC_Negotiation_Schedule/"
    step_3_file_name = "optimal_SEC_negotiation_schedule.csv"
    step_3_mip_time_limit = 600
    # step_4_folder = "../../4_Solutions/Metropolis/5_Instance_SEC_Negotiation_EV_2_SEC_Allocation/"
    step_4_folder = "../../4_Solutions/NYC/5_Instance_SEC_Negotiation_EV_2_SEC_Allocation/"
    step_4_file_name_1 = "SEC_negotiation_EV_2_SEC_allocation.csv"
    step_4_file_name_2 = "SEC_negotiation_log.csv"

    # 1.1. If we want to call the program by terminal
    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        step_1_folder_1 = sys.argv[2]
        step_1_folder_2 = sys.argv[3]
        step_1_file_name = sys.argv[4]
        step_2_folder = sys.argv[5]
        step_2_file_name = sys.argv[6]
        step_2_mip_time_limit = int(sys.argv[7])
        step_3_folder = sys.argv[8]
        step_3_file_name = sys.argv[9]
        step_3_mip_time_limit = int(sys.argv[10])
        step_4_folder = sys.argv[11]
        step_4_file_name_1 = sys.argv[12]
        step_4_file_name_2 = sys.argv[13]

    # 2. We call to my_main
    my_main(input_file_name,
            step_1_folder_1,
            step_1_folder_2,
            step_1_file_name,
            step_2_folder,
            step_2_file_name,
            step_2_mip_time_limit,
            step_3_folder,
            step_3_file_name,
            step_3_mip_time_limit,
            step_4_folder,
            step_4_file_name_1,
            step_4_file_name_2
           )

