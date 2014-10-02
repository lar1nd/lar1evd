#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict

import numpy as np
from matplotlib import cm
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

from dispatch import dispatch

parser = argparse.ArgumentParser(
    description="View events from LArSoft-generated ROOT file.")
parser.add_argument('file', type=str,
                    help="path to LArSoft-generated ROOT file")
parser.add_argument('--entry', type=int,
                    help="entry number in LArSoft-generated ROOT file")
args = parser.parse_args()

file_path = args.file

if not os.path.isfile(file_path):
    print("File {} does not exist".format(file_path))
    sys.exit(1)

def empty_list():
    return []

data = dispatch(file_path)

entry = 0

number_entries = data.entries()

if args.entry is not None:
    if args.entry < number_entries and args.entry > 0:
        entry = args.entry
    else:
        print("Entry number outside of range [ 0, {} )".format(number_entries))
        sys.exit(1)

data.get_entry(entry)

app = QtGui.QApplication([])
# Create a GLViewWidget for 3D view
gl_view_widget = gl.GLViewWidget()
gl_view_widget.pan(dx=47.5/2, dy=45, dz=0, relative=False)
gl_view_widget.opts['distance'] = 1000
gl_view_widget.show()
gl_view_widget.setWindowTitle("LAr1-ND Event Display")
gl_view_widget.resize(500, 350)

# Disable scipy.weave for current version of pyqtgraph (0.9.8) if OS is
# not Mac OS X
if sys.platform != 'darwin':
    pg.setConfigOptions(useWeave=False)

# Enable anti-aliasing
pg.setConfigOptions(antialias=True)

# Define edges of TPCs
# TODO: Figure out a better way of defining the edges of the TPCs.
tpc_x = (-200, 0, 200)
tpc_y = (-200, 200)
tpc_z = (0, 365)

tpc = np.array([
    [[ tpc_x[0], tpc_z[0], tpc_y[0] ], [ tpc_x[0], tpc_z[1], tpc_y[0] ]],
    [[ tpc_x[0], tpc_z[0], tpc_y[0] ], [ tpc_x[0], tpc_z[0], tpc_y[1] ]],
    [[ tpc_x[0], tpc_z[0], tpc_y[1] ], [ tpc_x[0], tpc_z[1], tpc_y[1] ]],
    [[ tpc_x[0], tpc_z[0], tpc_y[1] ], [ tpc_x[2], tpc_z[0], tpc_y[1] ]],
    [[ tpc_x[0], tpc_z[1], tpc_y[0] ], [ tpc_x[0], tpc_z[1], tpc_y[1] ]],
    [[ tpc_x[0], tpc_z[1], tpc_y[1] ], [ tpc_x[2], tpc_z[1], tpc_y[1] ]],
    [[ tpc_x[2], tpc_z[0], tpc_y[0] ], [ tpc_x[0], tpc_z[0], tpc_y[0] ]],
    [[ tpc_x[2], tpc_z[0], tpc_y[0] ], [ tpc_x[2], tpc_z[1], tpc_y[0] ]],
    [[ tpc_x[2], tpc_z[0], tpc_y[1] ], [ tpc_x[2], tpc_z[0], tpc_y[0] ]],
    [[ tpc_x[2], tpc_z[0], tpc_y[1] ], [ tpc_x[2], tpc_z[1], tpc_y[1] ]],
    [[ tpc_x[2], tpc_z[1], tpc_y[0] ], [ tpc_x[0], tpc_z[1], tpc_y[0] ]],
    [[ tpc_x[2], tpc_z[1], tpc_y[1] ], [ tpc_x[2], tpc_z[1], tpc_y[0] ]],
    [[ tpc_x[1], tpc_z[0], tpc_y[0] ], [ tpc_x[1], tpc_z[0], tpc_y[1] ]],
    [[ tpc_x[1], tpc_z[1], tpc_y[0] ], [ tpc_x[1], tpc_z[1], tpc_y[1] ]],
    [[ tpc_x[1], tpc_z[0], tpc_y[0] ], [ tpc_x[1], tpc_z[1], tpc_y[0] ]],
    [[ tpc_x[1], tpc_z[0], tpc_y[1] ], [ tpc_x[1], tpc_z[1], tpc_y[1] ]],
])

# Define grid lines
# TODO: Figure out a better way of defining the grid lines
grid = []
grid_spacing = 50
for i in range(grid_spacing, tpc_y[1] - tpc_y[0], grid_spacing):
    grid.append([[ tpc_x[0], tpc_z[0], tpc_y[0] + i ],
                 [ tpc_x[0], tpc_z[1], tpc_y[0] + i ]])
for i in range(grid_spacing, int(tpc_z[1] - tpc_z[0]), grid_spacing):
    grid.append([[ tpc_x[0], tpc_z[0] + i, tpc_y[0] ],
                 [ tpc_x[0], tpc_z[0] + i, tpc_y[1] ]])
    grid.append([[ tpc_x[0], tpc_z[0] + i, tpc_y[0] ],
                 [ tpc_x[1], tpc_z[0] + i, tpc_y[0] ]])
    grid.append([[ tpc_x[1], tpc_z[0] + i, tpc_y[0] ],
                 [ tpc_x[2], tpc_z[0] + i, tpc_y[0] ]])
for i in range(grid_spacing, tpc_x[1] - tpc_x[0], grid_spacing):
    grid.append([[ tpc_x[0] + i, tpc_z[0], tpc_y[0] ],
                 [ tpc_x[0] + i, tpc_z[1], tpc_y[0] ]])
    grid.append([[ tpc_x[1] + i, tpc_z[0], tpc_y[0] ],
                 [ tpc_x[1] + i, tpc_z[1], tpc_y[0] ]])
grid = np.array(grid)

# Plot grid lines
# TODO: Figure out a better way of plotting the grid lines
for i in xrange(grid.shape[0]):
    plt = gl.GLLinePlotItem(pos=grid[i], antialias=True,
                            color=(0.25, 0.25, 0.25, 1.0))
    gl_view_widget.addItem(plt)

# Define edges of TPCs
# TODO: Figure out a better way of plotting the edges of the TPCs
for i in xrange(tpc.shape[0]):
    plt = gl.GLLinePlotItem(pos=tpc[i], antialias=True,
                            color=(1.0, 1.0, 1.0, 1.0))
    gl_view_widget.addItem(plt)

# Get MC truth information of particles
number_particles = data.number_particles()
pdg_code = data.pdg_code()
track_id = data.track_id()
parent_id = data.parent_id()
process = data.process()
start_momentum = data.start_momentum()
trajectory_length = data.trajectory_length()
particle_x = data.particle_x()
particle_y = data.particle_y()
particle_z = data.particle_z()

# Particle colors
# TODO: Figure out a better way to handle this
def default_color():
    return pg.glColor(128, 128, 128, 0)

color_dict = defaultdict(default_color)
red = pg.glColor(255, 0, 0)
green = pg.glColor(0, 255, 0)
blue = pg.glColor(0, 128, 255)
magenta = pg.glColor(255, 0, 255)
maroon = pg.glColor(128, 0, 0)
gold = pg.glColor(255, 215, 0)
olive = pg.glColor(128, 128, 0)
silver = pg.glColor(192, 192, 192, 0)
color_dict.update({ 11:gold, -11:magenta, 13:red, -13:red, 211:green,
                    -211:green, 2212:blue, -2212:blue, 12:silver, -12:silver,
                    14:silver, -14:silver })

ignored_particles = (22, 2112, -2112)
trajectory_length_threshold = 1.0
trajectories = []

for i in xrange(len(pdg_code)):

    if pdg_code[i] in ignored_particles:
        continue

    x = np.array(particle_x[i])
    y = particle_y[i]
    z = particle_z[i]

    points = np.array([-x, z, y]).T

    if (trajectory_length[i] < trajectory_length_threshold):
        continue

    plt = gl.GLLinePlotItem(pos=points, antialias=True,
                            color=color_dict[pdg_code[i]])

    trajectories.append(plt)

for trajectory in trajectories:
    gl_view_widget.addItem(trajectory)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
