import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
from models import Actor, Critic
from replay_buffer import ReplayBuffer

class DDPGAgent:
    def __init__(self, env, gamma=0.99, tau=0.001, actor_lr=0.0001, critic_lr=0.001, batch_size=64, buffer_size=int(1e6)):
        self.env = env
        self.gamma = gamma
        self.tau = tau
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        self.batch_size = batch_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"{self.device}")

        # Create actor and critic networks
        self.actor = Actor(env.observation_space.shape[0], env.action_space.nvec).to(self.device)
        self.actor_target = Actor(env.observation_space.shape[0], env.action_space.nvec).to(self.device)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=self.actor_lr)

        self.critic = Critic(env.observation_space.shape[0], env.action_space.nvec).to(self.device)
        self.critic_target = Critic(env.observation_space.shape[0], env.action_space.nvec).to(self.device)
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=self.critic_lr)

        self.replay_buffer = ReplayBuffer(buffer_size)

    def predict(self, state, deterministic=True):
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        self.actor.eval()
        with torch.no_grad():
            action = self.actor(state).cpu().data.numpy()
        self.actor.train()
        return action[0]

    def train(self, num_timesteps):
        for _ in range(num_timesteps):
            # Sample a batch from the replay buffer
            states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

            # Update the critic
            next_actions = self.actor_target(next_states)
            next_q_values = self.critic_target(next_states, next_actions)
            target_q_values = rewards + self.gamma * next_q_values * (1 - dones)
            q_values = self.critic(states, actions)
            critic_loss = nn.MSELoss()(q_values, target_q_values)
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            self.critic_optimizer.step()

            # Update the actor
            actor_loss = -self.critic(states, self.actor(states)).mean()
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

            # Soft-update the target networks
            self.soft_update(self.actor, self.actor_target)
            self.soft_update(self.critic, self.critic_target)

    def soft_update(self, source, target):
        for src_param, target_param in zip(source.parameters(), target.parameters()):
            target_param.data.copy_(self.tau * src_param.data + (1 - self.tau) * target_param.data)

    def store_transition(self, state, action, reward, next_state, done):
        self.replay_buffer.add(state, action, reward, next_state, done)
