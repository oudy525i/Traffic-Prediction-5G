import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import scipy.io as sio
import csv

from matplotlib.patches import RegularPolygon


# Function that import the .mat dataset and convert to pandas dataframe
def get_data():
    # Import the .mat files
    import_mat = sio.loadmat('coordinate_BS.mat')
    import_traces = sio.loadmat('traces.mat')

    # Convert extracted data into pandas Dataframe adding header
    bs_coordinates = pd.DataFrame(import_mat['BSCoordinates'], columns=['x', 'y'])
    vehicle_traces = pd.DataFrame(import_traces['traces_data'], columns=['time', 'id', 'x', 'y', 'speed', 'C', 'C+1', 'C-1', 'C-2', 'C-3'])

    return bs_coordinates, vehicle_traces
# Function that extract all time-steps
def compute_uniq_times(vehicle_traces):
    # Extract unique timings
    uniq_times = np.unique(vehicle_traces['time'])
    return uniq_times
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
# Function that extract mini-batch for the time in input
def extract_time_batch(vehicle_traces, time):
    time_batch = vehicle_traces[vehicle_traces['time'] == time]
    return time_batch

#gets list of num car connected at every BS at time x
def BS_get_Ncar_by_time(trace, curtime):
    ncar_per_BS = []
    time_batch = extract_time_batch(trace, curtime)
    for i in range(0, 225): #0-224 BS
        bs_batch = time_batch[time_batch['C'] == i]
        ncar_per_BS.append(bs_batch['C'].size)
    return ncar_per_BS


bs_coordinates, traces = get_data()
# Get every time-step -> from 3845 to 86308 -> about 22.9 hours
times = compute_uniq_times(traces)






fig, ax = plt.subplots()
plt.subplots_adjust(left=0.20, bottom=0.25)
# Plot Base-Stations
ax.set_aspect('equal')
hexagonal = plt.scatter(bs_coordinates['x'], bs_coordinates['y'], alpha=0)
#-----------------settings colorscale
cmap = plt.get_cmap('viridis')
auto_per_BS = 10
#-----------------
curtime = 3845
ncar_per_Bs = BS_get_Ncar_by_time(traces, curtime)
for x, y, ncar in zip(bs_coordinates['x'], bs_coordinates['y'], ncar_per_Bs):
    curr_color = cmap(ncar/auto_per_BS)
    hex = RegularPolygon((x, y), numVertices=6, radius=40,
                         orientation=np.radians(30),
                         facecolor=curr_color, edgecolor='k')
    ax.add_patch(hex)
ax.margins(x=0)

#-----------------------------------------------------------------------------SLIDER
ft_g, nv_g = vehicle_count(traces, times, step=100, save=False)
axTime = plt.axes([0.2, 0.1, 0.65, 0.06])
sTime = Slider(axTime, 'Time', ft_g[0], ft_g[-1], valstep=100)
p, = plt.plot(ft_g, nv_g, linewidth=2, color='red')

#-----------------------------------------------------------------------------RELOAD PLOT
def update(val):
    curtime = sTime.val
    [p.remove() for p in reversed(ax.patches)]
    ncar_per_Bs = BS_get_Ncar_by_time(traces, curtime)
    for x, y, ncar in zip(bs_coordinates['x'], bs_coordinates['y'], ncar_per_Bs):
        curr_color = cmap(ncar / auto_per_BS)
        hex = RegularPolygon((x, y), numVertices=6, radius=40,
                             orientation=np.radians(30),
                             facecolor=curr_color, edgecolor='k')
        ax.add_patch(hex)
    fig.canvas.draw_idle()


sTime.on_changed(update)
plt.show()
























# fig_BS_load, ax = plt.subplots(2,1)
# plt.subplots_adjust(left=0.1, bottom=0.4)
#
# # Import the .mat files
# import_mat = sio.loadmat('coordinate_BS.mat')
# import_traces = sio.loadmat('traces.mat')
# # Extract .mat file coordinates and data
# bs_coordinates = import_mat['BSCoordinates']
# traces = import_traces['traces_data']
# # Plot Base-Stations
# ax.set_aspect('equal')
# hexagonal = plt.scatter(bs_coordinates[:, 0], bs_coordinates[:, 1], alpha=0)
# for x, y in zip(bs_coordinates[:, 0], bs_coordinates[:, 1]):
#     color = "orange"
#     hex = RegularPolygon((x, y), numVertices=6, radius=40,
#                          orientation=np.radians(30),
#                          facecolor=color, alpha=0.2, edgecolor='k')
#     ax.add_patch(hex)
#
#
#
#
# def val_update(val):
#  [p.remove() for p in reversed(ax.patches)]
#  ax.set_aspect('equal')
#  plt.scatter(bs_coordinates[:, 0], bs_coordinates[:, 1], alpha=1)
#  for x, y in zip(bs_coordinates[:, 0], bs_coordinates[:, 1]):
#      color = "red"
#      hex = RegularPolygon((x, y), numVertices=6, radius=40,
#                           orientation=np.radians(30),
#                           facecolor=color, alpha=0.2, edgecolor='k')
#      ax.add_patch(hex)
#
# AXtimeslider = plt.axes([0.1, 0.2, 0.8, 0.05])
# timeslider = Slider(AXtimeslider, 'Time s', 0, 9000, color='yellow')

#bs_coordinates, traces = get_data()
#times = compute_uniq_times(traces)
#ft_g, nv_g = vehicle_count(traces, times, step=1000, save=False)
#AXtimeslider = plt.axes([0.1, 0.2, 0.8, 0.05])
#timeslider = Slider(AXtimeslider, 'Time s', ft_g[0], ft_g[-1], color='yellow')
#p, = plt.plot(ft_g, nv_g, linewidth=2, color='red')

#timeslider.on_changed(val_update)


#plt.show()












# fig_BS_load, ax = plt.subplots()
# plt.subplots_adjust(left=0.1, bottom=0.5)
#
# bs_coordinates, traces = get_data()
# times = compute_uniq_times(traces)
# ft_g, nv_g = vehicle_count(traces, times, step=1000, save=False)
# p, = plt.plot(ft_g, nv_g, linewidth=2)
# plt.xlim(ft_g[0], ft_g[-1])
# plt.title('Traced Vehicle over Time')
# plt.ylabel('Number of Vehicles')
# plt.xlabel('Time [s]')
#
# axSlider1 = plt.axes([0.1, 0.4, 0.8, 0.05])
# slder1 = Slider(axSlider1, 'Time', valmin=ft_g[0], valmax=ft_g[-1])
#
# plt.show()