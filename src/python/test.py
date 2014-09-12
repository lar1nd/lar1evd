#!/usr/bin/env python

import os
import sys
import argparse
from collections import defaultdict

import numpy as np

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

def empty_list():
    return []

data = dispatch(file_path)

adc = data.adc()

print(adc.size)
print(adc.shape)
print(data.adc_rows())
print(data.adc_cols())

#print np.min(data.adc()[:240])
#print np.max(data.adc()[:240])
#
#print np.min(data.adc()[240:])
#print np.max(data.adc()[240:])

sys.exit(0)

number_entries = data.entries()

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
