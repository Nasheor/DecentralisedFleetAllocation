import sys
import random as r
import modal
import distributions
import codecs
import tkinter as tk
from tkinter import filedialog
import seaborn
import pandas as pd
import datetime
import math
import os
import shutil
import pandas as pd
import compute_neighbors


# constraints = {
#     'secs': [1, 4, 16],
#     'tps': [300, 1000, 10000],
#     'evs': [1.0, 1.5, 2.0],
#     'sys_energy': [0.5, 1.0, 2.0, 4.0, 5.0, 6.0],
#     'flexiblity': [2, 10, 25, 50],
#     'dispatch': ['start', 'spread']
# }
constraints = {
    'secs': [262],
    'tps': [50000],
    'evs': [ 100.0],
    'sys_energy': [10.0],
    'flexiblity': [25],
    'connections':[261, 600, 1600]
}

# constraints = {
#     'secs': [16],
#     'tps': [300],
#     'evs': [1.0],
#     'sys_energy': [6.0],
#     'flexiblity': [10],
#     'dispatch': ['start']
# }

raw_petitions = []

def writeToFile(time_horizon, grid_size, secs, evs, passengers, petitions, energy_required,
                flexiblity, sys_energy, dispatch_mode, ev_factor, total_evs, instance_level_energy_produced,
                connections, neighbors):
    # outfile ="./instances/"+file_type+"/"+str(file_num)+".txt"
    # output_folder = './instances/evaluation_spread_mode/'+str(flexiblity)+'_FLEX_'+str(sys_energy)+'_SYS_ENERGY/'
    outfile = './instances/'+str(dispatch_mode)+'_'+str(len(secs))+'_SEC_'+str(sys_energy)+'_ENERGY_'+\
                    str(ev_factor)+'_EV-FACTOR_'+str(len(evs))+'_EV_'+\
              str(flexiblity)+'_FLEX_'+str(len(petitions))+"_TPS_"+str(connections)+"_CONNECTIONS.txt"

    # excelfile = './analysis/'+str(dispatch_mode)+'_'+str(len(secs))+'_SEC_'+str(sys_energy)+'_ENERGY_'+\
    #                 str(ev_factor)+'_EV-FACTOR_'+str(len(evs))+'_EV_'+\
    #           str(flexiblity)+'_FLEX_'+str(len(petitions))+"_TPS_"+str(connections)+"_CONNECTIONS.xlsx"

    outstream = codecs.open(outfile, "w", encoding="utf-8")
    outstream.write(str(grid_size)+" "+str(grid_size)+" "+str(time_horizon)+"\n")
    outstream.write(str(len(secs))+"\n")
    energy_produced = 0
    analysis_data = pd.DataFrame(columns=['Petitions', 'Distance', 'Total Energy Produced', 'Total Energy Required'])
    for sec in secs:
        sec_str = str(sec.sec_id)+" "+str(sec.x_start)+" "+str(sec.y_start)+"\n"
        energy_produced += sec.total_energy
        outstream.write(sec_str)

    # Connections Here
    outstream.write(str(connections)+"\n")
    for sec_id in neighbors.keys():
        for connection in neighbors[sec_id]:
            connection_str = str(sec_id)+" "+str(connection)+"\n"
            outstream.write(connection_str)


    outstream.write(str(len(evs))+"\n")
    for ev in evs:
        ev_str = str(ev.ev_id)+" "+str(ev.sec_id)+" "+\
                 str(ev.release_time)+" "+str(ev.battery_capacity)+" "+\
                 str(ev.num_passengers)+"\n"+str(0)+"\n"
        outstream.write(ev_str)

    outstream.write(str(len(petitions))+"\n")
    for petition in petitions:
        sec_id = 0
        for per in passengers:
            if per.p_id == petition.passenger_id:
                sec_id = per.sec_id
        allocation_status = -1
        p_str = str(petition.petition_id)+ " " +str(sec_id)+" "+str(allocation_status)+"\n"+str(int(petition.time))+" "+\
                str(petition.pickup_x)+ " " +str(petition.pickup_y)+ " " + \
                str(petition.drop_x) + " " +str(petition.drop_y)+" "+str(petition.early_start)+" "+ \
                str(petition.late_start) + " " +str(petition.early_finish)+" "+str(petition.late_finish)+"\n"
        row = [petition.petition_id, (petition.early_finish-petition.early_start),
               instance_level_energy_produced[0], energy_required]
        analysis_data.loc[len(analysis_data)] = row
        outstream.write(p_str)

    # analysis_data.to_excel(excelfile, index=False)


def calculateManhattanDistance(pickup_x, pickup_y, drop_x, drop_y):
    return (abs(pickup_x - drop_x) + abs(pickup_y - drop_y))


def assignRealWorldConstraints(time_horizon, grid_size, num_sec, num_ev,
                      trip_rate, num_passengers, sys_energy, flexiblity,
                               block_size, distances, mode, ev_factor, total_evs, connections):
    print('Generating '+str(mode)+'_'+str(num_sec)+'_SEC_'+str(sys_energy)+'_ENERGY_'+\
                    str(ev_factor)+'_EV-FACTOR_'+str(total_evs)+'_EV_'+\
          str(flexiblity)+'_FLEX_'+str(num_passengers)+"_TPS_"+str(connections)+"_CONNECTIONS.txt")
    secs = []
    evs = []
    passengers = []
    petitions = []
    total_ev = 1
    total_petitions = num_passengers
    time_per_block = 1
    energy_required = 0
    pick_up_x, pick_up_y, drop_x, drop_y = 0, 0, 0, 0
    time = 0
    communities, neighbors = compute_neighbors.divide_and_compute_neighbors(grid_size, num_sec, connections)
    num_sec = len(communities)
    print(communities)
    print(neighbors)

    for i in range(num_passengers):
        p_id = i + 1
        sec_id = r.randint(0, num_sec-1)
        petition_id = i+1
        time =  int(trip_rate[i])
        pickup_x = communities[sec_id][0][0]
        pickup_y =communities[sec_id][0][1]
        distance = int(distances[i])
        tmp_x =  r.randint(0, distance)
        drop_x =  pickup_x + tmp_x
        if drop_x >= grid_size:
            drop_x = pickup_x - tmp_x
        tmp_y =  r.randint(0, (distance-tmp_x))
        drop_y = pickup_y + tmp_y
        if drop_y > grid_size:
            drop_y = pickup_y - tmp_y
        travel_time = distance * time_per_block
        energy_required += travel_time
        early_start = time + int((flexiblity/100) * trip_rate[num_passengers-1])
        late_start = early_start + int((flexiblity/100) * trip_rate[num_passengers-1])
        early_finish = early_start + travel_time
        late_finish = late_start + travel_time
        if late_finish > time_horizon:
            time_horizon = late_finish
        passengers.append(modal.Passenger(p_id, sec_id))
        petitions.append(modal.Trip_petition(petition_id, p_id, time,
                                             pickup_x, pickup_y, drop_x,
                                             drop_y, early_start,
                                             early_finish, late_start,
                                             late_finish, travel_time))
    energy_gen_time = time
    instance_level_energy_produced = 0

    for i in range(num_sec):
        sec_id = i + 1
        x_start = communities[i][0][0]
        y_start = communities[i][0][1]
        x_end = communities[i][1][0]
        y_end = communities[i][1][0]
        charge = 0
        energy_dis = distributions.generateWeibullDis(energy_gen_time, sys_energy,
                                                          energy_required, num_sec)

        total_energy_produced = 0
        for item in energy_dis:
            total_energy_produced += item
        secs.append(modal.Sec(sec_id, 1, x_start, y_start,
                              x_end, y_end, charge, total_energy_produced))
        instance_level_energy_produced += total_energy_produced

        for j in range(num_ev[i]):
            battery_capacity = 100
            ev_id = total_ev
            capacity = 4
            # Energy requirement for trip petitions is calculated using the metric
            charge_per_block = 1

            # Computing release time
            is_released = False
            total_energy = 0
            if mode == 'SPREAD':
                for i in range(len(energy_dis)):
                    if energy_dis[i] != -1:
                        total_energy += energy_dis[i]
                        energy_dis[i] = -1
                    if total_energy > battery_capacity:
                        release_time = i+1
                        is_released = True
                        break
            else:
                if total_energy_produced >= battery_capacity:
                    is_released = True
                    release_time = 0
                    total_energy_produced -= battery_capacity

            if is_released is False:
                release_time = -1
            evs.append(modal.Ev(sec_id, battery_capacity, ev_id,
                                capacity, charge_per_block, release_time))
            total_ev += 1
    writeToFile(time_horizon, grid_size, secs, evs, passengers, petitions,energy_required,
                flexiblity, sys_energy, mode, ev_factor, total_evs, instance_level_energy_produced,connections,
                neighbors)


def parseRealData(mode):
    valid_file = False
    data = []
    ny_zone_data = {}
    with open("taxi_zones_ny.txt") as f:
        for line in f:
            (k, v) = line.split(':')
            ny_zone_data[int(k)] = v
    while not valid_file:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir="./real_world_dataset_nyc_2018/", title="Input Data set",
                                              filetypes=[("Excel files","*.xlsx"), ("CSV files", "*.csv")])
        print(filename)
        file = filename.split("/")[-1].split(".")[0]
        file_type = filename.split("/")[-1].split(".")[1]
        if file_type == "csv":
            data = pd.read_csv(filename, delimiter=';', lineterminator='\n')
            valid_file = True
            break
        else:
            data = pd.read_excel(filename)
            valid_file = True
            break
    keys = ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID', 'trip_distance']
    data = data.filter(items=keys)
    data['pickup'] = pd.to_datetime(data['lpep_pickup_datetime'], format='%m/%d/%Y   %H:%M:%S %p')
    data = data.drop(['lpep_pickup_datetime'], axis=1)
    data = data.set_index(pd.DatetimeIndex(data['pickup']), drop=True)
    data = data[~data.index.duplicated()]
    data = data.dropna()
    index_date = pd.date_range('2018-01-01', periods=len(data.index), freq="1S")
    parsed_data = pd.DataFrame(data, index=index_date)
    parsed_data = parsed_data.dropna()
    n_hours = 3
    start_time = datetime.datetime.strptime(input('specify time in HHMM format: '), "%H%M")
    end_time = start_time + datetime.timedelta(hours = n_hours)
    block_size = 1


    for sec in constraints['secs']:
        for tp in constraints['tps']:
            for ev_factor in constraints['evs']:
                for flexiblity in constraints['flexiblity']:
                    for sys_energy in constraints['sys_energy']:
                        for connections in constraints['connections']:
                            grid_size = 1000
                            raw_petitions = parsed_data.head(tp)
                            raw_petitions = raw_petitions.reset_index(drop=False)
                            num_sec = sec
                            num_passengers = len(raw_petitions.index)
                            total_distance = 0
                            trip_rate = []
                            distances = []
                            for i, row in raw_petitions.iterrows():
                                diff = datetime.datetime.combine(datetime.date.today(), row['pickup'].time()) - \
                                       datetime.datetime.combine(datetime.date.today(), start_time.time())
                                trip_rate.append(diff.total_seconds() - 3600)
                                if row['trip_distance'] == 0:
                                    distances.append(4)
                                    total_distance += 4
                                else:
                                    distances.append(math.ceil(row['trip_distance']))
                                    total_distance += math.ceil(row['trip_distance'])
                            time_horizon = int(trip_rate[num_passengers-1])
                            total_charge_rate = total_distance * ev_factor
                            battery_capacity = grid_size
                            num_ev = int(total_charge_rate/battery_capacity)
                            ev_rate = int(num_ev/num_sec)
                            if ev_rate == 0:
                                ev_rate = 1
                            evs = {}
                            for i in range(num_sec):
                                evs[i] = ev_rate
                            assignRealWorldConstraints(time_horizon, grid_size, num_sec, evs, trip_rate,
                                                       num_passengers, sys_energy, flexiblity,
                                                       block_size, distances, mode, ev_factor, num_ev, connections)

def main():
        # modes = ['START', 'SPREAD']
        modes = ['SPREAD']
        for dispatch_mode in modes:
            parseRealData(dispatch_mode)


if __name__ == '__main__':
    main()
