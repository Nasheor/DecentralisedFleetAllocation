import pandas as pd

def get_metropolis_column_names():
    metropolis_env = {
        'num_sec':16,
        'num_ev': 400,
    }
    metropolis_column_names = ['File Name','Episodes', 'Trips Satisfied(TS)', 'Total Trips', 'Total Energy Consumed', 'Total Connections','Requests Per Community', 'Connections Per Community']
    for x in range(1, metropolis_env['num_sec']+1):
        metropolis_column_names.append('sec-'+str(x)+' Trips')
        metropolis_column_names.append('sec-'+str(x)+' EVs')
        metropolis_column_names.append('sec-'+str(x)+' Neighbors')
    return metropolis_column_names

def get_nyc_column_names():
    nyc_env = {
        'num_sec': 256,
        'num_ev': 1536
    }
    nyc_column_names = ['File Name','Episodes', 'Trips Satisfied',
                        'Total Trips', 'Total Energy Consumed', 'Total Connections',
                        'Requests Per Community', 'Connections Per Community']
    for x in range(1, nyc_env['num_sec']+1):
        nyc_column_names.append('sec-'+str(x)+' Trips')
        nyc_column_names.append('sec-'+str(x)+' EVs')
        nyc_column_names.append('sec-'+str(x)+' Neighbors')

    return nyc_column_names

def create_csv_file(file, dataset):
    if dataset == 'metropolis':
        columns = get_metropolis_column_names()
        df = pd.DataFrame(columns=columns)

        # Write the DataFrame to an Excel file
        df.to_excel(file, index=False)
        return {key: [] for key in columns}
    else:
        columns = get_nyc_column_names()
        df = pd.DataFrame(columns=get_nyc_column_names())
        # Write the DataFrame to an Excel file
        df.to_excel(file, index=False)
        return {key: [] for key in columns}
