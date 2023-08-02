class NewDeepTripsEnvironment(DeepTripsEnvironment):
    def __init__(self, community, input_dim, hidden_dim, output_dim, deep_model):
        super(NewDeepTripsEnvironment, self).__init__(community, deep_model)
        self.gcn_experience_sharing = GCNExperienceSharing(community, input_dim, hidden_dim, output_dim)

    def train(self, epochs):
        for epoch in range(epochs):
            # Run experience sharing using GCN
            self.gcn_experience_sharing.run_experience_sharing()

            # Train deep model with updated rewards (without modifying DeepTripsEnvironment)
            super().train(1)  # Call the original train() method for one epoch
