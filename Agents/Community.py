class Community:
    def __init__(self, community_id, x_loc, y_loc, initial_vehicle_count, trips, neighbors):
        self.community_id = community_id
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.initial_vehicle_count = initial_vehicle_count
        self.available_vehicles = initial_vehicle_count
        self.initial_trips = trips
        self.neighbors = neighbors
        self.reward = 0
        self.trips_satisfied = 0
        self.energy_consumed = 0
        self.energy_available = 0

    def reset(self):
        self.available_vehicles = self.initial_vehicle_count
        self.trips_satisfied = 0
        self.energy_consumed = 0
        self.reward = 0

    def get_state(self):
        # Return the current state of the community
        state = {
            'id': self.community_id,
            'initial_vehicle_count': self.initial_vehicle_count,
            'available_vehicles': self.available_vehicles,
            'total_trips': self.initial_trips,
            'trips_satisfied': self.trips_satisfied,
            'energy_consumed': self.energy_consumed,
            'energy_available': self.energy_available,
            'neighbors': self.neighbors,
            'reward': self.reward
        }
        return state

    def set_vehicles(self, available_vehicles):
        self.available_vehicles = available_vehicles
        self.energy_available = available_vehicles * 100

    def set_trips(self, trips_satisfied):
        self.trips_satisfied = trips_satisfied

    def set_energy(self, energy_consumed):
        self.energy_consumed = energy_consumed

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors