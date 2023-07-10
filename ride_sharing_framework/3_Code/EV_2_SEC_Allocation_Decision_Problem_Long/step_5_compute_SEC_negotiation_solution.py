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
import time
import docplex.mp.model


# ------------------------------------------------------------
# FUNCTION 01 - get_initial_EV_2_SEC_allocation
# ------------------------------------------------------------
def get_initial_EV_2_SEC_allocation(num_SECs, num_EVs):
    # 1. We create the output variable
    res = None

    # 2. We get a balanced number of EVs per SEC
    EV_per_SEC = num_EVs // num_SECs
    res = [EV_per_SEC] * num_SECs

    # 3. We add an EV to the first SECs if the division was not an integer
    total_EVs = EV_per_SEC * num_SECs
    index = 0
    while (total_EVs < num_EVs):
        res[index] += 1
        index += 1
        total_EVs += 1

    # 4. We return res
    return res


# ------------------------------------------------------------
# FUNCTION 02 - negotiate_SEC_i_and_SEC_j
# ------------------------------------------------------------
def negotiate_SEC_i_and_SEC_j(SEC_i,
                              SEC_j,
                              num_EVs,
                              solution_per_SEC_and_num_EVs,
                              negotiation_simulation,
                              time_limit
                             ):

    # 1. We get the number of EVs of the two SECs involved
    EV_i = negotiation_simulation[-1][SEC_i - 1]
    EV_j = negotiation_simulation[-1][SEC_j - 1]

    # 2. We get the total number of EVs between both SECs
    sum_EVs = EV_i + EV_j

    # 3. We get the ub of TPs that can be satisfied with sum_EVs (assuming the impossible case in which this sum_EVs are assigned to both SEC_i and SEC_j)
    ub_TP_i = solution_per_SEC_and_num_EVs[((SEC_i - 1) * (num_EVs + 1)) + sum_EVs]
    ub_TP_j = solution_per_SEC_and_num_EVs[((SEC_j - 1) * (num_EVs + 1)) + sum_EVs]

    ub_TPs = ub_TP_i + ub_TP_j

    # 4. We get the array_values
    aux_values_SEC_i = solution_per_SEC_and_num_EVs[((SEC_i - 1) * (num_EVs + 1)):(((SEC_i - 1) * (num_EVs + 1)) + (sum_EVs + 1))]
    aux_values_SEC_j = solution_per_SEC_and_num_EVs[((SEC_j - 1) * (num_EVs + 1)):(((SEC_j - 1) * (num_EVs + 1)) + (sum_EVs + 1))]

    array_values = aux_values_SEC_i + aux_values_SEC_j

    # 5. We solve the negotiation
    (succeed,
     best_value,
     sol_EVs
    ) = mip_models.solve_compute_optimal_EV_2_SEC_allocation(ub_TPs,
                                                             2,
                                                             sum_EVs,
                                                             array_values,
                                                             time_limit
                                                            )

    # 6. We update the results
    negotiation_simulation[-1][SEC_i - 1] = sol_EVs[0]
    negotiation_simulation[-1][SEC_j - 1] = sol_EVs[1]


# ------------------------------------------------------------
# FUNCTION 03 - are_results_the_same
# ------------------------------------------------------------
def are_results_the_same(negotiation_simulation, num_negotiation_steps_per_cycle):
    # 1. We create the output variable
    res = True

    # 2. We get the two lists to compare
    l1 = negotiation_simulation[(-1) * (num_negotiation_steps_per_cycle + 1)]
    l2 = negotiation_simulation[-1]

    # 3. We check if both lists are the exact same
    index = 0
    size = len(l1)

    while ((res == True) and (index < size)):
        if (l1[index] == l2[index]):
            index += 1
        else:
            res = False

    # 4. We return res
    return res


# ------------------------------------------------------------
# FUNCTION 04 - simulate_negotiation
# ------------------------------------------------------------
def simulate_negotiation(num_SECs,
                         num_EVs,
                         solution_per_SEC_and_num_EVs,
                         num_negotiation_steps_per_cycle,
                         negotiation_schedule,
                         time_limit
                        ):

    # 1. We create the output variable
    res = []

    # 2. We append the initial allocation at step 0
    initial_EV_per_SEC = get_initial_EV_2_SEC_allocation(num_SECs, num_EVs)
    res.append( initial_EV_per_SEC )

    # 3. We continue until the negotiation stalls
    is_progressing = True
    while (is_progressing == True):
        # 3.1. We perform all the negotiation steps in the cycle
        for index in range(num_negotiation_steps_per_cycle):
            # 3.1.1. We initialise the results using the ones from the last step
            new_step_results = res[-1][:]
            res.append(new_step_results)

            # 3.1.2. We get the negotiation SECs involved in this step
            step_negotiations = negotiation_schedule[index]
            num_step_negotiations = len(step_negotiations)

            # 3.1.3. We iterate through them
            for index in range(num_step_negotiations // 2):
                # I. We perform the negotiation of the two SECs involved
                negotiate_SEC_i_and_SEC_j(step_negotiations[(index * 2)],
                                          step_negotiations[(index * 2) + 1],
                                          num_EVs,
                                          solution_per_SEC_and_num_EVs,
                                          res,
                                          time_limit
                                         )

        # 3.2. Once all steps of the cycle are done, we check if progress has been made
        is_progressing = not are_results_the_same(res, num_negotiation_steps_per_cycle)

    # 5. We return res
    return res


# ------------------------------------------------------------
# FUNCTION 05 - compute_negotiation_EV_2_SEC_allocation
# ------------------------------------------------------------
def compute_negotiation_EV_2_SEC_allocation(input_file_name_subproblem_solutions,
                                            input_file_name_SEC_negotiation_schedule,
                                            output_folder,
                                            solution_file_SEC_negotiation_EV_2_SEC_allocation,
                                            solution_file_SEC_negotiation_log,
                                            time_limit
                                            ):

    # 1. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_folder):
        os.chmod(path, 0o777)
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We parse the instance subproblem solutions file
    (num_SECs,
     num_EVs,
     ub_TPs,
     solution_per_SEC_and_num_EVs
    ) = misc.parse_in_instance_subproblem_solutions(input_file_name_subproblem_solutions)

    # 3. We parse the SEC negotiation schedule file
    (num_negotiation_steps_per_cycle,
     is_optimal,
     negotiation_schedule
    ) = misc.parse_in_SECs_negotiation_schedule(input_file_name_SEC_negotiation_schedule)

    # 4. We compute the negotiation simulation
    EV_per_SEC_negotiation_simulation = simulate_negotiation(num_SECs,
                                                             num_EVs,
                                                             solution_per_SEC_and_num_EVs,
                                                             num_negotiation_steps_per_cycle,
                                                             negotiation_schedule,
                                                             time_limit
                                                            )

    best_value = sum([solution_per_SEC_and_num_EVs[(index * (num_EVs + 1)) + EV_per_SEC_negotiation_simulation[-1][index]] for index in range(num_SECs)])

    # 5. We parse out the negotiation process
    misc.parse_out_negotiation_process(output_folder + solution_file_SEC_negotiation_log,
                                       solution_per_SEC_and_num_EVs,
                                       num_negotiation_steps_per_cycle,
                                       negotiation_schedule,
                                       EV_per_SEC_negotiation_simulation,
                                       num_SECs,
                                       num_EVs
                                      )

    # 6. We parse out the final solution
    misc.parse_out_EV_2_SEC_allocation(output_folder + solution_file_SEC_negotiation_EV_2_SEC_allocation,
                                       best_value,
                                       EV_per_SEC_negotiation_simulation[-1],
                                       solution_per_SEC_and_num_EVs,
                                       num_SECs,
                                       num_EVs,
                                      )


# ---------------------------------------------------------------
#           PYTHON EXECUTION
# This is the main entry point to the execution of our program.
# It provides a call to the 'main function' defined in our
# Python program, making the Python interpreter to trigger
# its execution.
# ---------------------------------------------------------------
if __name__ == '__main__':
    # 1. We read the instance content
    input_file_name_subproblem_solutions = "../../4_Solutions/NYC/2_Instance_Subproblem_Solutions/subproblem_solutions.csv"
    input_file_name_SEC_negotiation_schedule = "../../4_Solutions/NYC/4_Instance_Optimal_SEC_Negotiation_Schedule/optimal_SEC_negotiation_schedule.csv"
    output_folder = "../../4_Solutions/NYC/5_Instance_SEC_Negotiation_EV_2_SEC_Allocation/"
    solution_file_SEC_negotiation_EV_2_SEC_allocation = "SEC_negotiation_EV_2_SEC_allocation.csv"
    solution_file_SEC_negotiation_log = "SEC_negotiation_log.csv"
    time_limit = 60

    if (len(sys.argv) > 1):
        input_file_name_subproblem_solutions = sys.argv[1]
        input_file_name_SEC_negotiation_schedule = sys.argv[2]
        output_folder = sys.argv[3]
        solution_file_SEC_negotiation_EV_2_SEC_allocation = sys.argv[4]
        solution_file_SEC_negotiation_log = sys.argv[5]
        time_limit = int(sys.argv[6])

    # 2. We call to my_main

    start_time = time.time()

    compute_negotiation_EV_2_SEC_allocation(input_file_name_subproblem_solutions,
                                            input_file_name_SEC_negotiation_schedule,
                                            output_folder,
                                            solution_file_SEC_negotiation_EV_2_SEC_allocation,
                                            solution_file_SEC_negotiation_log,
                                            time_limit
                                           )

    total_time = time.time() - start_time
    print("Total time = " + str(total_time))

