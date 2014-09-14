#!/usr/bin/env python

import os
import sys
import argparse

import numpy as np
import matplotlib.pyplot as plt

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

tpc_wires = (tpc_0_u, tpc_1_u, tpc_0_v, tpc_1_v, tpc_0_y, tpc_1_y)
tpc_plane_labels = ("TPC 0, U", "TPC 1, U", "TPC 0, V", "TPC 1, V", "TPC 0, Y",
                    "TPC 1, Y")

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

fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2)
axes = (ax1, ax2, ax3, ax4, ax5, ax6)

for i in xrange(len(axes)):
    axes[i].imshow(tpc_wires[i].T, aspect=0.2, origin='lower',
                   #vmin=vmin+induction_pedestal,
                   #vmax=vmax+induction_pedestal,
                   #vmin=vmin+collection_pedestal,
                   #vmax=vmax+collection_pedestal,
                   cmap=plt.get_cmap('jet'))
    axes[i].tick_params(axis='both', which='major', labelsize=10)
    axes[i].set_title(tpc_plane_labels[i], fontsize=10)
    axes[i].set_xlabel("Wire", fontsize=10)
    axes[i].set_ylabel("Time tick", fontsize=10)

plt.show()
