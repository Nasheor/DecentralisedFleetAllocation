import copy

from Q_Environment import TripsEnvironment
import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from collections import deque
import csv

class DeepTripsEnvironment(TripsEnvironment):
    def __init__(self, episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed,
                 state_size, action_size, total_trips, total_energy, file_name, alpha, gamma, normal_total_trips_satisfied):
        super().__init__(episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed,
                         total_trips, total_energy, normal_total_trips_satisfied)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Limited size memory for efficiency
        self.batch_size = 64
        self.learning_rate = 0.01
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma =gamma
        self.target_update_freq = 200
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.csv_file = file_name


    def build_model(self):
        model = Sequential()
        model.add(Dense(128, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
            self.model.fit(state, target, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def run(self):
        step_count = 0
        rewards = []
        states = []
        actions = []
        for episode in range(self.episodes):
        # self.reset()
        # for t in range(self.num_time_steps):
            for i in range(len(self.q_communities)):
                # Convert the state to an appropriate input for the neural network
                state = np.reshape(self.get_state_representation(), [1, self.state_size])
                action = self.act(state)
                reward, next_state, done = self.step(action, community_index=i)
                next_state = np.reshape(next_state, [1, self.state_size])

                states.append(state)
                actions.append(action)
                rewards.append((reward))

                self.remember(state, action, reward, next_state, done)
                if self.get_total_trips_satisfied_with_current_config() > self.best_config_trips_satisfied:
                    self.best_config_communities = copy.deepcopy(self.q_communities)
                    self.best_config_trips_satisfied = self.get_total_trips_satisfied_with_current_config()
                state = next_state

                self.replay()

                step_count += 1
                if step_count % self.target_update_freq == 0:
                    self.update_target_model()
        # with open(self.csv_file, "w", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(["State", "Action", "Reward"])
        #     for state, action, reward in zip(states, actions, rewards):
        #         writer.writerow([state, action, reward])

    def step(self, action, community_index):
        # Implement the logic for executing the chosen action and returning the next state, reward, and completion status
        done = False

        # Extract the current state information
        from_community_id, from_community_ev, to_community_id, to_community_ev = self.get_state_information(community_index)

        # Perform the action
        # if self.actions[action] == 'serve':
        #     # Update trips satisfied and energy consumed based on the action
        #     self.serve(from_community_id, from_community_ev)
        # elif self.actions[action] == 'rebalance_trips':
        #     # Rebalance vehicles and update trips satisfied and energy consumed
        #     self.rebalance_trips(from_community_id, from_community_ev, to_community_id, to_community_ev)
        self.rebalance_trips(from_community_id, from_community_ev, to_community_id, to_community_ev)

        # Get the next state information
        next_state = self.get_state_representation()

        # Calculate the reward based on the new state
        reward = self.calculate_reward(from_community_id, from_community_ev, to_community_id, to_community_ev, self.actions[action])

        return reward, next_state, done

