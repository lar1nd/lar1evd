#!/usr/bin/env python

import os
import sys
import argparse

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
args = parser.parse_args()

file_path = args.file

# ADC baseline for induction and collection planes
induction_pedestal = 2048
collection_pedestal = 400

# Range of ADC values to with respect to ADC baselines
#vmin = -20
#vmax = 80
vmin = -20
vmax = 50

if not os.path.isfile(file_path):
    print("File {} does not exist".format(file_path))
    sys.exit(1)

data = dispatch(file_path)

data.get_entry(2)

number_entries = data.entries()

# The ADC data is returned as a 1-dimensional array. Reshape the array
# into wire numbers as rows and clock ticks as columns.
adc = data.adc().reshape((data.adc_rows(), data.adc_cols()))

# Number of wires in each plane
#   u: 1760
#   v: 1760
#   y: 1216
tpc_0_u = adc[0:1760, :]
tpc_0_v = adc[1760:3520, :]
tpc_0_y = adc[3520:4736, :]
tpc_1_u = adc[4736:6496, :]
tpc_1_v = adc[6496:8256, :]
tpc_1_y = adc[8256:9472, :]

#///////////////////////////////////////////////////////////////////////
# For debugging
#///////////////////////////////////////////////////////////////////////
print(adc.size)
print(adc.shape)
print(data.adc_rows())
print(data.adc_cols())

print(tpc_0_u.shape)
print(tpc_0_v.shape)
print(tpc_0_y.shape)
print(tpc_1_u.shape)
print(tpc_1_v.shape)
print(tpc_1_y.shape)

# This is here to help determine the range of ADC counts for each wire
# plane
print("tpc_0_u ADC count range: ({}, {})"
      .format(np.min(tpc_0_u), np.max(tpc_0_u)))
print("tpc_0_v ADC count range: ({}, {})"
      .format(np.min(tpc_0_v), np.max(tpc_0_v)))
print("tpc_0_y ADC count range: ({}, {})"
      .format(np.min(tpc_0_y), np.max(tpc_0_y)))
print("tpc_1_u ADC count range: ({}, {})"
      .format(np.min(tpc_1_u), np.max(tpc_1_u)))
print("tpc_1_v ADC count range: ({}, {})"
      .format(np.min(tpc_1_v), np.max(tpc_1_v)))
print("tpc_0_y ADC count range: ({}, {})"
      .format(np.min(tpc_1_y), np.max(tpc_1_y)))
#///////////////////////////////////////////////////////////////////////

# Color map for wire vs. time tick
pos = np.arange(256)
color = cm.jet(np.arange(256))
#color = cm.spectral(np.arange(256))
color_map = pg.ColorMap(pos, color)
lookup_table = color_map.getLookupTable(0.0, 255.0, 256)

app = QtGui.QApplication([])
# Create a GraphicsWindow for wire plane views
window = pg.GraphicsWindow(title="LAr1-ND Event Display")
window.resize(1000, 700)
#window.setWindowTitle("LAr1-ND Event Display")

# Enable anti-aliasing
pg.setConfigOptions(antialias=True)

labels = ( pg.LabelItem(text="TPC 0, u"), pg.LabelItem(text="TPC 1, u"),
           pg.LabelItem(text="TPC 0, v"), pg.LabelItem(text="TPC 1, v"),
           pg.LabelItem(text="TPC 0, y"), pg.LabelItem(text="TPC 1, y") )

image_items = ( pg.ImageItem(tpc_0_u), pg.ImageItem(tpc_1_u),
                pg.ImageItem(tpc_0_v), pg.ImageItem(tpc_1_v),
                pg.ImageItem(tpc_0_y), pg.ImageItem(tpc_1_y) )

for image_item in image_items:
    image_item.setLookupTable(lookup_table)

view_boxes = ( window.addViewBox(row=1, col=1),
               window.addViewBox(row=1, col=3),
               window.addViewBox(row=4, col=1),
               window.addViewBox(row=4, col=3),
               window.addViewBox(row=7, col=1),
               window.addViewBox(row=7, col=3) )

for i in xrange(len(view_boxes)):
    view_boxes[i].addItem(image_items[i])
    view_boxes[i].setAspectLocked(lock=True, ratio=5)

x_axes = ( pg.AxisItem(orientation='bottom', linkView=view_boxes[0]),
           pg.AxisItem(orientation='bottom', linkView=view_boxes[1]),
           pg.AxisItem(orientation='bottom', linkView=view_boxes[2]),
           pg.AxisItem(orientation='bottom', linkView=view_boxes[3]),
           pg.AxisItem(orientation='bottom', linkView=view_boxes[4]),
           pg.AxisItem(orientation='bottom', linkView=view_boxes[5]) )

y_axes = ( pg.AxisItem(orientation='left', linkView=view_boxes[0]),
           pg.AxisItem(orientation='left', linkView=view_boxes[1]),
           pg.AxisItem(orientation='left', linkView=view_boxes[2]),
           pg.AxisItem(orientation='left', linkView=view_boxes[3]),
           pg.AxisItem(orientation='left', linkView=view_boxes[4]),
           pg.AxisItem(orientation='left', linkView=view_boxes[5]) )

for axis in x_axes:
    axis.setLabel("Wire")

for axis in y_axes:
    axis.setLabel("Time tick")

# u plane views
window.addItem(labels[0], row=0, col=1)
window.addItem(labels[1], row=0, col=3)
window.addItem(x_axes[0], row=2, col=1)
window.addItem(x_axes[1], row=2, col=3)
window.addItem(y_axes[0], row=1, col=0)
window.addItem(y_axes[1], row=1, col=2)

# v plane views
window.addItem(labels[2], row=3, col=1)
window.addItem(labels[3], row=3, col=3)
window.addItem(x_axes[2], row=5, col=1)
window.addItem(x_axes[3], row=5, col=3)
window.addItem(y_axes[2], row=4, col=0)
window.addItem(y_axes[3], row=4, col=2)

# y plane views
window.addItem(labels[4], row=6, col=1)
window.addItem(labels[5], row=6, col=3)
window.addItem(x_axes[4], row=8, col=1)
window.addItem(x_axes[5], row=8, col=3)
window.addItem(y_axes[4], row=7, col=0)
window.addItem(y_axes[5], row=7, col=2)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
