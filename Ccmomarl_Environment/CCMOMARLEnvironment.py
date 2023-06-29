import random

import numpy as np
import gym
from gym import spaces
from Q_Environment import TripsEnvironment
import torch
import torch.nn as nn
from torch.optim import Adam
from ddpg_agent import DDPGAgent
import csv

class CCMOMARLEnvironment(gym.Env):
    def __init__(self, episodes, num_time_steps, communities, num_evs, petitions_satisfied_energy_consumed,
                 total_trips, total_energy, path):
        super().__init__()
        self.env = TripsEnvironment(episodes, num_time_steps, communities, num_evs,
                                    petitions_satisfied_energy_consumed, total_trips, total_energy)
        self.num_agents = len(self.env.q_communities)
        self.agent = self.create_agent()

        # Assuming two actions: serve and rebalance_trips
        self.action_space = spaces.MultiDiscrete([2] * num_agents)
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(len(self.env.communities) * 4,), dtype=np.float32)
        self.path = path

    def create_agent(self):
        agent = DDPGAgent(self)
        return agent

    def get_joint_action(self, joint_state):
        return self.agent.predict(joint_state, deterministic=True)

    def step(self, action):
        self.execute_joint_action(action)
        joint_reward = self.calculate_joint_reward(action)
        next_joint_state = self.get_joint_state_representation()
        done = self.env.current_time_step >= self.env.num_time_steps - 1
        return next_joint_state, joint_reward, done, {}

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        pass  # You can implement a rendering method if needed

    def get_joint_state_information(self):
        joint_state_information = []
        for community in self.env.q_communities:
            joint_state_information.append(community.get_state()['id'])
            joint_state_information.append(community.get_state()['available_vehicles'])
            joint_state_information.append(community.get_state()['trips_satisfied'])
            joint_state_information.append(community.get_state()['energy_consumed'])
        return joint_state_information

    def get_joint_state_representation(self):
        joint_state_representation = np.zeros(len(self.env.q_communities) * 4)
        for i, community in enumerate(self.env.q_communities):
            joint_state_representation[i * 4] = community.get_state()['id']
            joint_state_representation[i * 4 + 1] = community.get_state['available_vehicles']
            joint_state_representation[i * 4 + 2] = community.get_state()['trips_satisfied']
            joint_state_representation[i * 4 + 3] = community.get_state()['energy_consumed']
        return joint_state_representation

    def calculate_joint_reward(self, joint_action, community_index):
        total_petitions_satisfied = sum([community.get_state()['trips_satisfied'] for community in self.env.q_communities])
        total_energy_consumed = sum([community.get_state()['energy_consumed'] for community in self.env.q_communities])

        petitions_satisfaction_ratio = total_petitions_satisfied / self.env.total_trips
        energy_consumption_ratio = total_energy_consumed / self.env.total_energy

        return petitions_satisfaction_ratio, energy_consumption_ratio

    def execute_joint_action(self, joint_action):
        actions = self.translate_joint_action(joint_action)

        for action in actions:
            # Assuming that the actions are defined per community
            for community in self.env.q_communities:
                if action == 'serve':
                    self.env.serve(community.id)
                elif action == 'rebalance_trips':
                    from_community_id = community.id
                    to_community_id = random.choice(community.get_state()['neighbors'])
                    self.env.rebalance_trips(from_community_id, to_community_id)

    def translate_joint_action(self, joint_action):
        return [self.env.actions[action_id] for action_id in joint_action]

    def run(self):
        # Train the agent
        self.agent.train(self.num_time_steps * self.episodes)
        # Initialize lists to store data
        rewards = []
        joint_states = []
        joint_actions = []

        # Run the experiment
        for episode in range(self.episodes):
            self.reset()
            joint_state = self.get_joint_state_representation()

            for t in range(self.num_time_steps):
                for community_index in range(len(self.env.q_communities)):
                    joint_action, _ = self.get_joint_action(joint_state)
                    self.execute_joint_action(joint_action)
                    joint_reward = self.calculate_joint_reward(joint_action, community_index)
                    next_joint_state = self.get_joint_state_representation()

                    # You can save the reward, joint_state, and joint_action information for analysis here.
                    # Save the reward, joint_state, and joint_action information for analysis
                    rewards.append(joint_reward)
                    joint_states.append(joint_state.tolist())
                    joint_actions.append(joint_action.tolist())

                    joint_state = next_joint_state
                    self.env.current_time_step += 1
            # Save the data to a CSV file
        with open("data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Joint State", "Joint Action", "Joint Reward"])
            for state, action, reward in zip(joint_states, joint_actions, rewards):
                writer.writerow([state, action, reward])
        self.env.print_results(self.path)

