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
import step_2_1_solve_instance
#
import sys
import os
import shutil
import codecs
import time


# ------------------------------------------------------
# FUNCTION 01 - compute_instance_subproblem_solutions
# ------------------------------------------------------
def compute_instance_subproblem_solutions(input_folder,
                                          output_folder,
                                          solution_file_name
                                         ):
    # 1. We start the clock
    start_time = time.time()

    # 2. If the output folder already exists, we remove it and re-create it
    # if os.path.exists(output_folder):
    #     os.chmod(path, 0o777)
    #     shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 3. We open a file called solution.csv for writing
    solution_csv_stream = codecs.open(output_folder + solution_file_name, "w", encoding="utf-8")

    # 4. We collect all the configurations to be analysed
    list_of_folders = os.listdir(input_folder)
    if (".DS_Store") in list_of_folders:
        list_of_folders.remove(".DS_Store")
    list_of_folders.sort()

    # 5. We run the set of instances for each configuration
    for folder in list_of_folders:
        # 5.1. We create the output folder to create the instances
        os.mkdir(output_folder + folder)

        # 5.2. We collect the list of instances to be solved (in sorted order) under the desired configuration
        list_of_files = os.listdir(input_folder + folder)
        if (".DS_Store") in list_of_files:
            list_of_files.remove(".DS_Store")
        list_of_files.sort()

        # 5.3. We traverse the instances
        for file in list_of_files:
            # 5.3.1. We get the name of the input and output files
            input_file_name = input_folder + folder + "/" + file
            output_file_name = output_folder + folder + "/" + file

            # 5.3.2. We solve the instance
            try:
                num_trips_satisfied, total_energy = step_2_1_solve_instance.solve_instance(input_file_name, output_file_name)
            except:
                print(input_file_name + " failed")
                num_trips_satisfied = -1

            # 5.3.3. We write the result to the solution file
            my_str = input_file_name + ";" + str(num_trips_satisfied) + ";"+str(total_energy)+"\n"
            solution_csv_stream.write(my_str)

    # 6. close the solution.csv file
    solution_csv_stream.close()

    # 7. We print the total time
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
    # 1. We get the name of the input and output folder
    input_folder = "../../4_Solutions/NYC/1_Instance_Subproblems/"
    output_folder = '../../4_Solutions/NYC/2_Instance_Subproblem_Solutions/'
    solution_file_name = "subproblem_solutions.csv"

    if (len(sys.argv) > 1):
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        solution_file_name = sys.argv[3]

    # 2. We call to the function my_main
    compute_instance_subproblem_solutions(input_folder,
                                          output_folder,
                                          solution_file_name
                                         )
