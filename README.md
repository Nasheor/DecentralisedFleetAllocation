# Multi-Agent Reinforcement Learning for Electric Vehicle Fleet Management
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

This repository contains a collection of Python classes implementing multi-agent reinforcement learning (MARL) environments and agents to optimize the management of electric vehicle (EV) fleets. The primary objective is to maximize trip satisfaction while minimizing energy consumption in the system.

## Classes
#### Community
This class represents a community in the electric vehicle fleet management system. Each community has a unique ID, available vehicles, satisfied trips, and energy consumed. The community class also stores information about neighboring communities.

#### TripsEnvironment
TripsEnvironment is a Gym environment designed to model the trips-based aspect of electric vehicle fleet management. The environment contains multiple communities with unique trip demands, and the agents must decide how to distribute vehicles to satisfy as many trips as possible.

##### EnergyEnvironment
EnergyEnvironment is another Gym environment specifically focused on the energy consumption aspect of electric vehicle fleet management. This environment contains multiple communities with unique energy demands, and the agents must decide how to distribute energy to minimize total energy consumption in the system.

#### DeepTripsEnvironment
DeepTripsEnvironment is an extension of TripsEnvironment and incorporates a deep reinforcement learning model. This environment is designed to handle more complex scenarios and can adapt better to dynamic situations compared to the basic TripsEnvironment.

#### DeepEnergyEnvironment
DeepEnergyEnvironment extends the EnergyEnvironment and incorporates a deep reinforcement learning model. Like the DeepTripsEnvironment, it is designed to handle more complex energy management scenarios and adapt better to changing situations.

#### CCMOMARLEnvironment
CCMOMARLEnvironment (Cooperative Coevolutionary Multi-Objective MARL Environment) is a custom Gym environment that integrates both the trips and energy aspects of electric vehicle fleet management into a single multi-objective optimization problem. This environment uses a DDPG agent to make decisions for multiple communities, and the objective is to maximize trip satisfaction while minimizing energy consumption.

## Usage
To use the provided classes, first install the required packages using the requirements.txt file:

```
pip install -r requirements.txt
```
Next, import the necessary classes and instantiate the desired environment:

```
from Community import Community
from Q_Environment import TripsEnvironment, EnergyEnvironment
from DeepQ_Environment import DeepTripsEnvironment, DeepEnergyEnvironment
from CCMOMARLEnvironment import CCMOMARLEnvironment

# Example: Create a TripsEnvironment instance
trips_env = TripsEnvironment(episodes, num_time_steps, communities, num_evs,
                             petitions_satisfied_energy_consumed, total_trips, total_energy)

# Example: Create a CCMOMARLEnvironment instance
ccmomarl_env = CCMOMARLEnvironment(episodes, num_time_steps, communities, num_evs,
                                   petitions_satisfied_energy_consumed, total_trips, total_energy, path)

```

To train and run the desired environment, call the run() method of the environment:
```
# Train and run the CCMOMARLEnvironment
ccmomarl_env.run()
```

## Results
The environments will save the data to a CSV file named data.csv after running the experiment. The file will contain joint states, joint actions, and joint rewards for each time step.

Additionally, the CCMOMARLEnvironment class provides a method print_results(path) that prints the final results of the environment after the experiment is completed.

## License
This project is licensed under the MIT License.