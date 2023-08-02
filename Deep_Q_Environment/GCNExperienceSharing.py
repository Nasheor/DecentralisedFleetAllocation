import torch
import torch.nn as nn
import torch.nn.functional as F

class GCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.5):
        super(GCN, self).__init__()
        self.gc1 = nn.Linear(input_dim, hidden_dim)
        self.gc2 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, adj_matrix):
        x = F.relu(self.gc1(x))
        x = self.dropout(x)
        x = self.gc2(x)
        x = torch.matmul(adj_matrix, x)  # Adjacency matrix-based aggregation
        return x

class GCNExperienceSharing:
    def __init__(self, community, input_dim, hidden_dim, output_dim):
        self.community = community
        self.gcn_model = GCN(input_dim, hidden_dim, output_dim)

    def compute_adjacency_matrix(self):
        # Compute adjacency matrix based on agent relationships in the community
        # For example, you can use the "Neighbors" dictionary from the previous data
        adj_matrix = ...
        return adj_matrix

    def run_experience_sharing(self):
        # Collect experiences and rewards for all agents
        all_experiences = []
        all_rewards = []
        for agent in self.community.agents:
            all_experiences.append(agent.get_experience())
            all_rewards.append(agent.reward)

        # Experience sharing using GCN model
        all_experiences_tensor = torch.stack(all_experiences)
        all_rewards_tensor = torch.tensor(all_rewards).unsqueeze(1)
        adj_matrix = self.compute_adjacency_matrix()
        shared_rewards = self.gcn_model(all_rewards_tensor, adj_matrix)

        # Update Q-values of each agent based on shared rewards
        for i, agent in enumerate(self.community.agents):
            agent.update_q_value(shared_rewards[i])
