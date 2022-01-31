import numpy as np
from random import random, randint
"""
Name: cosrays.py

Purpose: This function returns an array of cosmic rays to be added.

Calling Example: result = cosrays(raymask, maxval)

Inputs:
	raymask: The boolean frame that marks the cosmic ray locations
	inframe: The reference data frame
	maxval: The maximum value cosmic rays are to have (in terms of photons)

Outputs:
	An array with cosmic rays, and all else 0.
	
Procedure:
	First find the locations with cosmic rays, then add the ray's light to the locations.

History:

Created on 1/30/2022$
"""

def cosrays(raymask, maxval):

	# Make a copy of the ray mask
	rayframe = raymask

	# Add Rays
	badloc = np.argwhere(rayframe == 1)
	if not np.any(badloc):
		return rayframe

	nbad = np.shape(badloc)[0]

	rayframe[rayframe== 1] = maxval * np.random.standard_normal((nbad,))**2

	return rayframe

def main():
	import matplotlib.pyplot as plt
	ray_mask = np.zeros((50,50))
	for i in range(10):
		ray_mask[randint(0,49),randint(0,49)] = 1
	plt.imshow(ray_mask)
	plt.show()
	our_frame = np.zeros((50,50))
	rayframe = cosrays(ray_mask, 2)
	plt.imshow(rayframe)
	plt.show()

if __name__ == '__main__':
    main()
