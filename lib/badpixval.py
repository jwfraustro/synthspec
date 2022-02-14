import numpy as np

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

def badpixval(badmask, maxval):

	# Make bad pixels
	badframe = 1 - badmask

	badloc = np.where(badframe == 1)

	nbad = np.shape(badloc[0])

	if nbad == 0:
		return badframe

	vals = np.random.uniform(size=nbad)
	for i, loc in enumerate(list(zip(badloc[0], badloc[1]))):
		badframe[loc] = vals[i]

	# Frequency of lows
	f_low = 0.25

	lowloc = np.where(0 < badframe < f_low)
	nlow = np.shape(lowloc[0])
	if nlow != 0:
		lowloc = badloc[lowloc]
	nlow = np.size(lowloc)

	highloc = np.argwhere(badframe[badloc] > f_low)
	nhigh = np.size(highloc)
	if nhigh != 0:
		highloc = badloc[highloc]
	nhigh = np.size(highloc)

	# Dead pixels:
	if nlow != 0:
		badframe[lowloc] = 0

	# Gaussian related to read noise
	if nhigh != 0:
		badframe[highloc] = maxval * np.random.uniform(size=nhigh)

	return badframe