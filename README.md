# **LiDAR Data Processing and Visualization**

This project processes LiDAR data from a moving car, calculates object distances and angles, detects potential collisions, and generates visualizations.


## **Prerequisites**

- Python 3.x
- Required Python packages:
  - `json` (usually comes with Python)
  - `numpy`
  - `matplotlib`

## **Installation**

1.  **Install Python 3.x:** If you don't have it already, download and install Python from [python.org](https://www.python.org/).

2.  **Install the required Python packages:**
    Open your terminal or command prompt and use `pip` to install the necessary libraries:

    ```
    pip install numpy matplotlib
    ```

## **Usage**

1.  **Clone the repository:**

    ```
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Modify the data directories (if necessary):**

    Open `main_code.py` in a text editor and check the `label_directory` and `gps_imu_directory` variables within the `if __name__ == "__main__":` block.  These variables specify the paths to your LiDAR data.

    ```
    label_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\label'
    gps_imu_directory = r'D:\JHALAKLIDAR\drive_night_rain_2\downtown_sub1\Gps_Imu\data'
    ```

    **Important:** If your data is located in a different directory, **you MUST update these paths** to reflect the correct locations of your `label` and `Gps_Imu/data` folders.  Relative paths (e.g., `"label"` or `"Gps_Imu/data"`) would be relative to the location of the `main_code.py` script.

3.  **Run the script:**

    ```
    python main_code.py
    ```

## **Output**

The script will:

-   Process the LiDAR data from the specified `label` and `Gps_Imu/data` directories.
-   Print any detected collision warnings to the console.
-   Generate a plot showing object distances and angles over time, with collision warnings highlighted.

## **Notes**

-   The script assumes that for each label file (`.json`) in the `label` directory, there is a corresponding GPS/IMU file (`.txt`) in the `Gps_Imu/data` directory.  The files are paired based on their order in the sorted lists of files.

-   The collision detection uses a threshold of 2.0 meters. This value can be adjusted by modifying the `collision_threshold` variable in the `main_code.py` script.

-   The GPS/IMU data files are expected to contain latitude and longitude values on the first two lines, respectively.

-   The label files are expected to be in JSON format and contain object data with `obj_id`, `psr`, `position`, `x`, and `y` keys. Ensure the correct keys exist in JSON for correct execution, the keys being: `obj_id`, `psr`, `position`, `x`, and `y`.
