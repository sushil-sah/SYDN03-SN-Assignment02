import pandas as pd
import glob
import os
from utils import data_Formatter, map_Month_To_Season

# Path to the folder containing input files
input_Folder = './Input/Q2_input/temperatures'

# Path to the folder containing output files
output_Folder = "./Q2_output"

df_list = []

# create a dictonary to map each months to respective numbers
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}


# try catch block to handle folder and file not present exceptions
try:
    # checking if the input folder is presnt or not
    if not os.path.isdir(input_Folder):
        # checking if the folder exists or not. If folder doen't exist an Exception is raised
        raise Exception(f'Input folder {input_Folder} doesn\'t exist')

    # opening all the input files from input folder
    all_files = glob.glob(os.path.join(input_Folder, "*.csv"))

    # checking if the folder has any csv files or not. If no file is present an Exception is raised
    if not all_files:
        raise Exception(f"Input folder {input_Folder} has no csv files")
    
# raising other exceptions that can be thrown by try block
except Exception as e:
    raise e


for file in all_files:
    df_list = data_Formatter(file, month_map, df_list)

# Combining all the records into a single data frame for further analysis
df = pd.concat(df_list, ignore_index=True)


# Cleaning all the NA records from the data frames
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df = df.dropna(subset=['temperature', 'date'])



# mapping months to respective Australian seasons 
df['season'] = df['date'].dt.month.map(map_Month_To_Season)


# Calculating the seasonal average and writing the output into a file
average_file_name = 'average_temp.txt'
season_order = ["Summer", "Autumn", "Winter", "Spring"]
seasonal_avg = df.groupby('season')['temperature'].mean()

with open(os.path.join(output_Folder, average_file_name), "w") as f:
    for season in season_order:
        if season in seasonal_avg:
            f.write(f"{season}: {seasonal_avg[season]:.1f}°C\n")
    print(f'Output has been successfully written into file {average_file_name}')



# Calculating the temperature range and writing the output into a file
temeprature_range_file = 'largest_temp_range_station.txt'

# calculating the max and min temperature for each station
station_stats = df.groupby('STATION_NAME')['temperature'].agg(['max', 'min'])

# calculating the range for each station
station_stats['range'] = station_stats['max'] - station_stats['min']

# determing the station with maximum range
max_range = station_stats['range'].max()
largest_range_stations = station_stats[station_stats['range'] == max_range]

with open(os.path.join(output_Folder, temeprature_range_file), "w") as f:
    for station, row in largest_range_stations.iterrows():
        f.write(
            f"{station}: Range {row['range']:.1f}°C "
            f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
        )

print()
print(f'Output has been successfully written into file {temeprature_range_file}')


#  Calculating the station with high temperature stablity and writing the output into a file
temperature_stability_station_file = 'temperature_stability_stations.txt'
station_std = df.groupby('STATION_NAME')['temperature'].std().dropna()

# calculating the min and max standard deviation
min_std, max_std = station_std.min(), station_std.max() 
stable_stations, variable_stations = station_std[station_std == min_std], station_std[station_std == max_std]

with open(os.path.join(output_Folder, temperature_stability_station_file), "w") as f:
    for station, val in stable_stations.items():
        f.write(f"Most Stable: {station}: StdDev {val:.1f}°C\n")
    for station, val in variable_stations.items():
        f.write(f"Most Variable: {station}: StdDev {val:.1f}°C\n")

print()
print(f'Output has been successfully written into file {temperature_stability_station_file} \n')
print("Analysis complete. Check output files in the folder.")