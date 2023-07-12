import os
import pandas as pd
import datetime

def filename_split_lidartime(folder_path):
    # Initialize lists to store the split filenames
    frame_numbers = []
    gps_sow_values = []
    # Traverse the folder and sort filenames in ascending order
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            # Split the filename into frame number and gps_sow value
            file_parts = filename.split("_")
            frame_number = int(file_parts[0])
            gps_sow = float(file_parts[2].split(".")[0] + "." + file_parts[2].split(".")[1])

            # Append to the respective lists
            frame_numbers.append(frame_number)
            gps_sow_values.append(gps_sow)
    # Create a Pandas DataFrame
    data = {'frame': frame_numbers, 'lidar_sow': gps_sow_values}
    df = pd.DataFrame(data)
    # Sort the DataFrame by the 'frame' column in ascending order
    df_sorted = df.sort_values('frame')
    # Reset the index of the sorted DataFrame
    df_sorted = df_sorted.reset_index(drop=True)

    # Update the 'frame' column to start from 0
    df_sorted['frame'] = df_sorted.index
    return(df_sorted)


def filename_split_gpsweek(filename):
    
    # Extract the filename from the path
    base_filename = os.path.basename(filename)

    # Split the filename into its components using '-' as the delimiter
    filename = base_filename.split('/')[-1]

    # Extract the year, month, and day from the first component
    utctime = filename.split('_')[0]
    
    components = utctime.split('-')
    
    utc_year = int(components[0])
    utc_month = int(components[1])
    utc_day = int(components[2])
        
    # GPS epoch (January 6, 1980) in UTC
    gps_epoch_utc = datetime.datetime(1980, 1, 6, 0, 0, 0)

    # Target UTC time
    target_utc = datetime.datetime(utc_year, utc_month, utc_day, 0, 0, 0)

    # Calculate the time difference between GPS epoch and target UTC time
    time_diff = (target_utc - gps_epoch_utc).total_seconds()

    # Number of seconds in a GPS week
    seconds_per_week = 604800

    # Calculate the GPS week
    gps_week = int(time_diff // seconds_per_week)
    
    return gps_week



