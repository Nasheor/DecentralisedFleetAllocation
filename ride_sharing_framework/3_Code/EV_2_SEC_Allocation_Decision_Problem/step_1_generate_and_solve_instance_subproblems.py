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
import step_1_1_solve_instance
#
import sys
import os
import shutil
import codecs
import time


# ------------------------------------------
# FUNCTION 01 - populate_subproblem_file
# ------------------------------------------
def populate_subproblem_file(output_file_name,
                             city,
                             SECs,
                             EVs,
                             TPs,
                             SEC_index,
                             num_EVs
                            ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We populate the info from the city
    my_str = str(city[0]) + " " + str(city[1]) + " " + str(city[2]) + "\n"
    my_output_stream.write(my_str)

    # 3. We populate the info from the SEC
    my_str = "1\n"
    my_output_stream.write(my_str)

    info = SECs[SEC_index]
    my_str = str(SEC_index) + " " + str(info[0]) + " " + str(info[1]) + "\n"
    my_output_stream.write(my_str)

    # 4. We populate the info from the EVs

    # 4.1. We get an EV as template
    EV_Template = []
    for key in EVs:
        EV_Template = EVs[key]
        break

    # 4.2. We write the line of num_EVs
    my_str = str(num_EVs) + "\n"
    my_output_stream.write(my_str)

    # 4.3. We populate the info of the EVs
    for EV_index in range(num_EVs):
        my_str = str(EV_index + 1) + " " + str(SEC_index) + " " + str(EV_Template[0][1]) + " " + str(EV_Template[0][2]) + " " + str(EV_Template[0][3]) + "\n"
        my_output_stream.write(my_str)
        my_str = "0\n"
        my_output_stream.write(my_str)

    # 5. We populate the info from the TPs

    # 5.1. We filter only the TPs involved in this SEC
    num_TPs = 0
    SEC_specific_TPs = {}

    for TP_index in TPs:
        info = TPs[TP_index]
        if (info[1] == SEC_index):
            num_TPs += 1
            SEC_specific_TPs[TP_index] = TPs[TP_index]

    # 5.2. We write the line of num_TPs
    my_str = str(num_TPs) + "\n"
    my_output_stream.write(my_str)

    # 5.2. We write the info of the specific TPs
    for TP_index in SEC_specific_TPs:
        info = SEC_specific_TPs[TP_index]

        # 5.2.1. We write the first line
        my_str = str(TP_index) + " " + str(info[1]) + " " + str(info[2]) + "\n"
        my_output_stream.write(my_str)

        # 5.2.2. We write the second line
        my_str = str(info[0][0]) + ", " + str(info[0][1]) + ", " + str(info[0][2]) + ", " + \
                 str(info[0][3]) + ", " + str(info[0][4]) + ", " + str(info[0][5]) + ", " + \
                 str(info[0][6]) + ", " + str(info[0][7]) + ", " + str(info[0][8]) + "\n"
        my_output_stream.write(my_str)

    # 6. We close the file
    my_output_stream.close()


# --------------------------------------------------------
# FUNCTION 02 - generate_and_solve_instance_subproblems
# --------------------------------------------------------
def generate_and_solve_instance_subproblems(input_file_name,
                                            output_step_1,
                                            output_step_2,
                                            solution_file_name
                                           ):

    # 1. We start the clock
    start_time = time.time()

    # 2. We parse the instance in
    (city, SECs, EVs, TPs, TDs) = misc.parse_in_original_instance(input_file_name)

    # 3. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_step_1):
        shutil.rmtree(output_step_1)
    os.mkdir(output_step_1)

    # 4. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_step_2):
        shutil.rmtree(output_step_2)
    os.mkdir(output_step_2)

    # 5. We open a file called solution.csv for writing
    solution_csv_stream = codecs.open(output_step_2 + solution_file_name, "w", encoding="utf-8")

    # 6. We iterate the creation and solving of the subproblems
    for SEC_index in SECs:
        # 6.1. We create the folders for the SEC (instance and solution)
        my_SEC_name = "SEC_" + str(SEC_index)
        os.mkdir(output_step_1 + my_SEC_name)
        os.mkdir(output_step_2 + my_SEC_name)

        # 6.2. We create a dummy number of trips satisfied
        last_instance_trips_satisfied = -1
        continue_solving = True

        # 6.3. We iterate in the number of EVs being used
        for EV_index in EVs:
            # 6.3.1. We get the name of the instance and solution files
            instance_file_name = output_step_1 + my_SEC_name + "/" + my_SEC_name + "_num_EVs_" + str(EV_index) + ".txt"
            solution_file_name = output_step_1 + my_SEC_name + "/" + my_SEC_name + "_num_EVs_" + str(EV_index) + ".txt"

            # 6.3.2. If continue_solving is True, we solve the instance
            if (continue_solving == True):
                # I. We create the instance subproblem file
                populate_subproblem_file(instance_file_name,
                                         city,
                                         SECs,
                                         EVs,
                                         TPs,
                                         SEC_index,
                                         EV_index
                                        )

                # II. We solve the instance subproblem
                try:
                    num_trips_satisfied, total_energy = step_1_1_solve_instance.solve_instance(instance_file_name, solution_file_name)
                except:
                    print(input_file_name + " failed")
                    num_trips_satisfied = -1

                # III. If the num_trips_satisfied does not improve the trips of the previous instance, we stop generating and solving the remaining subproblems for this SEC
                if (num_trips_satisfied <= last_instance_trips_satisfied):
                    continue_solving = False

                # IV. We update the last_instance_trips_satisfied to the solution of the subproblem
                last_instance_trips_satisfied = num_trips_satisfied

            # 6.3.3. We write the result to the solution file
            my_str = instance_file_name + ";" + str(last_instance_trips_satisfied) + ";"+str(total_energy)+"\n"
            solution_csv_stream.write(my_str)

    # 7. close the solution.csv file
    solution_csv_stream.close()

    # 8. We print the total time
    total_time = time.time() - start_time
    print("Total time = " + str(total_time))


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
    # input_file_name = "../../2_Instances/Metropolis/Instance_to_solve/input.in"
    # output_step_1 = "../../4_Solutions/Metropolis/1_Instance_Subproblems/"
    # output_step_2 = "../../4_Solutions/Metropolis/2_Instance_Subproblem_Solutions/"
    solution_file_name = "subproblem_solutions.csv"

    # NYC Paths
    input_file_name = "../../1_Instance_Generator/instances/Instance_to_solve/input.in"
    output_step_1 = "../../4_Solutions/NYC/Instance_261_connections/1_Instance_Subproblems/"
    output_step_2 = "../../4_Solutions/NYC/Instance_261_connections/2_Instance_Subproblem_Solutions/"

    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        output_step_1 = sys.argv[2]
        output_step_2 = sys.argv[3]
        solution_file_name = sys.argv[4]

    # 2. We call to the function my_main
    generate_and_solve_instance_subproblems(input_file_name,
                                            output_step_1,
                                            output_step_2,
                                            solution_file_name
                                           )

