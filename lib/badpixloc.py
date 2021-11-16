import numpy as np
import math
import random

"""
Name:

Purpose:

Category:

Calling Example:

Inputs:

Outputs:

History:

Created on 11/14/2021$
"""

def badpixloc(nx, ny, nbad):

	# Make a wider mask
	mx = nx + 3
	my = ny + 3
	mask = np.ones((mx, my))

	count = 0

	# Constants for frequency of continuation
	f = np.asarray([0.3, 0.5, 0.5]) * 0.5 # correction for 2 possible directions

	if nbad == 0:
		mask = mask[0:nx-1,0:ny-1]
		return mask

	badloc = math.floor(random.uniform((10,))*nx) + math.floor(random.uniform((10,))*ny) * mx

	numtree = np.zeros((4,9))
	numtree[0,1] = nbad
	sumtree = numtree.copy()
	loctree = np.zeros((4,nbad))
	loctree[0,:] = badloc


