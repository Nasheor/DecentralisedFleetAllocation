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
import codecs


# ------------------------------------------
# FUNCTION 01 - parse_in_original_instance
# ------------------------------------------
# Description:
# We read the instance_input from a file
# ----------------------------------------------------
# Input Parameters:
# (1) input_file_name. => The name of the file to read our instance from.
# ----------------------------------------------------
# Output Parameters:
# (1) instance_input_object. => The 'instance_info object', represented as
# instance_info[0] -> city
# instance_info[1] -> SECs
# instance_info[2] -> EVs
# instance_info[3] -> TPs
# ----------------------------------------------------
def parse_in_original_instance(input_file_name):
    #  1. We create the output variable
    res = ()

    # 1.1. We output the city info and the simulation time horizon
    city = ()

    # 1.2. We output the SECs information
    SECs = {}

    # 1.3. We output the EVs information
    EVs = {}

    # 1.4. We output the trip petitions
    TPs = {}

    # 1.5. We output the trip distances
    TDs = {}

    #  2. We open the file for reading
    my_input_stream = codecs.open(input_file_name, "r", encoding='utf-8')

    # 3. We parse the content

    # 3.1. We parse the simulation information block
           # (city_max_x_location, city_max_y_location, simulation_time_horizon)
    city = tuple(map(int, my_input_stream.readline().strip().split(" ")))

    # 3.2. We parse the SEC information block
    SECs = {}

    # 3.2.1. We get the number of SECs
    num_SECs = int(my_input_stream.readline().strip())

    # 3.2.2. We parse the information for each of them
    for _ in range(num_SECs):
        # I. Main info

        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        # info = (SEC_id, x-position, y-position)

        SEC_id = info[0]
        del info[0]

        SECs[ SEC_id ] = tuple(info)

    # 3.2.3. We get the number of connections among SECs (for exchanging EVs)
    num_SEC_connections = int(my_input_stream.readline().strip())

    # 3.2.4. For the moment we just consume the line, as this is irrelevant for solving each instance subproblem.
    for _ in range(num_SEC_connections+1):
        my_input_stream.readline()

    # 3.3. We parse the EV information block
    EVs = {}

    # 3.3.1. We get the number of EVs
    num_EVs = int(my_input_stream.readline().strip())

    # 3.3.2. We parse the information for each of them
    for iteration in range(num_EVs):
        # I. Main info

        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        # info = (EV_id, SEC_id, EV_release_time, EV_energy, EV_max_passengers)

        EV_id = info[0]
        del info[0]

        # II. Schedule
        schedule = []

        # II.1. We get the number of movements of the EV schedule
        num_movs = int(my_input_stream.readline().strip())

        # II.2. If the schedule was hardcoded (debug mode), we set it to these movements
        if (num_movs > 0):
            for _ in range(num_movs):
                mov_info = tuple(map(int, my_input_stream.readline().strip().split(", ")))
                schedule.append(mov_info)
        # II.3. If the schedule was empty (normal mode), we initialise it to the resting mode
        else:
            # II.3.1. We enter the first movement
            EV_release_time = info[1]
            end_of_resting_time = city[2] - 2
            mov_duration = end_of_resting_time - EV_release_time
            assert (mov_duration >= 0)
            x_coord = SECs[ info[0] ][0]
            y_coord = SECs[info[0]][1]
            EV_energy = info[2]

            mov_info = (EV_release_time, end_of_resting_time, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, mov_duration, 0)
            schedule.append(mov_info)

            # II.3.2. We enter the second movement
            mov_info = (end_of_resting_time, end_of_resting_time + 1, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, 0, 0)
            schedule.append(mov_info)

            # II.3.3. We enter the third movement
            mov_info = (end_of_resting_time + 1, end_of_resting_time + 2, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, 0, 0)
            schedule.append(mov_info)

        # III. We enter the EV in the dictionary
        EVs[ EV_id ] = [ tuple(info), schedule ]

    # 3.4. We parse the TPs information
    TPs = {}

    # 3.4.1. We get the number of TPs
    num_TPs = int(my_input_stream.readline().strip())

    # 3.4.2. We parse the information for each of them
    for _ in range(num_TPs):
        # I. Main info
        (tp_id, SEC_id, EV_id) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # II. Rest of the trip info
        info = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # III. We enter the tp in the dictionary
        TPs[ tp_id ] = [ info, SEC_id, EV_id ]

    # 4. We close the file
    my_input_stream.close()

    # 5. We compute the trip distances
    for tp_id in TPs:
        info = TPs[tp_id][0]
        value = abs(info[3] - info[1]) + abs(info[4] - info[2])
        TDs[tp_id] = value

    # 5. We assign and return res
    res = (city,
           SECs,
           EVs,
           TPs,
           TDs
          )

    # 6. We return res
    return res


# --------------------------------------------
# FUNCTION 02 - parse_in_subproblem_instance
# --------------------------------------------
# Description:
# We read the instance_input from a file
# ----------------------------------------------------
# Input Parameters:
# (1) input_file_name. => The name of the file to read our instance from.
# ----------------------------------------------------
# Output Parameters:
# (1) instance_input_object. => The 'instance_info object', represented as
# instance_info[0] -> city
# instance_info[1] -> SECs
# instance_info[2] -> EVs
# instance_info[3] -> TPs
# ----------------------------------------------------
def parse_in_subproblem_instance(input_file_name):
    #  1. We create the output variable
    res = ()

    # 1.1. We output the city info and the simulation time horizon
    city = ()

    # 1.2. We output the SECs information
    SECs = {}

    # 1.3. We output the EVs information
    EVs = {}

    # 1.4. We output the trip petitions
    TPs = {}

    # 1.5. We output the trip distances
    TDs = {}

    #  2. We open the file for reading
    my_input_stream = codecs.open(input_file_name, "r", encoding='utf-8')

    # 3. We parse the content

    # 3.1. We parse the simulation information block
           # (city_max_x_location, city_max_y_location, simulation_time_horizon)
    city = tuple(map(int, my_input_stream.readline().strip().split(" ")))

    # 3.2. We parse the SEC information block
    SECs = {}

    # 3.2.1. We get the number of SECs
    num_SECs = int(my_input_stream.readline().strip())

    # 3.2.2. We parse the information for each of them
    for _ in range(num_SECs):
        # I. Main info

        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        # info = (SEC_id, x-position, y-position)

        SEC_id = info[0]
        del info[0]

        SECs[ SEC_id ] = tuple(info)

    # 3.3. We parse the EV information block
    EVs = {}

    # 3.3.1. We get the number of EVs
    num_EVs = int(my_input_stream.readline().strip())

    # 3.3.2. We parse the information for each of them
    for iteration in range(num_EVs):
        # I. Main info

        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        # info = (EV_id, SEC_id, EV_release_time, EV_energy, EV_max_passengers)

        EV_id = info[0]
        del info[0]

        # II. Schedule
        schedule = []

        # II.1. We get the number of movements of the EV schedule
        num_movs = int(my_input_stream.readline().strip())

        # II.2. If the schedule was hardcoded (debug mode), we set it to these movements
        if (num_movs > 0):
            for _ in range(num_movs):
                mov_info = tuple(map(int, my_input_stream.readline().strip().split(", ")))
                schedule.append(mov_info)
        # II.3. If the schedule was empty (normal mode), we initialise it to the resting mode
        else:
            # II.3.1. We enter the first movement
            EV_release_time = info[1]
            end_of_resting_time = city[2] - 2
            mov_duration = end_of_resting_time - EV_release_time
            assert (mov_duration >= 0)
            x_coord = SECs[ info[0] ][0]
            y_coord = SECs[info[0]][1]
            EV_energy = info[2]

            mov_info = (EV_release_time, end_of_resting_time, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, mov_duration, 0)
            schedule.append(mov_info)

            # II.3.2. We enter the second movement
            mov_info = (end_of_resting_time, end_of_resting_time + 1, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, 0, 0)
            schedule.append(mov_info)

            # II.3.3. We enter the third movement
            mov_info = (end_of_resting_time + 1, end_of_resting_time + 2, x_coord, y_coord, x_coord, y_coord, 0, 0, EV_energy, EV_energy, 0, 0, 0)
            schedule.append(mov_info)

        # III. We enter the EV in the dictionary
        EVs[ EV_id ] = [ tuple(info), schedule ]

    # 3.4. We parse the TPs information
    TPs = {}

    # 3.4.1. We get the number of TPs
    num_TPs = int(my_input_stream.readline().strip())

    # 3.4.2. We parse the information for each of them
    for _ in range(num_TPs):
        # I. Main info
        (tp_id, SEC_id, EV_id) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # II. Rest of the trip info
        info = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # III. We enter the tp in the dictionary
        TPs[ tp_id ] = [ info, SEC_id, EV_id ]

    # 4. We close the file
    my_input_stream.close()

    # 5. We compute the trip distances
    for tp_id in TPs:
        info = TPs[tp_id][0]
        value = abs(info[3] - info[1]) + abs(info[4] - info[2])
        TDs[tp_id] = value

    # 5. We assign and return res
    res = (city,
           SECs,
           EVs,
           TPs,
           TDs
          )

    # 6. We return res
    return res


# ----------------------------------------------
# FUNCTION 03 - parse_out_subproblem_instance
# ----------------------------------------------
# Description:
# We write the instance_solution to a file
# ----------------------------------------------------
# Input Parameters:
# (1) output_file_name. => The name of the file to write our solution to.
# (2) num_trips_satisfied. => The number of trips satisfied.
# (3) EVs. => The info with the schedule of each EV.
# (4) TPs. => The info regarding each TP.
# ----------------------------------------------------
# Output Parameters:
# ----------------------------------------------------
def parse_out_subproblem_instance(output_file_name,
                                  num_trips_satisfied,
                                  EVs,
                                  TPs,
                                  TDs
                                 ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We get the ids of the TPs and EVs
    TP_IDs = sorted(TPs.keys())
    EV_IDs = sorted(EVs.keys())

    # 3. We compute the percentage of trips satisfied
    num_trips = len(TP_IDs)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)
    my_str = "TPs satisfied = " + str(num_trips_satisfied) + "; Total TPs = " + str(num_trips) + "; Percentage Satisfied + " + str(round(num_trips_satisfied / num_trips , 3) * 100) + "%\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    # 4. We compute the info per EV
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "EVs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    EV_D = {}
    EV_total_energy = 0

    for ev_id in EV_IDs:
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "EV" + str(ev_id) + "\n"
        my_output_stream.write(my_str)

        # 4.1. We compute the overall statistics
        TP_served_by_EV = {}
        num_TPs_served = 0
        my_EV_schedule = EVs[ ev_id ][1]
        total_energy = my_EV_schedule[0][8] - my_EV_schedule[-1][9]
        EV_total_energy += total_energy

        for item in my_EV_schedule:
            if ((item[10] != 0) and (item[10] != 1000000000)):
                if (abs(item[10]) not in TP_served_by_EV):
                    TP_served_by_EV[ abs(item[10]) ] = True
                    num_TPs_served += 1

        EV_D[ev_id] = total_energy

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)
        my_str = "Num TPs served = " + str(num_TPs_served) + "\n"
        my_output_stream.write(my_str)
        my_str = "TPs served = " + " ".join([ str(x) for x in sorted(TP_served_by_EV.keys()) ]) + "\n"
        my_output_stream.write(my_str)
        my_str = "Total energy used = " + str(total_energy) + "\n"
        my_output_stream.write(my_str)
        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

        # 4.2. We print the schedule
        my_str = "Schedule:\n"
        my_output_stream.write(my_str)
        for item in my_EV_schedule:
            my_str = " ".join([ str(x) for x in item ]) + "\n"
            my_output_stream.write(my_str)

        my_str = "--------------------------------------\n"
        my_output_stream.write(my_str)

    # 5. We compute the info per TP
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "TPs" + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    TP_total_energy = 0
    TP_not_covered_total_energy = 0

    for tp_id in TP_IDs:
        my_str = "\n----------------------\n"
        my_output_stream.write(my_str)
        allocated_to = TPs[tp_id][2]
        if (allocated_to == -1):
            my_str = "TP" + str(tp_id) + " not allocated\n"
            TP_not_covered_total_energy += TDs[tp_id]
        else:
            my_str = "TP" + str(tp_id) + " allocated to " + str(allocated_to) + "\n"
        TP_total_energy += TDs[tp_id]
        my_output_stream.write(my_str)
        my_str = "----------------------\n"
        my_output_stream.write(my_str)

    # 6. We compute the overall Ride-sharing vs. Individual num_vehicles and distance info
    my_str = "\n-------------------------------------------------------------------------\n\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing vs Individual Mode - Num Vehicles and Distance Comparisson " + "\n\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    num_EV = len(EVs)
    individuals_not_covered = (num_trips - num_trips_satisfied)
    vehicles_diff = num_EV + individuals_not_covered

    my_str = "Individual Mode = " + str(num_trips) + " vehicles.\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing Mode = " + str(vehicles_diff) + " vehicles. The " + str(num_EV) + " ride-sharing vehicles + " + str(individuals_not_covered) + " vehicles of the individuals not served by the ride-sharing service.\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    individual_mode_distance = TP_total_energy
    EV_total_distance = 0
    for ev_id in EV_D:
        EV_total_distance += EV_D[ev_id]
    EV_mode_total_distance = EV_total_distance + TP_not_covered_total_energy

    my_str = "Individual Mode = " + str(individual_mode_distance) + " distance.\n"
    my_output_stream.write(my_str)
    my_str = "Ride-sharing Mode = " + str(EV_mode_total_distance) + " distance. " + str(EV_total_distance) + " from the EV fleet + " + str(TP_not_covered_total_energy) + " from the distance of the trips not covered individuals had to do with their own vehicle.\n"
    my_output_stream.write(my_str)
    my_str = "-------------------------------------------------------------------------\n"
    my_output_stream.write(my_str)

    # 7. We close the file
    my_output_stream.close()
    return EV_total_energy


# -----------------------------------------------
# FUNCTION 04 - get_num_SECs_num_EVs_and_ub_TPs
# -----------------------------------------------
def get_num_SECs_num_EVs_and_ub_TPs(input_instance):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the num_SECs
    num_SECs = 0

    # 1.2. We output the num_EVs
    num_EVs = 0

    # 1.3. We output the ub_TPs
    ub_TPs = 0

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_instance, "r", encoding="utf-8")

    # 3. We keep track of the current SEC_val
    current_SEC_val = -1
    current_best_val = 0

    # 3. We traverse the file
    for line in my_input_stream:
        # 3.1. We get the info from the line
        content = (line.strip().split("/")[-1]).split("_num_EVs_")
        SEC_val = int(content[0].split("_")[1])
        EV_val = int(content[1].split(".")[0])
        new_TP_val = int(content[1].split(";")[1])

        if (SEC_val == 10):
            x = 2

        # 3.2. If the new SEC_val is different from current_SEC_val
        if (SEC_val != current_SEC_val):
            # 3.2.1. We update current_SEC_val
            current_SEC_val = SEC_val

            # 3.2.2. We update ub_TPs
            ub_TPs += current_best_val

            # 3.2.2. We re-start current_best_val
            current_best_val = 0

        # 3.3. If the number of TPs improves the best one, we update it
        if (new_TP_val > current_best_val):
            current_best_val = new_TP_val

        # 3.4. We update num_SECs and num_EVs
        if (SEC_val > num_SECs):
            num_SECs = SEC_val
        if (EV_val > num_EVs):
            num_EVs = EV_val

    # 4. We close the file
    my_input_stream.close()

    # 5. We assign res
    res = (num_SECs,
           num_EVs,
           ub_TPs
          )

    # 6. We return res
    return res


# ------------------------------------------
# FUNCTION 05 - get_array_values
# ------------------------------------------
def get_array_values(input_instance,
                     num_SECs,
                     num_EVs
                    ):

    # 1. We create the output variable
    res = [0] * (num_SECs * (num_EVs + 1))

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_instance, "r", encoding="utf-8")

    # 3. We traverse the file
    for line in my_input_stream:
        # 3.1. We get the info from the line
        content = (line.strip().split("/")[-1]).split("_num_EVs_")
        SEC_val = int(content[0].split("_")[1])
        EV_val = int(content[1].split(".")[0])
        num_TPs_satisfied = int(content[1].split(";")[1])

        # 3.2. We populate the index of res
        res[ ((SEC_val - 1) * (num_EVs + 1)) + EV_val ] = num_TPs_satisfied

    # 4. We close the file
    my_input_stream.close()

    # 5. We return res
    return res


# ---------------------------------------------------------
# FUNCTION 06 - parse_in_instance_subproblem_solutions
# ---------------------------------------------------------
def parse_in_instance_subproblem_solutions(input_instance):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the num_SECs
    num_SECs = 0

    # 1.2. We output the num_EVs
    num_EVs = 0

    # 1.3. We output the ub_TPs
    ub_TPs = 0

    # 1.4. We output the array of values
    array_values = None

    # 2. We read the file for getting the number of SECs and EVs
    (num_SECs,
     num_EVs,
     ub_TPs
    ) = get_num_SECs_num_EVs_and_ub_TPs(input_instance)

    # 3. We get the array of values
    array_values = get_array_values(input_instance,
                                    num_SECs,
                                    num_EVs
                                   )

    # 4. We assign res
    res = (num_SECs,
           num_EVs,
           ub_TPs,
           array_values
          )

    # 5. We return res
    return res


# -----------------------------------------------------
# FUNCTION 07 - parse_out_EV_2_SEC_allocation
# -----------------------------------------------------
def parse_out_EV_2_SEC_allocation(output_file,
                                  best_value,
                                  EV_per_SEC,
                                  array_values,
                                  num_SECs,
                                  num_EVs
                                 ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file, "w", encoding="utf-8")

    # 2. We write the optimal number of trips
    my_str = "TotalSECs_" + str(num_SECs) + ";TotalEVs_" + str(num_EVs) + ";TotalTPs_" + str(best_value) + "\n"
    my_output_stream.write(my_str)

    # 3. We traverse the SECs
    for SEC_val in range(num_SECs):
        # 3.1. We write the number of EVs allocated and the number of TPs satisfied
        my_str = "SEC_" + str(SEC_val + 1) + ";EVs_" + str(EV_per_SEC[SEC_val]) + ";TPs_" + str(array_values[ (SEC_val * (num_EVs + 1)) + EV_per_SEC[SEC_val] ]) + "\n"
        my_output_stream.write(my_str)

    # 4. We close the file
    my_output_stream.close()


# --------------------------------------------------
# FUNCTION 08 - parse_in_num_SEC_connections
# --------------------------------------------------
def parse_in_num_SEC_connections(input_file_name):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the number of edges
    num_edges = 0

    # 1.2. We output the different constraints on edges
    edges_different_constraints = {}

    # 1.3. We output the connections per edge
    nodes_per_edge = {}

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_file_name, "r", encoding="utf-8")

    # 3. We parse the preliminary content

    # 3.1. We consume the line of the simulation information block
    my_input_stream.readline()

    # 3.2. We parse the SEC information block
    SECs = {}

    # 3.2.1. We get the number of SECs
    num_SECs = int(my_input_stream.readline().strip())

    # 3.2.2. We consume the line with the information for each of them
    for _ in range(num_SECs):
        my_input_stream.readline()

    # 4. We create a dict to store the edge connections per node
    edges_per_node = {}

    # 5. We read the line with the num_SEC_connections info
    num_edges = int(my_input_stream.readline().strip())

    # 6. We read the lines for each specific souce_SEC target_SEC connection
    for index in range(num_edges):
        # 6.1. We parse the edge
        (source_node, target_node) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

        # 6.2. We search for new nodes appearing in the line
        for node_name in [source_node, target_node]:
            # 6.2.1. If the node has not appeared before, we create its associated list
            if node_name not in edges_per_node:
                edges_per_node[node_name] = []

        # 6.3. We populate the nodes, to say both are involved in this edge
        edges_per_node[source_node].append(index)
        edges_per_node[target_node].append(index)

        # 6.4. We populate the edge too, to say it involves these two nodes
        nodes_per_edge[index] = sorted([source_node, target_node])

        # 6.5. We enter the edge in edge_differences
        edges_different_constraints[index] = {}

    # 7. We make the info to be a tuple (num_neighbours, neighbours_list)
    for edge in edges_per_node:
        # 7.1. We get the list of edges for which different constraints are to be imposed
        diff_list = edges_per_node[edge]

        # 7.2. We incorporate this list into edge_different
        size = len(diff_list)
        for i in range(size - 1):
            for j in range(i + 1, size):
                edges_different_constraints[diff_list[i]][diff_list[j]] = True
                edges_different_constraints[diff_list[j]][diff_list[i]] = True

    # 8. We adapt the format of edge_different_constraints
    for edge in edges_different_constraints:
        # 8.1. We get the list of edges it is different to, in sorted order
        keys = sorted(list(edges_different_constraints[edge].keys()))

        # 8.2. We get the size of such list
        size = len(keys)

        # 8.3. We enter this as the final info for edges_different_constraints
        edges_different_constraints[edge] = (size, keys)

    # 9. We close the file
    my_input_stream.close()

    # 10. We assign res
    res = (num_edges,
           edges_different_constraints,
           nodes_per_edge
           )

    # 11. We return res
    return res


# -----------------------------------------------------
# FUNCTION 09 - parse_out_SECs_negotiation_schedule
# -----------------------------------------------------
def parse_out_SECs_negotiation_schedule(output_file_name,
                                        num_edges,
                                        nodes_per_edge,
                                        best_value,
                                        optimal,
                                        colour_per_edge
                                        ):
    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file_name, "w", encoding="utf-8")

    # 2. We write the first line
    my_str = str(best_value) + " " + str(optimal) + "\n"
    my_output_stream.write(my_str)

    # 3. We use an auxiliary structure to print the edges in chronological order of the negotiation
    pair_colour_edge_index = [(colour_per_edge[index], index) for index in range(num_edges)]
    pair_colour_edge_index.sort()

    # 3. We write the info for all edges
    for index in range(num_edges):
        # 3.1. We get the item to look for
        edge_index = pair_colour_edge_index[index][1]

        # 3.2. We get the nodes from the edge
        (source_node, target_node) = tuple(nodes_per_edge[edge_index])

        # 3.3. We get the colour of the edge
        colour = colour_per_edge[edge_index]

        # 3.4. We write the line: "Schedule_step SEC_i SEC_j"
        my_str = str(colour) + " " + str(source_node) + " " + str(target_node) + "\n"
        my_output_stream.write(my_str)

    # 5. We close the file
    my_output_stream.close()


# -----------------------------------------------------
# FUNCTION 10 - parse_in_SECs_negotiation_schedule
# -----------------------------------------------------
def parse_in_SECs_negotiation_schedule(input_file_name):
    # 1. We create the output variable
    res = ()

    # 1.1. We output the number of steps
    num_steps = 0

    # 1.2. We output whether the solution is optimal or not
    is_optimal = False

    # 1.3. We output a dictionary with negotiations per step
    negotiations = {}

    # 2. We open the file for reading
    my_input_stream = codecs.open(input_file_name, "r", encoding="utf-8")

    # 3. We read the first line
    (num_steps, is_optimal) = tuple(map(int, my_input_stream.readline().strip().split(" ")))

    # 4. We read the rest of the file
    for line in my_input_stream:
        # 4.1. We get the info of the line
        (step_id, source_SEC_id, target_SEC_id) = tuple(map(int, line.strip().split(" ")))

        # 4.2. If the step_id is not in the dictionary, we enter it
        if (step_id not in negotiations):
            negotiations[step_id] = []

        # 4.3. We add the pair to the list
        negotiations[step_id].append(source_SEC_id)
        negotiations[step_id].append(target_SEC_id)

    # 5. We close the file
    my_input_stream.close()

    # 6. We assign res
    res = (num_steps,
           is_optimal,
           negotiations
          )

    # 7. We return res
    return res


# -----------------------------------------------------
# FUNCTION 11 - parse_out_negotiation_process
# -----------------------------------------------------
def parse_out_negotiation_process(output_file,
                                  solution_per_SEC_and_num_EVs,
                                  num_negotiation_steps_per_cycle,
                                  negotiation_schedule,
                                  EV_per_SEC_negotiation_simulation,
                                  num_SECs,
                                  num_EVs
                                  ):

    # 1. We open the file for writing
    my_output_stream = codecs.open(output_file, "w", encoding="utf-8")

    # 2. We print the overall solution for the initial step
    total_TPs = sum([solution_per_SEC_and_num_EVs[(index * (num_EVs + 1)) + EV_per_SEC_negotiation_simulation[0][index]] for index in range(num_SECs)])
    my_str = "-----------\nStep_0;Total_TPs_" + str(total_TPs) + "\n"
    my_output_stream.write(my_str)

    # 3. We write the negotiations step by step
    num_steps = len(EV_per_SEC_negotiation_simulation)

    for step in range(num_steps - 1):
        # 3.1. We get the SECs involved in negotiations at this step
        step_negotiations = negotiation_schedule[(step % num_negotiation_steps_per_cycle)]
        num_step_negotiations = len(step_negotiations)

        # 3.2. We iterate through them
        for index in range(num_step_negotiations // 2):
            # 3.2.1. We get the two SECs involved in the negotiation
            SEC_i = step_negotiations[(index * 2)]
            SEC_j = step_negotiations[(index * 2) + 1]

            # 3.2.2. We see if there was a trade among them
            if (EV_per_SEC_negotiation_simulation[step][SEC_i] != EV_per_SEC_negotiation_simulation[step + 1][SEC_i]):
                # I. We get the info
                old_EV_i = EV_per_SEC_negotiation_simulation[step][SEC_i - 1]
                old_EV_j = EV_per_SEC_negotiation_simulation[step][SEC_j - 1]

                old_TP_i = solution_per_SEC_and_num_EVs[((SEC_i - 1) * (num_EVs + 1)) + old_EV_i]
                old_TP_j = solution_per_SEC_and_num_EVs[((SEC_j - 1) * (num_EVs + 1)) + old_EV_j]

                old_sum_EVs = old_EV_i + old_EV_j
                old_sum_TPs = old_TP_i + old_TP_j

                new_EV_i = EV_per_SEC_negotiation_simulation[step + 1][SEC_i - 1]
                new_EV_j = EV_per_SEC_negotiation_simulation[step + 1][SEC_j - 1]

                new_TP_i = solution_per_SEC_and_num_EVs[((SEC_i - 1) * (num_EVs + 1)) + new_EV_i]
                new_TP_j = solution_per_SEC_and_num_EVs[((SEC_j - 1) * (num_EVs + 1)) + new_EV_j]

                new_sum_EVs = new_EV_i + new_EV_j
                new_sum_TPs = new_TP_i + new_TP_j

                # II. We format it into a String
                my_str = "step_" + str(step + 1) + ";" +\
                         "SEC_i_" + str(SEC_i) + ";" + \
                         "SEC_j_" + str(SEC_j) + ";" + \
                         "old_EV_i_" + str(old_EV_i) + ";" +\
                         "old_EV_j_" + str(old_EV_j) + ";" +\
                         "old_TP_i_" + str(old_TP_i) + ";" +\
                         "old_TP_j_" + str(old_TP_j) + ";" +\
                         "old_sum_EVs_" + str(old_sum_EVs) + ";" +\
                         "old_sum_TPs_" + str(old_sum_TPs) + ";" +\
                         "new_EV_i_" + str(new_EV_i) + ";" +\
                         "new_EV_j_" + str(new_EV_j) + ";" +\
                         "new_TP_i_" + str(new_TP_i) + ";" +\
                         "new_TP_j_" + str(new_TP_j) + ";" +\
                         "new_sum_EVs_" + str(new_sum_EVs) + ";" +\
                         "new_sum_TPs_" + str(new_sum_TPs) + ";" +\
                         "\n"

                # III. We write the String
                my_output_stream.write(my_str)

        # 3.3. We print the overall solution in the step
        total_TPs = sum([ solution_per_SEC_and_num_EVs[(index * (num_EVs + 1)) + EV_per_SEC_negotiation_simulation[step + 1][index] ] for index in range(num_SECs) ])
        my_str = "-----------\nStep_" + str(step + 1) + ";Total_TPs_" + str(total_TPs) + "\n"
        my_output_stream.write(my_str)

    # 4. We close the file
    my_output_stream.close()

