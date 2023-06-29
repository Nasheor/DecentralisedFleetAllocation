import seaborn
import tkinter as tk
import pandas as pd
from tkinter import filedialog
import json

def parseTaxiZones():
    valid_file = False
    zone_data = []
    trip_data = []

    while not valid_file:
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir="./instances/real_world_dataset", title="Taxi Zone File", filetypes=[("Excel files","*.xlsx"), ("CSV files", "*.csv")])
        file = filename.split("/")[-1].split(".")[0]
        file_type = filename.split("/")[-1].split(".")[1]
        if file_type == "csv":
            zone_data = pd.read_csv(filename, delimiter=';', lineterminator='\n')
            valid_file = True
            break
        elif file_type == "xlsx":
            zone_data = pd.read_excel(filename)
            valid_file = True
            break
        else:
            print("Invalid File Type. Supported file types are .csv and .xlsx")
    keys = ['OBJECTID', 'the_geom']
    zone_data = zone_data.filter(items=keys)
    print(type(zone_data['OBJECTID']))
    dict_zone_data ={}
    # for i in range(len(zone_data['OBJECTID'])):
    #     dict_zone_data[zone_data['OBJECTID'][i]] = zone_data['the_geom'][i]
    dict_zone_data = dict(zip(zone_data['OBJECTID'], zone_data['the_geom']))

    print(dict_zone_data)
    with open("taxi_zones_ny.txt", 'w') as f:
        for key, value in dict_zone_data.items():
            f.write('%s:%s\n' % (key, value))


if __name__ == '__main__':
    parseTaxiZones()