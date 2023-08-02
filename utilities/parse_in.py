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
# FUNCTION 01 - parse_in
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
def parse_in(input_file_name):
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
    ids = []

    # 3.2.2. We parse the information for each of them
    for _ in range(num_SECs):
        # I. Main info

        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        # info = (SEC_id, x-position, y-position)

        SEC_id = info[0]
        ids.append(SEC_id)
        del info[0]

        SECs[ SEC_id ] = tuple(info)

    Neighbors = {}
    for sec_id in ids:
        Neighbors[sec_id] = []

    num_connections = int(my_input_stream.readline().strip())
    for _ in range(num_connections):
        info = list(map(int, my_input_stream.readline().strip().split(" ")))
        Neighbors[info[0]].append(info[1])
        Neighbors[info[1]].append(info[0])

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
        # info = tuple(map(int, my_input_stream.readline().strip().split(" ")))
        info = tuple(map(int, my_input_stream.readline().strip().split(",")))

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
           Neighbors,
           EVs,
           TPs,
           TDs,
           num_connections
          )

    # 6. We return res
    return res
