import pandas as pd
import glob
import os

# -----------------------------
# Folder containing CSV files
# -----------------------------
FOLDER = r"C:/Users/KIIT/Downloads/Assignment 2/temperatures"
OUTPUT_DIR = FOLDER  # Save output files in the same folder

# -----------------------------
# Step 1: Read all CSVs and reshape data
# -----------------------------
all_files = glob.glob(os.path.join(FOLDER, "*.csv"))
if not all_files:
    raise FileNotFoundError(f"No CSV files found in {FOLDER}")

df_list = []
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

for f in all_files:
    temp_df = pd.read_csv(f)
    # Extract year from filename, e.g., stations_group_1986.csv → 1986
    year = os.path.basename(f).split("_")[-1].split(".")[0]
    
    # Melt month columns into long format
    melted = temp_df.melt(
        id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
        var_name="month",
        value_name="temperature"
    )
    
    # Convert month names to numbers
    melted["month_num"] = melted["month"].map(month_map)
    
    # Create proper date (first day of the month)
    melted["date"] = pd.to_datetime(
        dict(year=int(year), month=melted["month_num"], day=1),
        errors="coerce"
    )
    
    # Rename station column
    melted = melted.rename(columns={"STATION_NAME": "station"})
    
    # Keep only required columns
    df_list.append(melted[["date", "station", "temperature"]])

# Combine all years into one DataFrame
df = pd.concat(df_list, ignore_index=True)

# -----------------------------
# Step 2: Clean data
# -----------------------------
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df = df.dropna(subset=['temperature', 'date'])

# -----------------------------
# Step 3: Define Australian seasons
# -----------------------------
def get_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"

df['season'] = df['date'].dt.month.map(get_season)

# -----------------------------
# Step 4: Seasonal Average
# -----------------------------
season_order = ["Summer", "Autumn", "Winter", "Spring"]
seasonal_avg = df.groupby('season')['temperature'].mean()

with open(os.path.join(OUTPUT_DIR, "average_temp.txt"), "w") as f:
    for season in season_order:
        if season in seasonal_avg:
            f.write(f"{season}: {seasonal_avg[season]:.1f}°C\n")

# -----------------------------
# Step 5: Temperature Range
# -----------------------------
station_stats = df.groupby('station')['temperature'].agg(['max', 'min'])
station_stats['range'] = station_stats['max'] - station_stats['min']

max_range = station_stats['range'].max()
largest_range_stations = station_stats[station_stats['range'] == max_range]

with open(os.path.join(OUTPUT_DIR, "largest_temp_range_station.txt"), "w") as f:
    for station, row in largest_range_stations.iterrows():
        f.write(
            f"{station}: Range {row['range']:.1f}°C "
            f"(Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n"
        )

# -----------------------------
# Step 6: Temperature Stability (Std Dev)
# -----------------------------
station_std = df.groupby('station')['temperature'].std().dropna()

min_std = station_std.min()
max_std = station_std.max()

stable_stations = station_std[station_std == min_std]
variable_stations = station_std[station_std == max_std]

with open(os.path.join(OUTPUT_DIR, "temperature_stability_stations.txt"), "w") as f:
    for station, val in stable_stations.items():
        f.write(f"Most Stable: {station}: StdDev {val:.1f}°C\n")
    for station, val in variable_stations.items():
        f.write(f"Most Variable: {station}: StdDev {val:.1f}°C\n")

print("Analysis complete. Check output files in the folder.")