from scipy.stats import weibull_min
import numpy as np
import random as r


def generateWeibullDis(sample_size, sys_energy, energy_required, num_sec):
    sample_size = int(sample_size)
    data = np.random.random((sample_size, 1))
    total = [int((sys_energy * energy_required)/num_sec)]
    return corrections(data, total, sample_size)

# Here we ensure the system energy parameter is not compromised
# The Energy generated adds up to sys_energy*energy_required_by_trip_petitions
def corrections(data, total, sample_size):
    data = data/np.sum(data, axis =0) * total
    data = np.round(data)
    remainings = total - np.sum(data, axis = 0)
    for j, r in enumerate(remainings):
        step = 1 if r > 0 else -1
        while r != 0:
            i = np.random.randint(sample_size-1)
            if data[i, j] + step >= 0:
                data[i, j] += step
                r -= step
    return data