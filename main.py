from utilities import parse_in, compute_neighbors
import codecs
from Q_Environment import TripsEnvironment, EnergyEnvironment
from Deep_Q_Environment import DeepTripsEnvironment, DeepEnergyEnvironment
# from Ccmomarl_Environment import CCMOMARLEnvironment
from Agents.Community import Community
import os
import shutil
import time

def parse_initial_data():

    # Read the Input file
    file = './ride_sharing_framework/2_Instances/Instance_to_solve/d_metropolis.in'
    (city, SECs, neighbors, EVs, TPs, TDs) = parse_in.parse_in(file)
    print(f"City Dimensions: {city[0]}X{city[1]}")
    # Getting the number of Vehicles and TPs for each SEC at the start of the simulation
    community_trips = {}
    for id in SECs.keys():
        v_count = 0
        t_count = 0
        community_trips[id] = []
        for e_id in EVs.keys():
            if EVs[e_id][0][0] == id:
                v_count += 1
        for t_id in TPs.keys():
            if TPs[t_id][1] == id:
                community_trips[id].append(t_id)
                t_count+=1
        SECs[id] = SECs[id] + (v_count, t_count,)
    print(f"SEC IDS: {list(SECs.keys())} ")


    community_numbers = list(SECs.keys())
    community_indices = [(SECs[community_number][0], SECs[community_number][1])
                         for community_number in community_numbers]
    print(f"SEC Locations: {community_indices}")
    community_vehicles_petitions = [(SECs[community_number][2], SECs[community_number][3])
                         for community_number in community_numbers]
    print(f"SEC Vehicles and Petitions: {community_vehicles_petitions}")
    print(f"Neighbors: {neighbors}")

    # Create the Commmumities
    communities = []
    for index in range(len(community_numbers)):
        id = community_numbers[index]
        # For NYC uncomment following line and comment above]
        # id = community_numbers[index]
        x_loc, y_loc = community_indices[index]
        initial_vehicle_count, initial_trips = community_vehicles_petitions[index]
        community_neighbors = neighbors[index+1]
        if len(community_neighbors) == 0:
            community_neighbors = [id-1]
        action = 'serve'
        c = Community(id, x_loc, y_loc, initial_vehicle_count, initial_trips,
                                     community_neighbors)
        communities.append(c)

    # Reading the solutions file for getting the number of trips satisfied and energy consumed
    # solutions_file = './ride_sharing_framework/4_Solutions/2_Instance_Subproblem_Solutions/subproblem_solutions.csv'
    solutions_file = './ride_sharing_framework/4_Solutions/subproblem_solutions.csv'
    requests_satisfied_data = {}
    with codecs.open(solutions_file, "r", encoding='utf-8') as f:
        data = f.readlines()
        for line in data:
            path, trips_satisfied, energy_consumed = line.strip().split(';')
            requests_satisfied_data[path.split('/')[5].split('.')[0]] = (int(trips_satisfied), float(energy_consumed))

    num_evs = len(EVs.keys())
    return communities, num_evs, requests_satisfied_data, community_vehicles_petitions


if __name__ == '__main__':
    # Run the Q Environment
    communities, num_evs, requests_satisfied_data, community_vehicle_petitions = parse_initial_data()
    total_trips = 0
    total_energy = 0
    for item in community_vehicle_petitions:
        (ev, trips) = item
        total_trips += trips
        total_energy += (ev * 100)

    alphas = [0.1, 0.2, 0.3]
    gammas = [0.7, 0.8, 0.9]
    # alphas = [0.3]
    # gammas = [0.8]
    epsilon = 0.1
    episodes = [5, 10, 15, 20]
    # episodes = [5]
    num_days = [5]
    # episodes = [10]
    # num_days = [10]
    paths = ['./output/trips_environment/metropolis/',
             # './output/energy_environment/metropolis/',
             './output/deep_trips_environment/metropolis_terminal/',
             # './output/deep_energy_environment/metropolis/',
            ]
    # paths = ['./output/ccmomarl_environment']

    for path in paths:
        if os.path.exists(path):
            os.chmod(path, 0o777)
            shutil.rmtree(path)
        os.mkdir(path)
    for alpha in alphas:
        for gamma in gammas:
            for episode in episodes:
                for num_day in num_days:
                    file_name = str(episode)+'_episode_'+str(num_day)+'_days_'+str(alpha)+'_alpha_'+str(gamma)+'_gamma.txt'
                    csv_file =  str(episode)+'_episode_'+str(num_day)+'_days_'+str(alpha)+'_alpha_'+str(gamma)+'_gamma.csv'
                    normal_total_trips_satisfied = 0
                    normal_total_energy_consumed = 0
                    for community in communities:
                        from_community_id = community.get_state()['id']
                        from_community_ev = community.get_state()['available_vehicles']
                        from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
                        community.set_trips(requests_satisfied_data[from_community_key][0])
                        normal_total_trips_satisfied += requests_satisfied_data[from_community_key][0]
                        normal_total_energy_consumed += requests_satisfied_data[from_community_key][1]

                    start_time = time.time()
                    path = paths[0]+file_name
                    trips_env = TripsEnvironment(episode, num_day, communities, num_evs,
                                                 requests_satisfied_data, total_trips, total_energy, normal_total_trips_satisfied)
                    trips_env.compute_initial_states_and_rewards()
                    trips_env.compute_initial_trips_satisfied()
                    trips_env.run(alpha, gamma, epsilon)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    trips_env.print_results(path, elapsed_time)
                    #
                    # start_time = time.time()
                    # path = paths[1]+file_name
                    # energy_env = EnergyEnvironment(episode, num_day, communities, num_evs,
                    #                                requests_satisfied_data, total_trips, total_energy)
                    # energy_env.compute_initial_states_and_rewards()
                    # energy_env.compute_initial_trips_satisfied()
                    # energy_env.run()
                    # end_time = time.time()
                    # elapsed_time = end_time - start_time
                    # energy_env.print_results(path, elapsed_time)

                    # start_time = time.time()
                    # csv_path = paths[2]+csv_file
                    # path = paths[2]+file_name
                    # state_size = len(communities) * 4
                    # action_size = 2
                    # deep_trips_env = DeepTripsEnvironment(episode, num_day, communities, num_evs,
                    #                                       requests_satisfied_data,
                    #                                       state_size, action_size,
                    #                                       total_trips, total_energy,
                    #                                       csv_path, alpha, gamma, normal_total_trips_satisfied)
                    # deep_trips_env.run()
                    # end_time = time.time()
                    # elapsed_time = end_time - start_time
                    # deep_trips_env.print_results(path, elapsed_time)

                    # csv_path = paths[3]+csv_file
                    # path = paths[3]+file_name
                    # state_size = len(communities) * 4
                    # action_size = 2
                    # deep_energy_env = DeepEnergyEnvironment(episode, num_day, communities, num_evs,
                    #                                       requests_satisfied_data,
                    #                                       state_size, action_size,
                    #                                         total_trips, total_energy,
                    #                                         csv_path)
                    # deep_energy_env.run()
                    # deep_energy_env.print_results(path)

                    # path = paths[4]+file_name
                    # path = paths[0]
                    # ccmomarl_env = CCMOMARLEnvironment(episode, num_day, communities, num_evs,
                    #                                requests_satisfied_data, total_trips, total_energy, path)
                    # ccmomarl_env.run()




