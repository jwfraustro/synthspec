from lib.config_utils import load_config
from lib.initheader import initheader
import sys, math
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


def synthspec(**config):
	# Check for blank config and set defaults
	nx = config.get('nx', 512)
	ny = config.get('ny', config['nx'])
	bklevel = config.get('bklevel', 200)
	epadu = config.get('epadu', 10)
	rdnoise = config.get('rdnoise', 10)
	numemil = config.get('numemil', 10)
	numabsl = config.get('numabsl', numemil * 2 / 3)
	speclevel = config.get('speclevel', 10000)
	seeing = config.get('seeing', 10)
	specres = config.get('specres', 2)
	numbad = config.get('numbad', 100)
	numrays = config.get('numrays', numbad)
	maxbadval = config.get('maxbadval', 15000)
	maxrayval = config.get('maxrayval', maxbadval * 1 / 2)
	skyllvl = config.get('skyllvl', bklevel * 4)
	emillvl = config.get('emillvl', speclevel * 6)
	temp = config.get('temp', 5000)
	swavel = config.get('swavel', 1.5E-6)
	ewavel = config.get('ewavel', swavel + 0.1E-6)
	tiltangle = config.get('tiltangle', 1)
	traceosc = config.get('traceosc', 0.5)
	traceamp = config.get('traceamp', 6)
	smile = config.get('smile', 7)
	biasframe = config.get('biasframe', 0)
	flatframe = config.get('flatframe', 1)

	nonoise = config.get('nonoise', False)
	nobad = config.get('nobad', False)
	norays = config.get('norays', False)
	nobbcurve = config.get('nobbcurve', False)
	noskyl = config.get('noskyl', False)
	nospecl = config.get('nospecl', False)
	randskyl = config.get('randskyl', False)
	notilt = config.get('notilt', False)
	notrace = config.get('notrace', False)
	nosmile = config.get('nosmile', False)

	# Remake Variables
	# Some variables need to be changed from ADUs to photons, so make new
	# variables with a "p" at the ends of their names. If a 'no' keywords is
	# set, the corresponding variable needs to be made 0 so that the header
	# reads correctly. Tx and Ty are created so that the initial array
	# calculated will be large enough that the rotation and curves do not
	# introduce new data.

	bklevelp = epadu * bklevel  # Background level in photons
	speclevelp = epadu * speclevel  # Obj Spectrum level in photons
	maxbadvalp = epadu * maxbadval  # Max bad pixel level
	maxrayvalp = epadu * maxrayval  # Max cosmic ray level
	maxskyvalp = epadu * (skyllvl - bklevel)  # Max Sky line level
	maxobjvalp = epadu * (emillvl - speclevel)  # Max obj emission line level

	if nobad:
		numbad = 0
	if norays:
		numrays = 0
	if notilt:
		tiltangle = 0
	if nonoise:
		rdnoise = 0
	if nosmile:
		smile = 0
	if notrace:
		traceamp = 0

	if tiltangle < 0:
		tiltangle = 360 + tiltangle
	tilta = tiltangle * math.pi / 180
	tx = math.ceil(max(abs(nx * math.cos(tilta)) + abs(ny * math.sin(tilta)), nx + 2 * abs(traceamp)))
	ty = math.ceil(max(abs(ny * math.cos(tilta)) + abs(nx * math.sin(tilta)), ny + 2 * abs(smile)))

	bx = float(tx - nx) / 2
	by = float(ty - ny) / 2

	ta = tiltangle

	objpos = config.get('objpos', None)

	if not objpos:
		objposb = (tx / 2 )
	else:
		objposb = objpos + abs(traceamp)

	# Initialize
	# Simpleheader is the parent of both objheader and skyheader. It is
	# filled with variables needed for both the sky frame and the object
	# frame.  Badmask is the mask used for the bad pixels in both frames.
	# Badframe is a 2D array of size (nx,ny) that conains 0 for a good
	# value, and the bad pixel's level for bad pixels.  Skymask and
	# objmask are created using badpixloc.  Finally skycrmask and
	# objcrmask are prepared for output.

	hdu = initheader(nx, ny, 'SYNTHSPEC')

	print(hdu.header)

	simpleheader = hdu.header

	simpleheader.append(('SWAVEL', swavel, "start wavelength(m)"))
	simpleheader.append(('EWAVEL', ewavel, "end wavelength(m)"))
	simpleheader.append(('SPECRES', specres, "spectral resolution"))
	simpleheader.append(('SMILE', smile, "Maximum shift in sky lines"))
	simpleheader.append(('TILT',  tiltangle, "deg"))
	simpleheader.append(('SEEING', seeing,"full-width at half-max"))
	simpleheader.append(('TRACEAMP', traceamp,"Max bend amount in object trace"))
	simpleheader.append(('TRACEOSC', traceosc,"number of sine oscil. in trace"))
	simpleheader.append(('MXRAYVAL', maxrayvalp, "in photons"))
	simpleheader.append(('MXBADVAL', maxbadval,"in ADUs"))
	simpleheader.append(('MXSKYVAL', maxskyvalp, "in photons"))
	simpleheader.append(('RDNOISE', rdnoise, "RMS readout noise (e-)"))
	simpleheader.append(('EPADU', epadu, "electrons per ADU"))
	simpleheader.append(('BKLEVEL', bklevelp, 'e-'))

	badmask = badpixloc(nx, ny, numbad)         # Mask contains a 0 for bad
	badframe = badpixval(badmask, maxbadvalp)   # bad pixel values
	skyrays = badpixloc(nx, ny, numrays)        # mask for sky cosmic rays
	objrays = badpixloc(nx, ny, numrays)        # mask for obj cosmic rays

	# Create Sky Frame
	# Simpleframe is the parent frame of both objframe and skyframe.  It
	# is initially filled with the sky spectrum using speclines.  The 1D
	# array skyspec is matrix multiplied to create simpleframe.  Skyframe
	# becomes simpleframe with geometric distrotions, and observational
	# errors (bad pixels, cosmic rays, readnoise, signal noise, gain) from
	# function adderrors.  Bgframe is also prepeared for output.

	if not randskyl:
		fromoh = 1
	else:
		fromoh = 0

	skyspec = speclines(simpleheader, bklevelp, maxskyvalp, numskyl, ty, inspec=inspec, fromoh=fromoh,
	                    nolines=noskyl, ohloc=ohloc)

	skysimple = np.matmul(np.ones(tx), skyspec)

	skysimple = distort(skysimple, simpleheader, bx, by) # Sky frame without noise or bad pixels

	skyheader = simpleheader
	skyframe = skysimple.copy()
	bgframe = skyframe / epadu

	skyframe = adderrors(skyframe, skyheader, skyrays, badmask, badframe, flatframe, biasframe, nonoise = nonoise)

	skycrmask = badmask * skyrays # all bad locations for skyframe

	# Create Object Frame
	# Object header is prepared by adding objframe only variables to
	# simpleheader.  A 1D array ob the object's spectrum is created using
	# speclines.  That spectrum is added into the simpleframe at objposb,
	# with the resulting frame called objframe.  Objframe is distorted,
	# and proframe is prepared for output by distorting a frame with 0
	# background and a flat spectrum.  Finally observational errors are
	# added to objframe.

	objheader = simpleheader

	objheader.append('OBJPOS', objposb, 'starting object position')
	objheader.append('SPECLVL', speclevelp, 'speclevel (e-)')
	objheader.append('NUMEMIL', numemil, 'number of emission lines')
	objheader.append('MXEMILVL', maxobjvalp, 'max obj emission lvl (e-)')
	objheader.append('NUMABSL', numabsl, 'number of emission lines')
	objheader.append('TEMP', temp, 'Temperature of object (K)')

	if not nobbcurve:
		bbcurve = 1
	else:
		bbcurve = 0

	spectrum = speclines(objheader, speclevelp, maxobjvalp, numemil, ty, inspec = inobjspec, bbcurve = bbcurve,
	                     numabs=numabsl, specoff=specoff, nolines=nospecl)

	objframe = np.zeros((tx, ty))
	proframe = np.zeros((tx, ty))
	objframe[:, objposb] = spectrum
	proframe[:, objposb] = 1
	spectrum = spectrum / epadu
	objframe = distort(objframe, objheader, bx, by, xin=tracein)
	proframe = distort(proframe, simpleheader, bx, by, xpos=traceout, xin=tracein)
	specframe = objframe / epadu
	objframe = objframe + skysimple
	fakeval = np.max(specframe)

	objframe = adderrors(objframe, objheader, objrays, badmask, badframe, flatframe, biasframe, nonoise = nonoise,
	                     fakeval=fakeval)

	objcrmask = badmask * objrays
	traceout = traceout + nx/2

	return objframe

	return


if __name__ == '__main__':
	config = load_config(sys.argv[1])
	synthspec(**config)
