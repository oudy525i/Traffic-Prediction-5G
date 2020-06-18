# Import scientific computation lib
import numpy as np
import pandas as pd

# Import I/O and data management lib
import scipy.io as sio
import csv

# Import Plotting lib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.patches import RegularPolygon



# Import the .mat dataset and convert to pandas dataframe
def get_data():
    # Import the .mat files
    import_mat = sio.loadmat('coordinate_BS.mat')
    import_traces = sio.loadmat('traces.mat')

    # Convert extracted data into pandas Dataframe adding header
    bs_coordinates = pd.DataFrame(import_mat['BSCoordinates'], columns=['x', 'y'])
    vehicle_traces = pd.DataFrame(import_traces['traces_data'], columns=['time', 'id', 'x', 'y', 'speed', 'C', 'C+1', 'C-1', 'C-2', 'C-3'])
    return bs_coordinates, vehicle_traces


# Extract unique vehicle ID
def compute_uniq_id(vehicle_traces):
    # Extract and get unique vehicleID
    uniq_id = np.unique(vehicle_traces['id'])
    return uniq_id


# Extract all time-steps
def compute_uniq_times(vehicle_traces):
    # Extract unique timings
    uniq_times = np.unique(vehicle_traces['time'])
    return uniq_times


# Extract mini-batch for the time in input
def extract_time_batch(vehicle_traces, time):
    time_batch = vehicle_traces[vehicle_traces['time'] == time]
    return time_batch


# Assign random colors to each vehicle -> return a dict
def assign_colors(ID):
    color_dict = {}
    # Just random pick colors for each vehicle
    # Could be very similar, or identical color
    for n in ID:
        color_dict[n] = np.random.rand(1, 3)
    return color_dict


# Count number of traced vehicles per time-step
def vehicle_count(v_trace, times, step, save=False):
    v_count = []
    tmp_time = []
    tmp_vehi = []

    for time in range(0, len(times), step):
        tmp = []
        time_batch = extract_time_batch(v_trace, times[time])

        if save:
            # Append time data and number of vehicle
            tmp.append(int(times[time]))
            tmp.append(len(time_batch))
            # Append tmp=['time', '# vehicle'] to initial dataset
            v_count.append(tmp)
        else:
            tmp_time.append(int(times[time]))
            tmp_vehi.append(len(time_batch))

    if save:
        with open('Vehicle_count.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(v_count)

    return tmp_time, tmp_vehi


# Count number of vehicle in selected BS per time-step
def BS_vehicle_counter(trace, timess, step, BSID, save=False):
    v_count = []
    tmp_time = []
    tmp_vehi = []

    # Filter by only selected bs-number
    bs_batch = trace[trace['C'] == BSID]

    for time in range(0, len(timess), step):
        tmp = []
        time_batch = extract_time_batch(bs_batch, timess[time])

        if save:
            # Append time data and number of vehicle
            tmp.append(int(timess[time]))
            tmp.append(len(time_batch))
            # Append tmp=['time', '# vehicle'] to initial dataset
            v_count.append(tmp)
        else:
            tmp_time.append(int(timess[time]))
            tmp_vehi.append(len(time_batch))

    if save:
        with open(f'BS_{BSID}_{step}_count.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(v_count)

    return tmp_time, tmp_vehi


# Read vehicle counts from csv File
def import_counts(file_path):
    tmp_time = []
    tmp_vehi = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for elem in reader:
            tmp_time.append(int(elem[0]))
            tmp_vehi.append(int(elem[1]))

    return tmp_time, tmp_vehi


# Vehicle animation plot function
def vehicle_animation_test(bs_coordinates, times, traces, color_dict):
    plt.figure(1)

    # Plot Base stations
    plt.scatter(bs_coordinates['x'], bs_coordinates['y'], s=10, marker='s', alpha=0.5)
    plt.show(block=False)
    # LOOP BY TIME-STEP
    for time in times:
        time_batch = extract_time_batch(traces, time)
        print(f'Time-{time}')

        # Extract and all vehitcle positions in the time-step
        points_list = []
        for index, vehicle in time_batch.iterrows():
            points = plt.scatter(float(vehicle['x']), float(vehicle['y']), s=50, marker='.', c=color_dict[vehicle['id']])
            points_list.append(points)

        # Draw all vhicle positions
        plt.draw()
        # Delay
        plt.pause(0.00000001)
        # Delete all vehicle positions
        for p2 in points_list:
            p2.remove()
    return


# Plot BS positions + BS label
def show_bs(bs_coordinates):
    plt.figure(1)

    # Plot Base stations
    plt.scatter(bs_coordinates['x'], bs_coordinates['y'], s=20, marker='s', alpha=0.5)

    # Point annotation function
    for i in range(len(bs_coordinates)):
        plt.annotate(f'BS-{i+1}', (bs_coordinates['x'][i], bs_coordinates['y'][i]))
    plt.show()
    return


# Gets list of number of car connected at every BS at time x
def BS_get_Ncar_by_time(trace, curtime):
    ncar_per_BS = []
    time_batch = extract_time_batch(trace, curtime)
    for i in range(1, 226): #0-224 BS
        bs_batch = time_batch[time_batch['C'] == i]
        ncar_per_BS.append(bs_batch['C'].size)
    return ncar_per_BS

#Gets array where cols are[ID, x position, y position] by input time
def get_car_pos_by_time(trace, curtime):
    time_batch = extract_time_batch(trace, curtime)
    carID = time_batch['id']
    carX = time_batch['x']
    carY = time_batch['y']
    car_position = np.zeros((carY.size, 3))
    i = 0
    for curID, posx, posy, in zip(carID, carX, carY):
        car_position[i, 0] = curID
        car_position[i, 1] = posx
        car_position[i, 2] = posy
        i += 1
    return car_position
