import json
import numpy as np
import matplotlib.pyplot as plt
import os
from math import atan2, degrees

def process_data(label_dir, gps_imu_dir):
    distances = {}
    angles = {}
    label_files = sorted([f for f in os.listdir(label_dir) if f.endswith('.json')])
    gps_imu_files = sorted([f for f in os.listdir(gps_imu_dir) if f.endswith('.txt')])

    if not label_files or not gps_imu_files:
        print("No label or GPS/IMU data files found.")
        return {}, {}

    for i, label_file in enumerate(label_files):
        gps_imu_file = gps_imu_files[i]
        label_path = os.path.join(label_dir, label_file)
        gps_imu_path = os.path.join(gps_imu_dir, gps_imu_file)

        try:
            with open(gps_imu_path, 'r') as f:
                lines = f.readlines()
                latitude = float(lines[0].strip())
                longitude = float(lines[1].strip())
                latitude = convert_to_decimal_degrees(latitude)
                longitude = convert_to_decimal_degrees(longitude)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error with GPS/IMU file {gps_imu_path}: {str(e)}")
            continue

        try:
            with open(label_path, 'r') as f:
                label_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error with label file {label_path}: {str(e)}")
            continue

        for obj in label_data:
            obj_id = obj.get('obj_id')
            if not obj_id:
                continue
            x = obj['psr']['position']['x']
            y = obj['psr']['position']['y']
            distance = np.sqrt(x**2 + y**2)
            angle = calculate_angle(x, y)
            if obj_id not in distances:
                distances[obj_id] = []
                angles[obj_id] = []
            distances[obj_id].append(distance)
            angles[obj_id].append(angle)

    return distances, angles

def convert_to_decimal_degrees(coordinate):
    degrees = int(coordinate / 100)
    minutes = coordinate - (degrees * 100)
    return degrees + (minutes / 60)

def calculate_angle(x, y):
    angle_radians = atan2(y, x)
    angle_degrees = degrees(angle_radians)
    return angle_degrees

def detect_collisions(distances, collision_threshold=2.0):
    collision_warnings = {}
    max_time_steps = max(len(dist_list) for dist_list in distances.values())
    
    for time_step in range(max_time_steps):
        collisions = []
        for obj_id, distance_list in distances.items():
            if time_step < len(distance_list) and distance_list[time_step] <= collision_threshold:
                collisions.append(obj_id)
        if collisions:
            collision_warnings[time_step] = collisions
    return collision_warnings

def plot_data(distances, angles, collision_warnings):
    if not distances or not angles:
        print("No data to plot.")
        return

    max_time_points = max(len(distance_list) for distance_list in distances.values())
    time = range(max_time_points)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Object Distances and Angles Over Time')

    # Plot distances
    for obj_id, distance_list in distances.items():
        ax1.plot(range(len(distance_list)), distance_list, label=f'Object {obj_id}')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Distance (meters)')
    ax1.grid(True)

    # Highlight collision warnings on distance plot
    for t, objects in collision_warnings.items():
        for obj in objects:
            if t < len(distances[obj]):
                ax1.plot(t, distances[obj][t], 'ro', markersize=10)

    # Plot angles
    for obj_id, angle_list in angles.items():
        ax2.plot(range(len(angle_list)), angle_list, label=f'Object {obj_id}')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Angle (degrees)')
    ax2.grid(True)

    # Add a single legend below both subplots
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, 0))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Make room for the legend
    plt.show()

if __name__ == "__main__":
    label_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\label'
    gps_imu_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\Gps_Imu\data'

    distances, angles = process_data(label_directory, gps_imu_directory)
    
    if not distances or not angles:
        print("No data to process. Exiting.")
    else:
        # Detect collisions
        collision_threshold = 2.0  # meters
        collision_warnings = detect_collisions(distances, collision_threshold)

        # Print collision warnings
        if collision_warnings:
            print("Collision Warnings:")
            for time, objects in collision_warnings.items():
                print(f"Time {time}: Potential collision with objects {', '.join(objects)}")
        else:
            print("No collision warnings detected.")

        # Plot the data with collision warnings
        plot_data(distances, angles, collision_warnings)
