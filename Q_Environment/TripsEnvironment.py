import numpy as np
import pandas as pd
from tqdm import tqdm
import time
import random
import codecs
import copy


class TripsEnvironment:
    def __init__(self,episodes, num_time_steps, communities, num_evs,
                 petitions_satisfied_energy_consumed, total_trips, total_energy, normal_total_trips_satisfied):
        self.episodes = episodes
        self.num_time_steps = num_time_steps
        self.current_time_step = 0
        self.communities = copy.deepcopy(communities)
        self.num_evs = num_evs
        self.petitions_satisfied_energy_consumed = petitions_satisfied_energy_consumed
        # Rebalance and compute reward based on trips
        self.q_communities = copy.deepcopy(communities)
        self.best_config_trips_satisfied = normal_total_trips_satisfied
        self.best_config_communities = copy.deepcopy(communities)
        self.total_trips = total_trips
        self.total_energy = total_energy
        self.actions = ['serve', 'rebalance_trips'] # serve: 0, rebalance_trips: 1
        self.states = []
        self.rewards = {}
        self.q_table = []

    def compute_initial_states_and_rewards(self):
        for community in self.communities:
            from_community_id = community.get_state()['id']
            for neighbor in community.get_state()['neighbors']:
                to_community_id = self.communities[neighbor-1].get_state()['id']
                for from_community_ev in range(1, self.num_evs+1):
                    for to_community_ev in range(1, self.num_evs+1):
                        if from_community_ev + to_community_ev > self.num_evs:
                            continue
                        for action in self.actions:
                            self.states.append((from_community_id, from_community_ev,
                                                to_community_id, to_community_ev, action))
        test_state = 0
        for state in self.states:
            test_state = state
            from_community_id, from_community_ev, to_community_id, to_community_ev, action = state
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(to_community_ev)
            from_community_petitions, from_community_energy = self.petitions_satisfied_energy_consumed[from_community_key]
            to_community_petitions, to_community_energy = self.petitions_satisfied_energy_consumed[to_community_key]
            if action == 'serve':
                self.rewards[state] = from_community_petitions
            else:
                reward = (from_community_petitions+to_community_petitions)/2
                self.rewards[state] = reward

        self.q_table = [np.random.rand(len(self.states), len(self.actions))
                        for _ in range(len(self.communities))]

    def compute_initial_trips_satisfied(self):
        total_trips_satisfied = 0
        total_energy_consumed = 0
        for community in self.communities:
            from_community_id = community.get_state()['id']
            from_community_ev = community.get_state()['available_vehicles']
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            community.set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])
            total_trips_satisfied += self.petitions_satisfied_energy_consumed[from_community_key][0]
            total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
        #     print(f"Commmunity ID: {community.get_state()['id']}")
        #     print(f"Available Vehicles: {community.get_state()['available_vehicles']}")
        #     print(f"Total Trips: {community.get_state()['total_trips']}\tTrips Satisfied: {community.get_state()['trips_satisfied']}")
        #     print(f"Energy Consumed: {self.petitions_satisfied_energy_consumed[from_community_key][1]}")
        #     print(f"------------------------------------------------------------------\n")
        # print(f"Total Trips Satisfied: {total_trips_satisfied}")
        # print(f"Total Energy Consumed: {total_energy_consumed}")

    def get_total_trips_satisfied_with_current_config(self):
        total_trips_satisfied = 0
        total_energy_consumed = 0
        for community in self.q_communities:
            from_community_id = community.get_state()['id']
            from_community_ev = community.get_state()['available_vehicles']
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            total_trips_satisfied += self.petitions_satisfied_energy_consumed[from_community_key][0]
            total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
        return total_trips_satisfied

    def target_policy(self, community):
        # print(f"Community-{community.get_state()['id']} Target Policy")
        target_policy= {}
        neighbors = community.get_state()['neighbors']
        from_community_id = community.get_state()['id']
        from_community_ev = community.get_state()['available_vehicles']
        for neighbor in neighbors:
            for action in self.actions:
                to_community_id = self.q_communities[neighbor-1].get_state()['id']
                to_community_ev = self.q_communities[neighbor-1].get_state()['available_vehicles']
                state = (from_community_id, from_community_ev, to_community_id, to_community_ev, action)
                target_policy[state] = self.q_table[from_community_id-1][self.states.index(state), self.actions.index(action)]
        return max(target_policy, key=target_policy.get)

    def exploratory_policy(self, community):
        # print(f"Community-{community.get_state()['id']} Exploratory Policy")
        target_policy= {}
        neighbors = community.get_state()['neighbors']
        from_community_id = community.get_state()['id']
        from_community_ev = community.get_state()['available_vehicles']
        neighbor = neighbors[np.random.randint(len(neighbors))]
        to_community_id = self.q_communities[neighbor - 1].get_state()['id']
        to_community_ev = self.q_communities[neighbor - 1].get_state()['available_vehicles']
        action = self.actions[np.random.randint(len(self.actions))]
        return (from_community_id, from_community_ev, to_community_id, to_community_ev, action)

    def run(self, alpha, gamma, epsilon):
        # Q-learning loop
        for episode in tqdm(range(self.episodes)):
            # self.reset()
            for t in tqdm(range(self.num_time_steps)):
                for i in range(len(self.q_communities)):
                    # np.random.seed(time.time())
                    from_community_id = self.q_communities[i].get_state()['id']
                    from_community_ev = self.q_communities[i].get_state()['available_vehicles']
                    to_community_id, to_community_ev, action = (0, 0, "")
                    current_state = ()
                    if np.random.uniform(0, 1) > epsilon:
                        from_community_id, from_community_ev, to_community_id, to_community_ev, action = self.target_policy(
                            self.q_communities[i])
                    else:
                        from_community_id, from_community_ev, to_community_id, to_community_ev, action = self.exploratory_policy(
                            self.q_communities[i]
                        )
                    current_state = (from_community_id, from_community_ev, to_community_id, to_community_ev, action)
                    next_state = current_state
                    # if action != 'serve':
                    if from_community_ev > 1:
                        total_vehicles = from_community_ev + to_community_ev
                        max_petitions = 0
                        key = ()
                        # Dividing the total vehicles available in the two communities to maximise trips satisfied
                        for v in range(1, total_vehicles + 1):
                            j = total_vehicles - v
                            if j > 0 and v < 50:
                                from_community_key = 'SEC_'+ str(from_community_id) + '_num_EVs_' + str(v)
                                to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(j)
                                petitions_city_1 = self.petitions_satisfied_energy_consumed[from_community_key][0]
                                petitions_city_2 = self.petitions_satisfied_energy_consumed[to_community_key][0]
                                total_petitions = petitions_city_1 + petitions_city_2
                                if total_petitions > max_petitions:
                                    max_petitions = total_petitions
                                    key = (v, j)
                        from_community_ev = key[0]
                        to_community_ev = key[1]
                        self.q_communities[i].set_vehicles(key[0])
                        self.q_communities[to_community_id-1].set_vehicles(key[1])
                        next_state = (from_community_id, from_community_ev, to_community_id, to_community_ev, action)
                        from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
                        to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(to_community_ev)
                        self.q_communities[i].set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])
                        self.q_communities[to_community_id-1].set_trips(self.petitions_satisfied_energy_consumed[to_community_key][0])
                        if self.get_total_trips_satisfied_with_current_config() > self.best_config_trips_satisfied:
                            self.best_config_trips_satisfied = self.get_total_trips_satisfied_with_current_config()
                            self.best_config_communities = copy.deepcopy(self.q_communities)

                    reward = self.rewards[next_state]
                    discounted_reward = self.q_table[i][self.states.index(current_state), self.actions.index(action)] + \
                                        alpha * (reward + gamma * np.max(self.q_table[i][self.states.index(next_state)])) - \
                                        self.q_table[i][self.states.index(current_state), self.actions.index(action)]

                    self.q_table[i][self.states.index(current_state), self.actions.index(action)] = discounted_reward


    def print_results(self, path, csv_file, data_to_append, elapsed_time):
        # my_output_stream.write(f"Generating {path} took {elapsed_time} seconds\n")
        n_total_trips_satisfied = 0
        n_total_energy_consumed = 0
        data_to_append['File Name'].append(path)
        data_to_append['Episodes'].append(self.episodes)
        data_to_append['Trips Satisfied'].append(self.best_config_trips_satisfied)
        data_to_append['Total Trips'].append(self.total_trips)

        for community in self.communities:
            from_community_id = community.get_state()['id']
            from_community_ev = community.get_state()['available_vehicles']
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            community.set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])
            n_total_trips_satisfied += self.petitions_satisfied_energy_consumed[from_community_key][0]
            n_total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]

        # NYC Dataset
        # if self.best_config_trips_satisfied > n_total_trips_satisfied:
        #     my_output_stream = codecs.open(path, "w", encoding="utf-8")
        #     my_output_stream.write(f"Generating {path} took {elapsed_time} seconds\n")
        #     for community in self.communities:
        #         from_community_id = community.get_state()['id']
        #         from_community_ev = community.get_state()['available_vehicles']
        #         from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
        #         total_trips_satisfied += self.petitions_satisfied_energy_consumed[from_community_key][0]
        #         total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
        #         my_output_stream.write(f"Commmunity ID: {community.get_state()['id']}\n")
        #         my_output_stream.write(f"Available Vehicles: {community.get_state()['available_vehicles']}\n")
        #         my_output_stream.write(f"Total Trips: {community.get_state()['total_trips']}\tTrips Satisfied: {community.get_state()['trips_satisfied']}\n")
        #         my_output_stream.write(f"Energy Consumed: {self.petitions_satisfied_energy_consumed[from_community_key][1]}\n")
        #         my_output_stream.write(f"------------------------------------------------------------------\n")
        #     my_output_stream.write(f"\t\t\tTotal Trips Satisfied: {total_trips_satisfied}\n")
        #     my_output_stream.write(f"\t\t\tTotal Energy Consumed: {total_energy_consumed}\n")
        #     my_output_stream.write(f"------------------------------------------------------------------\n")
        #     total_trips_satisfied = 0
        #     total_energy_consumed = 0
        #     for community in self.best_config_communities:
        #         from_community_key = 'SEC_' + str(community.get_state()['id']) + "_num_EVs_" + str(community.get_state()['available_vehicles'])
        #         my_output_stream.write(f"Commmunity ID: {community.get_state()['id']}\n")
        #         my_output_stream.write(f"Available Vehicles: {community.get_state()['available_vehicles']}\n")
        #         total_trips_satisfied += community.get_state()['trips_satisfied']
        #         total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
        #         my_output_stream.write(f"Total Trips: {community.get_state()['total_trips']}\tTrips Satisfied: {community.get_state()['trips_satisfied']}\n")
        #         my_output_stream.write(f"Energy Consumed: {self.petitions_satisfied_energy_consumed[from_community_key][1]}\n")
        #         my_output_stream.write(f"------------------------------------------------------------------\n")
        #
        #     my_output_stream.write(f"\t\t\tTotal Trips Satisfied: {n_total_trips_satisfied}\n")
        #     my_output_stream.write(f"\t\t\tTotal Energy Consumed: {n_total_energy_consumed}\n")

        # Constraint for good confogs for Metropolis Dataset
        # if self.best_config_trips_satisfied > 4900:
        my_output_stream = codecs.open(path, "w", encoding="utf-8")
        csv_stream = pd.read_excel(csv_file)

        my_output_stream.write(f"Generating {path} took {elapsed_time} seconds\n")
        total_trips_satisfied = 0
        total_energy_consumed = 0
        for community in self.communities:
            from_community_id = community.get_state()['id']
            from_community_ev = community.get_state()['available_vehicles']
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            community.set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])
            total_trips_satisfied += self.petitions_satisfied_energy_consumed[from_community_key][0]
            total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
            my_output_stream.write(f"Commmunity ID: {community.get_state()['id']}\n")
            my_output_stream.write(f"Available Vehicles: {community.get_state()['available_vehicles']}\n")
            my_output_stream.write(
                f"Total Trips: {community.get_state()['total_trips']}\tTrips Satisfied: {community.get_state()['trips_satisfied']}\n")
            my_output_stream.write(
                f"Energy Consumed: {self.petitions_satisfied_energy_consumed[from_community_key][1]}\n")
            my_output_stream.write(f"------------------------------------------------------------------\n")
        my_output_stream.write(f"\t\t\tTotal Trips Satisfied: {total_trips_satisfied}\n")
        my_output_stream.write(f"\t\t\tTotal Energy Consumed: {total_energy_consumed}\n")
        my_output_stream.write(f"------------------------------------------------------------------\n")

        total_trips_satisfied = 0
        total_energy_consumed = 0
        for community in self.best_config_communities:
            from_community_key = 'SEC_' + str(community.get_state()['id']) + "_num_EVs_" + str(
                community.get_state()['available_vehicles'])
            my_output_stream.write(f"Commmunity ID: {community.get_state()['id']}\n")
            my_output_stream.write(f"Available Vehicles: {community.get_state()['available_vehicles']}\n")
            total_trips_satisfied += community.get_state()['trips_satisfied']
            total_energy_consumed += self.petitions_satisfied_energy_consumed[from_community_key][1]
            my_output_stream.write(
                f"Total Trips: {community.get_state()['total_trips']}\tTrips Satisfied: {community.get_state()['trips_satisfied']}\n")
            my_output_stream.write(
                f"Energy Consumed: {self.petitions_satisfied_energy_consumed[from_community_key][1]}\n")
            my_output_stream.write(f"------------------------------------------------------------------\n")

        my_output_stream.write(f"\t\t\tTotal Trips Satisfied: {total_trips_satisfied}\n")
        my_output_stream.write(f"\t\t\tTotal Energy Consumed: {total_energy_consumed}\n")
        data_to_append['Total Energy Consumed'].append(total_energy_consumed)



    def reset(self):
        self.q_communities = copy.deepcopy(self.communities)

    def get_state_information(self, community_index):
        # Extract the current state information
        from_community_id = self.q_communities[community_index].get_state()['id']
        from_community_ev = self.q_communities[community_index].get_state()['available_vehicles']
        from_community_trips_satisfied = self.q_communities[community_index].get_state()['trips_satisfied']
        chosen_neighbor = 0
        to_community_id = random.choice(self.q_communities[community_index].get_state()['neighbors'])
        chosen_neighbor = to_community_id# randomly choosing a neighbor
        epsilon = 0.1
        if np.random.uniform(0, 1) > epsilon:
            for neighbor in self.q_communities[community_index].get_state()['neighbors']:
                neighbor_trips_satisfied_counter = self.q_communities[neighbor-1].get_state()['trips_satisfied']
                if (neighbor_trips_satisfied_counter + from_community_trips_satisfied)/2 > from_community_trips_satisfied:
                        chosen_neighbor = neighbor
            to_community_id = chosen_neighbor
        to_community_ev =self.q_communities[to_community_id - 1].get_state()['available_vehicles']
        return from_community_id, from_community_ev, to_community_id, to_community_ev

    def get_state_representation(self):
        # Combine the state information and return as a tuple
        state_representation = []
        for community in self.q_communities:
            community_id = community.get_state()['id']
            available_vehicles = community.get_state()['available_vehicles']
            energy_consumed = community.get_state()['energy_consumed']
            trips_satisfied = community.get_state()['trips_satisfied']
            state_representation.extend([community_id, available_vehicles, trips_satisfied, energy_consumed])
        return np.array(state_representation)

    def serve(self, from_community_id, from_community_ev):
        # Update trips satisfied and energy consumed based on the action
        from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
        self.q_communities[from_community_id-1].set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])

    def rebalance_trips(self, from_community_id, from_community_ev, to_community_id, to_community_ev):
        # Rebalance vehicles and update trips satisfied and energy consumed
        if from_community_ev > 1:
            total_vehicles = from_community_ev + to_community_ev
            max_petitions = 0
            key = ()
            for v in range(1, total_vehicles + 1):
                j = total_vehicles - v
                if j > 0 and v < 50:
                    from_community_key = 'SEC_' + str(from_community_id) + '_num_EVs_' + str(v)
                    to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(j)
                    petitions_city_1 = self.petitions_satisfied_energy_consumed[from_community_key][0]
                    petitions_city_2 = self.petitions_satisfied_energy_consumed[to_community_key][0]
                    total_petitions = petitions_city_1 + petitions_city_2
                    if total_petitions > max_petitions:
                        max_petitions = total_petitions
                        key = (v, j)
            from_community_ev = key[0]
            to_community_ev = key[1]
            self.q_communities[from_community_id - 1].set_vehicles(key[0])
            self.q_communities[to_community_id - 1].set_vehicles(key[1])
            from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
            to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(to_community_ev)
            self.q_communities[from_community_id-1].set_trips(self.petitions_satisfied_energy_consumed[from_community_key][0])
            self.q_communities[to_community_id-1].set_trips(self.petitions_satisfied_energy_consumed[to_community_key][0])

    def calculate_reward(self, from_community_id, from_community_ev, to_community_id, to_community_ev, action):
        # Calculate the reward based on the new state
        from_community_key = 'SEC_' + str(from_community_id) + "_num_EVs_" + str(from_community_ev)
        to_community_key = 'SEC_' + str(to_community_id) + "_num_EVs_" + str(to_community_ev)
        from_community_petitions, _ = self.petitions_satisfied_energy_consumed[from_community_key]
        if to_community_key == 0:
            print(to_community_id)
        to_community_petitions, _ = self.petitions_satisfied_energy_consumed[to_community_key]
        reward = 0
        # if action == 'serve':
        #     reward = from_community_petitions
        # else:
        #     reward = (from_community_petitions + to_community_petitions) / 2
        reward = (from_community_petitions + to_community_petitions) / 2
        return reward




