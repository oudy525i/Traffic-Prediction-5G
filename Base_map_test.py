import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import csv


# Function that import the .mat dataset and convert to pandas dataframe
def get_data():
    # Import the .mat files
    import_mat = sio.loadmat('coordinate_BS.mat')
    import_traces = sio.loadmat('traces.mat')

    # Convert extracted data into pandas Dataframe adding header
    bs_coordinates = pd.DataFrame(import_mat['BSCoordinates'], columns=['x', 'y'])
    vehicle_traces = pd.DataFrame(import_traces['traces_data'], columns=['time', 'id', 'x', 'y', 'speed', 'C', 'C+1', 'C-1', 'C-2', 'C-3'])

    return bs_coordinates, vehicle_traces


# Function that extract unique vehicle ID
def compute_uniq_id(vehicle_traces):
    # Extract and get unique vehicleID
    uniq_id = np.unique(vehicle_traces['id'])
    return uniq_id


# Function that extract all time-steps
def compute_uniq_times(vehicle_traces):
    # Extract unique timings
    uniq_times = np.unique(vehicle_traces['time'])
    return uniq_times


# Function that extract mini-batch for the time in input
def extract_time_batch(vehicle_traces, time):
    time_batch = vehicle_traces[vehicle_traces['time'] == time]
    return time_batch



# Old version of dynamic plot (laggy and high refreshrate)
def tmp_plot():
    # Import datasets
    bs_coordinates, traces = get_data()

    # Extract and get unique vehicleID
    vehicle_id = traces[:, 1]
    uniq_id_raw = np.unique(vehicle_id)

    # Initialize unique ID vector
    ID_vec = np.zeros(len(uniq_id_raw), dtype=int)
    N_vehicle = len(ID_vec)
    # Fill unique ID vector
    for x in range(N_vehicle):
        ID_vec[x] = int(uniq_id_raw[x])

    # Initialize list
    vehicle_trace = []
    for i in range(100):
        # Extract temporal vector containing all parameters
        tmp = traces[traces[:, 1] == ID_vec[i]]
        # Append only position parameter to the vehicle_trace list
        vehicle_trace.append(tmp[:, 2:4])
        print(f'Loaded Vehicle-{i}')

    print('ALL VEHICLES TRACE LOADED')
    # Test plotting some vehicle movement trace
    # Plot Base-Stations
    plt.scatter(bs_coordinates[:, 0], bs_coordinates[:, 1])
    plt.show(block=False)
    # Plot vehicle-traces
    for g in range(100):
        plt.scatter(vehicle_trace[g][:, 0], vehicle_trace[g][:, 1], s=1)
        print(f'Loaded Vehicle-{g} - TRACE ON MAP')
        plt.draw()
        plt.pause(0.001)

    plt.show(block=True)
    return


# Function that assign random colors to each vehicle -> return a dict
def assign_colors(ID):
    color_dict = {}
    # Just random pick colors for each vehicle
    # Could be very similar, or identical color
    for n in ID:
        color_dict[n] = np.random.rand(1, 3)
    return color_dict


# Function that count the number of traces vehicles per time-step
def vehicle_count(traces, times, step, save=False):
    v_count = []
    tmp_time = []
    tmp_vehi = []

    for time in range(0, len(times), step):
        tmp = []
        time_batch = extract_time_batch(traces, times[time])

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


# Support function that read vehicle counts from file
def import_counts(file_path):
    tmp_time = []
    tmp_vehi = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for elem in reader:
            tmp_time.append(int(elem[0]))
            tmp_vehi.append(int(elem[1]))

    return tmp_time, tmp_vehi


# Main vehicle animation function
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


# plot BS positions
def show_bs(bs_coordinates):
    plt.figure(1)

    # Plot Base stations
    plt.scatter(bs_coordinates['x'], bs_coordinates['y'], s=20, marker='s', alpha=0.5)

    # Point annotation function
    for i in range(len(bs_coordinates)):
        plt.annotate(f'BS-{i}', (bs_coordinates['x'][i], bs_coordinates['y'][i]))
    plt.show()

    return


if __name__ == "__main__":

    # Import datasets
    # NOT POSSIBLE TO SORT BY TIME BECAUSE THE PROCEDURE WILL FILL THE ENTIRE MEMORY
    bs_coordinates, traces = get_data()

    # Get every time-step -> from 3845 to 86308 -> about 22.9 hours
    times = compute_uniq_times(traces)
    # Get uniq vehicles Id
    ID = compute_uniq_id(traces)
    # Assign random color to each vehicle
    color_dict = assign_colors(ID)
    # Dynamic plot for vehicle animation
    vehicle_animation_test(bs_coordinates, times, traces, color_dict)

    ft_g, nv_g = vehicle_count(traces, times, step=100, save=False)
    ft_1, nv_1 = BS_vehicle_counter(traces, times, step=100, BSID=10)
    ft_2, nv_2 = BS_vehicle_counter(traces, times, step=100, BSID=100)
    plt.figure(1)
    # PLOT total case
    plt.plot(ft_g, nv_g, label='TOTAL')
    # PLOT BS1-vehicles
    plt.plot(ft_1, nv_1, label='BS-100', markersize=1, alpha=0.5)
    # PLOT BS10-vehicles
    plt.plot(ft_2, nv_2, label='BS-10', markersize=1, alpha=0.5)

    # Limit x axes
    plt.xlim(ft_g[0], ft_g[-1])
    plt.legend()
    plt.title('Traced Vehicle over Time')
    plt.ylabel('Number of Vehicles')
    plt.xlabel('Time [s]')
    plt.show()