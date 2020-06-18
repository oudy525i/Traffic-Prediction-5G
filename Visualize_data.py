import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
import scipy.io as sio
import csv
import pickle

from matplotlib.patches import RegularPolygon
import VF as vf


def update_bs_cells(traces, curtime, figurename, bs_position, cmap_scale_color):
    [old_patches.remove() for old_patches in reversed(figurename.patches)]
    cars_per_bs = vf.BS_get_Ncar_by_time(traces, curtime)
    for xbs, ybs, ncarbs in zip(bs_position['x'], bs_position['y'], cars_per_bs):
        color = cmap_scale_color(ncarbs / auto_per_BS)
        hex_patch_apply = RegularPolygon((xbs, ybs), numVertices=6, radius=40,
                                         orientation=np.radians(30),
                                         facecolor=color, edgecolor='k')
        figurename.add_patch(hex_patch_apply)
    fig.canvas.draw_idle()


def update_car_pos(traces, curtime, cur_car_ax, colormap_dict):
    cur_car_ax.clear()
    cur_car_ax.set_xlim(0, 900)
    cur_car_ax.set_ylim(0, 1050)
    cur_car_ax.set_aspect('equal')
    cur_car_ax.imshow(plt.imread('background.png'), origin='lower')
    vehicle_coordinates = vf.get_car_pos_by_time(traces, curtime)
    car_color = np.zeros((vehicle_coordinates[:, 0].size, 3))
    i = 0
    for ids in vehicle_coordinates[:, 0]:
        car_color[i, :] = colormap_dict[ids]
        i += 1
    cur_car_ax.scatter(vehicle_coordinates[:, 1], vehicle_coordinates[:, 2], s=50, marker='.', c=car_color)


# spit traces in hours.
def cut_trace_into_smaller_time(input_traces):
    # time-step -> from 3845 to 86308 -> about 22.9 hours , 82463 sec
    input_traces['x'] = input_traces['x'] - 12700  # Normalize points 12700<x<13600 = 900px
    input_traces['y'] = input_traces['y'] - 13200  # Normalize points 13200<y<14250 = 1050px
    for i in range(0, 23):
        cur_trace = input_traces[
            (3845 + 3600 * i <= input_traces['time']) & (input_traces['time'] < 3845 + 3600 * (+i + 1))]
        cur_trace.to_pickle('data_fast_loading/traces_hour_' + str(i) + '.plk')


# get correct trace
def get_fast_trace(desired_trace_time):
    # time-step -> from 3845 to 86308 -> about 22.9 hours , 82463 sec
    hour = math.floor((desired_trace_time - 3845) / 3600.0)
    return pd.read_pickle('data_fast_loading/traces_hour_' + str(hour) + '.plk')


# fast loading sequence
try:
    bs_coordinates = pd.read_pickle('data_fast_loading/fast_bs_coordinates.plk')
    times = np.load('data_fast_loading/fast_times.npy')
    with open('data_fast_loading/fast_carID_colorDict.plk', 'rb') as handle:
        color_dict = pickle.load(handle)
    ft_g = np.load('data_fast_loading/fast_ft_g.npy')
    nv_g = np.load('data_fast_loading/fast_nv_g.npy')
    pass
except IOError:
    print("Could not read files, slow loading started.")
    bs_coordinates, traces = vf.get_data()
    cut_trace_into_smaller_time(traces)
    bs_coordinates['x'] = bs_coordinates['x'] - 12700  # Normalize points 12700<x<13600 = 900px
    bs_coordinates['y'] = bs_coordinates['y'] - 13200  # Normalize points 13200<y<14250 = 1050px
    bs_coordinates.to_pickle('data_fast_loading/fast_bs_coordinates.plk')
    # Get every time-step -> from 3845 to 86308 -> about 22.9 hours
    times = vf.compute_uniq_times(traces)
    np.save('data_fast_loading/fast_times', times)
    car_ID = vf.compute_uniq_id(traces)
    color_dict = vf.assign_colors(car_ID)
    with open('data_fast_loading/fast_carID_colorDict.plk', 'wb') as handle:
        pickle.dump(color_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    ft_g, nv_g = vf.vehicle_count(traces, times, step=100, save=False)
    np.save('data_fast_loading/fast_ft_g', ft_g)
    np.save('data_fast_loading/fast_nv_g', nv_g)

traces = get_fast_trace(ft_g[0])
prev_traces_time = ft_g[0]
# set up the 3 plots
fig, [ax_cell, ax_car, ax_way] = plt.subplots(1, 3)
plt.subplots_adjust(left=0.10, bottom=0.4)

# -----------------------------------------------------------------------------SLIDER
axTime = plt.axes([0.15, 0.25, 0.70, 0.06])
sTime = Slider(axTime, 'Time[s]', ft_g[0], ft_g[-1], valstep=100)
p, = plt.plot(ft_g, nv_g, linewidth=2, color='red')

# -----------------------------------------------------------------------------TEXT BOX
axbox = plt.axes([0.425, 0.05, 0.05, 0.075])
text_box = TextBox(axbox, label='', initial=str(ft_g[0]))

# ------------------------------------------------------------------------------NEXT BUTTON

axnext = plt.axes([0.3, 0.05, 0.1, 0.075])
bnext = Button(axnext, '+1 sec')

# ------------------------------------------------------------------------------PREV BUTTON
axprev = plt.axes([0.5, 0.05, 0.1, 0.075])
bprev = Button(axprev, '-1 sec')

# -------------------------------------------------------------------------------------------Plot Base-Stations cells
colormap_scale = plt.get_cmap('viridis')  # settings colorscale
auto_per_BS = 10  # max number of car per cell, if bigger->saturation
# -----------------
ax_cell.set_aspect('equal')
ax_cell.set_xlim(0, 900)
ax_cell.set_ylim(0, 1050)
ax_cell.scatter(bs_coordinates['x'], bs_coordinates['y'], alpha=0)
# plot base station for the first time
update_bs_cells(traces, ft_g[0], ax_cell, bs_coordinates, colormap_scale)
ax_cell.margins(x=0)

# -------------------------------------------------------------------------------------------Plot Car by time
update_car_pos(traces, ft_g[0], ax_car, color_dict)
# ax_car.scatter(bs_coordinates['x'], bs_coordinates['y'], marker='s', s=5)  # Plot Base-Stations


# -------------------------------------------------------------------------------------------Plot Street
ax_way.set_aspect('equal')
ax_way.set_xlim(0, 900)
ax_way.set_ylim(0, 1050)
ax_way.imshow(plt.imread('background.png'), origin='lower')
ax_way.scatter(bs_coordinates['x'], bs_coordinates['y'], marker='s', s=5)  # Plot Base-Stations


# -----------------------------------------------------------------------------RELOAD PLOTS
def update(val):
    global traces
    text_box.set_val(int(val))
    if math.floor((prev_traces_time - 3845) / 3600.0) != math.floor((val - 3845) / 3600.0):
        traces = get_fast_trace(val)  # refresh traces
    update_bs_cells(traces, sTime.val, ax_cell, bs_coordinates, colormap_scale)
    update_car_pos(traces, sTime.val, ax_car, color_dict)
    # ax_car.scatter(bs_coordinates['x'], bs_coordinates['y'], marker='s', s=5)  # Plot Base-Stations


def submitTime(text):
    new_val_sec = float(text)
    if new_val_sec > ft_g[-1]:
        new_val_sec = ft_g[-1]
    elif new_val_sec < ft_g[0]:
        new_val_sec = ft_g[0]
    sTime.set_val(int(new_val_sec))


def next_time(event):
    new_val_sec = int(sTime.val) + 1
    if new_val_sec > ft_g[-1]:
        new_val_sec = ft_g[-1]
    elif new_val_sec < ft_g[0]:
        new_val_sec = ft_g[0]
    sTime.set_val(int(new_val_sec))


def prev_time(event):
    new_val_sec = int(sTime.val) - 1
    if new_val_sec > ft_g[-1]:
        new_val_sec = ft_g[-1]
    elif new_val_sec < ft_g[0]:
        new_val_sec = ft_g[0]
    sTime.set_val(int(new_val_sec))


text_box.on_submit(submitTime)
sTime.on_changed(update)
bnext.on_clicked(next_time)
bprev.on_clicked(prev_time)

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')  # Open plot full screen on windows
plt.show()
