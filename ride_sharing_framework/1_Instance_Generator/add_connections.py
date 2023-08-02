import compute_neighbors
import os
import shutil
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        # Read simulation information
        city_max_x_location, city_max_y_location, simulation_time_horizon = map(int, file.readline().split())

        # Read SECs information
        num_secs = int(file.readline())
        sec_info = {}
        for _ in range(num_secs):
            sec_id, sec_x_location, sec_y_location = map(int, file.readline().split())
            sec_info[sec_id] = (sec_x_location, sec_y_location)

        # Read SECs Neighbor information
        total_num_connections = int(file.readline())
        sec_neighbors = {}
        for _ in range(total_num_connections):
            sec_id, neighbor_sec_id = map(int, file.readline().split())
            sec_neighbors.setdefault(sec_id, []).append(neighbor_sec_id)

        # Read EVs information
        num_evs = int(file.readline())
        ev_info = {}
        for _ in range(num_evs):
            ev_id, sec_id, ev_release_time, ev_battery_energy, ev_max_passengers = map(int, file.readline().split())
            schedule_num_movs = int(file.readline())
            schedule = []
            for _ in range(schedule_num_movs):
                movement_info = tuple(map(int, file.readline().split()))
                schedule.append(movement_info)
            ev_info[ev_id] = {
                'sec_id': sec_id,
                'ev_release_time': ev_release_time,
                'ev_battery_energy': ev_battery_energy,
                'ev_max_passengers': ev_max_passengers,
                'schedule': schedule
            }

        # Read TPs information
        num_tps = int(file.readline())
        tp_info = {}
        for _ in range(num_tps):
            tp_id, sec_id, ev_id = map(int, file.readline().split())
            trip_info = tuple(map(int, file.readline().split(",")))
            tp_info[tp_id] = {'sec_id': sec_id, 'ev_id': ev_id, 'trip_info': trip_info}

    return (city_max_x_location, city_max_y_location,simulation_time_horizon, num_secs, sec_info,total_num_connections,
            sec_neighbors,num_evs, ev_info, num_tps, tp_info)

def write_output_file(file_path, city_max_x_location, city_max_y_location, simulation_time_horizon, sec_info, sec_neighbors, ev_info, tp_info):
    with open(file_path, 'w') as file:
        # Write simulation information
        file.write(f"{city_max_x_location} {city_max_y_location} {simulation_time_horizon}\n")

        # Write SECs information
        num_secs = len(sec_info)
        file.write(f"{num_secs}\n")
        for sec_id, (sec_x_location, sec_y_location) in sec_info.items():
            file.write(f"{sec_id} {sec_x_location} {sec_y_location}\n")

        # Write SECs Neighbor information
        total_num_connections = sum(len(neighbor_list) for neighbor_list in sec_neighbors.values()) // 2
        file.write(f"{total_num_connections}\n")
        for sec_id, neighbor_list in sec_neighbors.items():
            for neighbor_id in neighbor_list:
                if neighbor_id > sec_id:
                    file.write(f"{sec_id} {neighbor_id}\n")

        # Write EVs information
        num_evs = len(ev_info)
        file.write(f"{num_evs}\n")
        for ev_id, ev_data in ev_info.items():
            sec_id = ev_data['sec_id']
            ev_release_time = ev_data['ev_release_time']
            ev_battery_energy = ev_data['ev_battery_energy']
            ev_max_passengers = ev_data['ev_max_passengers']
            schedule_num_movs = len(ev_data['schedule'])

            file.write(f"{ev_id} {sec_id} {ev_release_time} {ev_battery_energy} {ev_max_passengers}\n")
            file.write(f"{schedule_num_movs}\n")
            for movement_info in ev_data['schedule']:
                file.write(" ".join(map(str, movement_info)) + "\n")

        # Write TPs information
        num_tps = len(tp_info)
        file.write(f"{num_tps}\n")
        for tp_id, tp_data in tp_info.items():
            sec_id = tp_data['sec_id']
            ev_id = tp_data['ev_id']
            trip_info = tp_data['trip_info']

            file.write(f"{tp_id} {sec_id} {ev_id}\n")
            file.write(",".join(map(str, trip_info)) + "\n")

if __name__ == '__main__':
    connections_rate = []
    num = 1.0
    while num <= 3.0:
        connections_rate.append(num)
        num += 0.1
    print(connections_rate)
    # GHC dataset
    # input_file_path = '../2_Instances/Metropolis/Instance_to_solve/input.in'
    # instances_folder = '../2_Instances/Metropolis/'

    # NYC Dataset
    input_file_path = '../2_Instances/NYC/Instance_to_solve/input.in'
    instances_folder = '../2_Instances/NYC/'
    out_file = 'input.in'
    (city_max_x_location, city_max_y_location, simulation_time_horizon, num_secs, sec_info, total_num_connections,
     sec_neighbors, num_evs, ev_info, num_tps, tp_info) = read_input_file(input_file_path)
    print(sec_neighbors)

    for connection in connections_rate:
        total_connections = int(num_secs * connection)
        print(total_connections)
        communities, community_neighbors = compute_neighbors.divide_and_compute_neighbors(city_max_x_location,
                                                                                          num_secs, total_connections)

        print(community_neighbors)
        out_path = instances_folder + '/Instance_1_'+str(total_connections)+'_connections/'+out_file

        output_directory = os.path.dirname(out_path)

        # Create the directory if it doesn't exist
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)

        # Create the directory
        os.makedirs(output_directory)
        write_output_file(out_path, city_max_x_location, city_max_y_location, simulation_time_horizon, sec_info,
                          community_neighbors, ev_info, tp_info)

    # total_connections = 1600
    # print(total_connections)
    # communities, community_neighbors = compute_neighbors.divide_and_compute_neighbors(city_max_x_location,
    #                                                                                   num_secs, total_connections)
    # out_path = instances_folder + '/Instance_1_' + str(total_connections) + '_connections/' + out_file
    #
    # output_directory = os.path.dirname(out_path)
    # # Create the directory if it doesn't exist
    # if os.path.exists(output_directory):
    #     shutil.rmtree(output_directory)
    #
    # # Create the directory
    # os.makedirs(output_directory)
    # write_output_file(out_path, city_max_x_location, city_max_y_location, simulation_time_horizon, sec_info,
    #                   community_neighbors, ev_info, tp_info)