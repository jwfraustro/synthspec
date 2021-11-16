import getpass, time
from astropy.io import fits

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

def initheader(nx, ny, obj):

	hdu = fits.PrimaryHDU()

	header = hdu.header

	# Get Variables
	user = getpass.getuser()
	date = time.strftime("%c")

	header['SIMPLE'] = 'T'
	header['NAXIS'] = 2
	header['NAXIS1'] = nx
	header['NAXIS2'] = ny
	header['OBJECT'] = obj
	header['ORIGIN'] = 'SYNTHSPEC'
	header['DATE-OBS'] = date
	header['OBSERVER'] = user

	return hdu