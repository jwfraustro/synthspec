import numpy as np

"""
Name: randlines.py

Purpose: This function makes a 1D array of random spec lines.

Calling Example: result = randlines(ny, numl)

Inputs:
	ny = Number of columns
	numl = Number of lines

Outputs:
	A 1D array with spectrum lines with values between 0 and 1.

History:

Created on 1/30/2022$
"""

def randlines(ny, numl):

	spec = np.zeros(ny)

	# Each line's position, width, and height
	# TODO height value does not work
	lines = [[np.floor(np.random.uniform(0, ny, numl))],
	         [np.random.uniform(0,2.5, numl) + 0.5],
	         [min(1/(np.random.uniform(0,1000,numl)), 1.0)]]

	lines = np.transpose(lines)
	return lines

def main():
	import matplotlib.pyplot as plt
	lines = randlines(100, 10)
	print(lines[0])
	plt.plot(lines[0][0])
	plt.show()

if __name__ == '__main__':
    main()