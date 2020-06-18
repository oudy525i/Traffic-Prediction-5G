import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

# Import the .mat files
import_mat = sio.loadmat('coordinate_BS.mat')
import_traces = sio.loadmat('traces.mat')

# Extract .mat file coordinates and data
bs_coordinates = import_mat['BSCoordinates']
traces = import_traces['traces_data']

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
for i in range(1000):
    # Extract temporal vector containing all parameters
    tmp = traces[traces[:, 1] == ID_vec[i]]
    # Append only position parameter to the vehicle_trace list
    vehicle_trace.append(tmp[:, 2:4])
    print(f'Loaded Vehicle-{i}')

print('ALL VEHICLES TRACE LOADED')
# Test plotting some vehicle movement trace
plt.figure(1)

#test importing and plotting background image
#background = plt.imread('background.png')
#plt.imshow(background)

# Plot Base-Stations
plt.scatter(bs_coordinates[:, 0], bs_coordinates[:, 1], marker='s', s=5)

#Plot vehicle-traces
for g in range(1000):
    plt.scatter(vehicle_trace[g][:, 0], vehicle_trace[g][:, 1], s=1)
    print(f'Loaded Vehicle-{g} - TRACE ON MAP')

plt.show()
