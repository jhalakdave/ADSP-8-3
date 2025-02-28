import json
import numpy as np
import matplotlib.pyplot as plt
import os
from math import atan2, degrees

def process_data(label_dir, gps_imu_dir):


    distances = {}  # Store distances for each object over time
    angles = {}     # Store angles for each object over time

    # Get sorted lists of label and GPS/IMU files
    label_files = sorted([f for f in os.listdir(label_dir) if f.endswith('.json')])
    gps_imu_files = sorted([f for f in os.listdir(gps_imu_dir) if f.endswith('.txt')])

    if not label_files or not gps_imu_files:
        print("No label or GPS/IMU data files found.")
        return [], []

    # Iterate through the label files (assuming each corresponds to a GPS/IMU file)
    for i, label_file in enumerate(label_files):
        gps_imu_file = gps_imu_files[i]

        # Construct full file paths
        label_path = os.path.join(label_dir, label_file)
        gps_imu_path = os.path.join(gps_imu_dir, gps_imu_file)

        # Read GPS/IMU data (car's position)
        try:
            with open(gps_imu_path, 'r') as f:
                lines = f.readlines()
                latitude = float(lines[0].strip())
                longitude = float(lines[1].strip())

                # Convert latitude and longitude to decimal degrees (if needed)
                latitude = convert_to_decimal_degrees(latitude)
                longitude = convert_to_decimal_degrees(longitude)

        except FileNotFoundError:
            print(f"GPS/IMU file not found: {gps_imu_path}")
            continue  # Skip to the next label file
        except ValueError:
            print(f"Error reading GPS/IMU data from: {gps_imu_path}")
            continue

        # Read object labels
        try:
            with open(label_path, 'r') as f:
                label_data = json.load(f)
        except FileNotFoundError:
            print(f"Label file not found: {label_path}")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding JSON from: {label_path}")
            continue

        # Process each object in the label file
        for obj in label_data:
            obj_id = obj.get('obj_id')
            if not obj_id:
                print("Object ID not found, skipping object")
                continue

            x = obj['psr']['position']['x']
            y = obj['psr']['position']['y']

            # Calculate distance and angle
            distance = np.sqrt(x**2 + y**2)
            angle = calculate_angle(x, y)  # Angle relative to the car

            # Store the data
            if obj_id not in distances:
                distances[obj_id] = []
                angles[obj_id] = []

            distances[obj_id].append(distance)
            angles[obj_id].append(angle)

    return distances, angles

def convert_to_decimal_degrees(coordinate):
    """
    Convert coordinate from ddmm.mmmm format to decimal degrees.

    Args:
        coordinate (float): Coordinate in ddmm.mmmm format.

    Returns:
        float: Coordinate in decimal degrees.
    """
    degrees = int(coordinate / 100)
    minutes = coordinate - (degrees * 100)
    return degrees + (minutes / 60)

def calculate_angle(x, y):
    """
    Calculates the angle of an object relative to the car's forward direction.

    Args:
        x (float): X-coordinate of the object.
        y (float): Y-coordinate of the object.

    Returns:
        float: Angle in degrees.
    """
    angle_radians = atan2(y, x)
    angle_degrees = degrees(angle_radians)
    return angle_degrees

def plot_representative_data(distances, angles):
    """Plots representative distance and angle trends."""

    # Define representative object IDs for distance trends
    distance_trend_objects = {
        'Approaching': '1',  # Example: Object approaching the car
        'Moving Away': '2',  # Example: Object moving away from the car
        'Non-Linear (Approach then Away)': '31',  # Example: Object approaching then moving away
        'Non-Linear (Away then Approach)': '34'  # Example: Object moving away then approaching
    }

    # Define representative object IDs for angle trends
    angle_trend_objects = {
        'Increasing Angle': '1',  # Example: Object moving to the right
        'Decreasing Angle': '22',  # Example: Object moving to the left
        'Towards Center': '34',  # Example: Object angle becoming close to 0
        'From Center': '3', #object angle becoming far from 0
    }

    # Line styles for better distinction
    line_styles = ['-', '--', ':', '-.']

    # Number of time points to plot
    num_time_points = min(len(distance_list) for distance_list in distances.values())
    time = range(num_time_points)

    # Create Distance Trend Plot
    plt.figure(figsize=(12, 6))
    plt.title('Representative Distance Trends')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Distance (meters)')
    for i, (trend, obj_id) in enumerate(distance_trend_objects.items()):
        if obj_id in distances:
            plt.plot(time, distances[obj_id][:num_time_points], label=f'{trend} (Object {obj_id})', linestyle=line_styles[i % len(line_styles)])
    plt.legend()
    plt.grid(True)
    plt.show()

    # Create Angle Trend Plot
    plt.figure(figsize=(12, 6))
    plt.title('Representative Angle Trends')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle (degrees)')
    for i, (trend, obj_id) in enumerate(angle_trend_objects.items()):
        if obj_id in angles:
            plt.plot(time, angles[obj_id][:num_time_points], label=f'{trend} (Object {obj_id})', linestyle=line_styles[i % len(line_styles)])
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Create Distance Trend with corresponding Angle Plot
    plt.figure(figsize=(12, 6))
    plt.title('Distance trends with corresponding angles')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle (degrees)')
    for i, (trend, obj_id) in enumerate(distance_trend_objects.items()):
        if obj_id in angles:
            plt.plot(time, angles[obj_id][:num_time_points], label=f'{trend} (Object {obj_id})', linestyle=line_styles[i % len(line_styles)])
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Create Angle Trend with corresponding Distance Plot
    plt.figure(figsize=(12, 6))
    plt.title('Angle trend with corresponding Distance')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Distance (meters)')
    for i, (trend, obj_id) in enumerate(angle_trend_objects.items()):
        if obj_id in distances:
            plt.plot(time, distances[obj_id][:num_time_points], label=f'{trend} (Object {obj_id})', linestyle=line_styles[i % len(line_styles)])
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Specify the directories where your data is stored
    label_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\label'  # Replace with the actual path to your label files
    gps_imu_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\Gps_Imu\data'  # Replace with the actual path to your GPS/IMU files

    # Process the data
    distances, angles = process_data(label_directory, gps_imu_directory)

    # Plot the representative data
    plot_representative_data(distances, angles)
