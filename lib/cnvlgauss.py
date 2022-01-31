import numpy as np
from math import sqrt, pi, exp
from scipy.ndimage import gaussian_filter

"""
Name: cnvlgauss.py

Purpose: This function Gaussian smooths an array in its first dimension.

Category:

Calling Example: result = cnvlgauss(inarray, sigma, fwhm=fwhm)

Inputs:
	inarray: Vector to be spread
	sigma: Width of Gaussian
	fwhm (optional): Used instead of sigma for Gaussian, full width at half maximum.

Outputs: A 1D array that is smoothed according to a Gaussian.

History:

Created on 1/30/2022$
"""

def cnvlgauss(inarray, sigma, fwhm=None):

	if fwhm:
		res = fwhm / 2.354
	else:
		res = sigma

	if res == 0: return inarray

	cnvlarray = gaussian_filter(inarray, res)

	return cnvlarray

def main():
	import matplotlib.pyplot as plt
	x = np.zeros(100)
	x[:50] = np.linspace(0,1)
	x[50:] = np.linspace(1,0)

	cnvlarray = cnvlgauss(x, 5)
	plt.plot(x)
	plt.plot(cnvlarray)
	plt.show()

if __name__ == '__main__':
    main()