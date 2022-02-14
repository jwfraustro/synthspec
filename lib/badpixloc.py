import numpy as np
import math
import matplotlib.pyplot as plt
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


# Shapes for bad pixels.
def cross(x, y, mask):
	mask[x - 1:x + 2, y] = 0
	mask[x, y - 1:y + 2] = 0

	return mask, 5


def point(x, y, mask):
	mask[x, y] = 0

	return mask, 1


def line_vert(x, y, mask):
	num_pixels = random.randint(1, 5)

	mask[x:x + num_pixels + 2, y] = 0

	return mask, num_pixels


def line_horz(x, y, mask):
	num_pixels = random.randint(1, 5)

	mask[x, y:y + num_pixels + 2] = 0

	return mask, num_pixels


def gen_pixel_shapes(mask, nbad, mx, my):
	# Function will randomly choose shapes for bad pixels.
	# New shapes can be added or removed by adding them to the list or  commenting them out.

	shapes = ['cross',
	          'point',
	          'line_vert',
	          'line_horz',
	          ]

	count = 0

	while count < nbad:
		shape = random.choice(shapes)

		# Generate center for bad pixel
		x, y, = random.randint(0, mx), random.randint(0, my)

		num = 0

		if shape == 'cross':
			mask, num = cross(x, y, mask)

		elif shape == 'point':
			mask, num = point(x, y, mask)

		elif shape == 'line_vert':
			mask, num = line_vert(x, y, mask)

		elif shape == 'line_horz':
			mask, num = line_horz(x, y, mask)

		count += num

	return mask


def badpixloc(nx, ny, nbad):
	# Make a wider mask
	mx = nx + 3
	my = ny + 3
	mask = np.ones((mx, my))

	mask = gen_pixel_shapes(mask, nbad, mx-1, my-1)
	mask = mask[:nx, :ny]

	count = np.count_nonzero(mask == 0)

	if count > nbad:
		while np.count_nonzero(mask==0) > nbad:
			pixel = random.choice(np.argwhere(mask==0))
			mask[pixel] = 1

	count = np.count_nonzero(mask == 0)

	return mask


if __name__ == '__main__':
	mask, count = badpixloc(512, 512, 500)
	plt.imshow(mask,cmap='gray')
	plt.show()
	print(count)
