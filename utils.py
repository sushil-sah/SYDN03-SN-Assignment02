# This files will contain all the necessary functions

import pandas as pd
import os

def data_Formatter(file, month_map, df_list):
    temp_df = pd.read_csv(file)
    # Spliting the file_name at '_' so that we can extract year from filename, e.g., for stations_group_1986.csv we can get 1986
    year = os.path.basename(file).split("_")[-1].split(".")[0]
    
    # Unpivot the data to generate columns for each month based on station_name, stn_id, latitude and longitude
    melted = temp_df.melt(
        id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
        var_name="month",
        value_name="temperature"
    )
    
    # mapping the months name to their respective number
    melted["month_num"] = melted["month"].map(month_map)
    
    ''' Converting the month number into proper date format by using the year from the csv file 
    and using 1st day for each month as day '''

    melted["date"] = pd.to_datetime(
        dict(year=int(year), month=melted["month_num"], day=1)
    )
    
    # Removing all the unnecessary columns and keeping only the necessary columns for further processing
    df_list.append(melted[["date", "STATION_NAME", "temperature"]])

    return df_list

# Functions defined to map the months to the Australian seasons
def map_Month_To_Season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"