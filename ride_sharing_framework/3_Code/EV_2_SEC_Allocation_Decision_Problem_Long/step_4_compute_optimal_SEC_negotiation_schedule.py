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


# ---------------------------------------------------------
# FUNCTION 01 - compute_optimal_SEC_negotiation_schedule
# ---------------------------------------------------------
def compute_optimal_SEC_negotiation_schedule(input_file_name,
                                             output_folder,
                                             solution_file_name,
                                             time_limit
                                            ):

    # 1. If the output folder already exists, we remove it and re-create it
    if os.path.exists(output_folder):
        os.chmod(path, 0o777)
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # 2. We open the file for reading
    #    Note: Please note here we use the variable 'num_nodes', whereas this is indeed 'num_edges' of the original graph.
    #          Please note here we use the variable 'edges_per_node', whereas this is indeed 'edges_different_constraints' of the original graph.
    #          The reason for doing this is that, after transforming the graph, for it to be edge_centric (instead of node-centric)
    #          we find it easier to follow up with the names 'num_nodes' and 'edges_per_node' of the new obtained graph.
    (num_nodes,
     edges_per_node,
     new_2_old_graph_dict
     ) = misc.parse_in_num_SEC_connections(input_file_name)

    # 3. We solve the problem by applying the desired technique
    best_value = num_nodes
    colours = None
    optimal = 0

    # 4. We try to improve the solution using MIP
    succeed = -1

    # 4.1. We run our algorithm
    (succeed,
     new_best_value,
     new_colours
     ) = mip_models.solve_compute_optimal_SEC_negotiation_schedule(num_nodes,
                                                                   edges_per_node,
                                                                   best_value,
                                                                   time_limit
                                                                  )

    # 4.2. If we found a new solution, we update the result
    if (succeed >= 0):
        best_value = int(new_best_value)
        colours = new_colours
        optimal = succeed

    # 5. We parse the solution out
    #    Note: Please note here we use the variable 'num_nodes', whereas this is indeed 'num_edges' of the original graph.
    #          Please note here we use the variable 'new_2_old_graph_dict', whereas this is indeed 'nodes_per_edge' of the original graph.
    #          The reason for doing this is that, after transforming the graph, for it to be edge_centric (instead of node-centric)
    #          we find it easier to follow up with the names 'num_nodes' and 'new_2_old_graph_dict' of the new obtained graph.
    misc.parse_out_SECs_negotiation_schedule(output_folder + solution_file_name,
                                             num_nodes,
                                             new_2_old_graph_dict,
                                             best_value,
                                             optimal,
                                             colours
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
    input_file_name = "../../1_Instance_Generator/instances/Instance_to_solve/input.in"
    output_folder = "../../4_Solutions/NYC/4_Instance_Optimal_SEC_Negotiation_Schedule/"
    solution_file_name = "optimal_SEC_negotiation_schedule.csv"
    time_limit = 600

    if (len(sys.argv) > 1):
        input_file_name = sys.argv[1]
        output_folder = sys.argv[2]
        solution_file_name = sys.argv[3]
        time_limit = int(sys.argv[4])

    # 2. We call to my_main
    compute_optimal_SEC_negotiation_schedule(input_file_name,
                                             output_folder,
                                             solution_file_name,
                                             time_limit
                                            )
