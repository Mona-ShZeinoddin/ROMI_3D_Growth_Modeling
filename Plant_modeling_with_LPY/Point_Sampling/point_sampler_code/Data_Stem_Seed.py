#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Automatically generates snapshots of scenes simulated by an L-System.

See `doc/snapshots.md` in lpy_snapshot module for documentation

Launch with:
```shell
cd examples
ipython fractal_snapshots.py
```

This should display a graphical window with a figure containing 6*4 subfigures
"""

from openalea.plantgl.all import Vector3

from lpy_tools.snapshots.lscene_snapshots import grid_simulate_and_shoot

model_filename = 'Data_Stem.lpy'

##############################
# Input variables
##############################

Narray = [6, 10, 15, 20]

###########################################
# Simulate the plant and generate the scans
###########################################

def build_suffix(var):
    return "N"+str(var["N"])+"-A"+str(var["alpha"])

# Definition of shortnames for variables (used for generating small image names)
variable_short_names = {'N':'N', 'alpha':'A'}

# Set fixed variables input to the L-system for all the simulations here:

# Set variables x,y that you want to vary in the L-system to build the figure
# x = [x1,x2,.. ]
# this is made using a dictionary providing for each md the list of x values to simulate
# y = dict key,
# x list = dict values giving for each key the list of x for which a
# simulation sim(x,y) must be computed

fixed_variables_dict = {}
free_variable_list = ['N', 'alpha']  # Should contain the two variables which will vary (simpoints) to make the grid
simpoints = {1: Narray, 3:Narray, 5:Narray, 6:Narray, 20:Narray, 30:Narray}

# Building of the image
# setting camera options
target_point = Vector3(0, 0, 0.)  # looks a bit above z = 0
zoomcoef = 1  # increase to zoom out
camdist = 150.  # increase to widen the observation window


# camdict = {'camdist':camdist, 'zoomcoef':zoomcoef, 'bb':None, 'target_point':target_point}

def cam_setting_fun1(x, y):
    """Defines the camera setting values for each pair of parameter values (x,y).

    Parameters
    ----------
    x represents time
    y represents meristem delay
    """
    t = target_point
    z = zoomcoef
    c = camdist

    return {'camdist': c, 'zoomcoef': z, 'bb': None, 'target_point': t, 'elevation': 0.0}


# Test for reusing a camera file recorded from L-py
# camdict_save = read_camera('camA')
# print(camdict_save)
# grid_simulate_and_shoot(simpoints, model_filename, free_variable_list, fixed_variables_dict, cam_settings = camdict_save, short_names = variable_short_names)

grid_simulate_and_shoot(simpoints, model_filename, free_variable_list, fixed_variables_dict,
                        cam_settings=cam_setting_fun1, short_names = variable_short_names)
