import yaml, os
from shutil import copyfile

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

def defaults(**kwargs):
	config = {}
	config['nx'] = kwargs.get('nx', 512)
	config['ny'] = kwargs.get('ny', config['nx'])
	config['bklevel'] = kwargs.get('bklevel', 200)
	config['epadu'] = kwargs.get('epadu', 10)
	config['rdnoise'] = kwargs.get('rdnoise', 10)
	config['numemil'] = kwargs.get('numemil', 10)
	config['numabsl'] = kwargs.get('numabsl', config['numemil']*2/3)
	config['speclevel'] = kwargs.get('speclevel', 10000)
	config['objpos'] = kwargs.get('objpos', config['nx']/2)
	config['seeing'] = kwargs.get('seeing', 10)
	config['specres'] = kwargs.get('specres', 2)
	config['numbad'] = kwargs.get('numbad', 100)
	config['numrays'] = kwargs.get('numrays', config['numbad'])
	config['maxbadval'] = kwargs.get('maxbadval', 15000)
	config['maxrayval'] = kwargs.get('maxrayval', config['maxbadval']*1/2)
	config['skyllvl'] = kwargs.get('skyllvl', config['bklevel']*4)
	config['emillvl'] = kwargs.get('emillvl', config['speclevel']*6)
	config['temp'] = kwargs.get('temp', 5000)
	config['swavel'] = kwargs.get('swavel', 1.5E-6)
	config['ewavel'] = kwargs.get('ewavel', config['swavel']+0.1E-6)
	config['tiltangle'] = kwargs.get('tiltangle', 1)
	config['traceosc'] = kwargs.get('traceosc', 0.5)
	config['traceamp'] = kwargs.get('traceamp', 6)
	config['smile'] = kwargs.get('smile', 7)
	config['biasframe'] = kwargs.get('biasframe', 0)
	config['flatframe'] = kwargs.get('flatframe', 1)
	return config


def load_config(config_file):
	with open(config_file) as r:
		config = yaml.safe_load(r)

	empty_keys = [k for k, v in config.items() if v == None]
	for k in empty_keys:
		config.pop(k)

	config = defaults(**config)

	return config