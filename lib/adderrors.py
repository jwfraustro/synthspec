"""
Name:

Purpose:

Category:

Calling Example:

Inputs:

Outputs:

History:

Created on 11/16/2021$
"""

import numpy as np


def adderrors(inframe, header, raymask, badmask, badframe, flatframe, biasframe, nonoise=None, fakeval=None):

	nx = np.shape(1)
	ny = np.shape(0)

	#TODO
	#maxrayvalp = sxpar(header, 'MXRAYVAL')
	#rdnoise    = sxpar(header, 'RDNOISE')
	#epadu      = sxpar(header, 'EPADU')

	nbad = len(np.where(raymask == 0))
	nrays = len(np.where(badmask == 0))
	fakeval = max(inframe)

