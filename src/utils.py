#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
#    This file is part of Matching Pursuit Python program (python-MP).
#
#    python-MP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-MP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-MP. If not, see <http://www.gnu.org/licenses/>.

author: Tomasz Spustek
e-mail: tomasz@spustek.pl
University of Warsaw, July 06, 2015
'''
from __future__ import division

import numpy as np

def determineAlgorithmConfig(dataInfo):
	config = {}
	config['algorithmType']   = 'smp'
	config['useGradient']     = 1
	config['displayInfo']     = 0
	config['nfft']            = str(1 << (int(dataInfo['samplingFreq'])-1).bit_length())
	config['energyLimit']     = '0.99'
	config['iterationsLimit'] = '20'
	config['channels2calc']   = '1 - ' + str(dataInfo['numberOfChannels'])
	config['trials2calc']     = '1 - ' + str(dataInfo['numberOfTrials'])
	return config

def determineDictionaryConfig(dictionaryConfig , energyLimit , dataInfo):
	density = 1.0 - float(energyLimit)

	if dictionaryConfig == {}:
		dictionaryConfig['useAsym'] = 0
		dictionaryConfig['useRect'] = 0
		dictionaryConfig['minS']    = (str(int((dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'])) , '[samples]')
		dictionaryConfig['maxS']    = (str(int(dataInfo['numberOfSamples'])) , '[samples]')
		dictionaryConfig['dictionaryDensity'] = str(density)
	else:
		if dataInfo['numberOfSamples'] > dictionaryConfig['maxS'][0]:
			dictionaryConfig['maxS']    = (str(int(dataInfo['numberOfSamples'])) , '[samples]')
		if (dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'] < dictionaryConfig['minS'][0]:
			dictionaryConfig['minS']    = (str(int((dataInfo['numberOfSeconds']/8)*dataInfo['samplingFreq'])) , '[samples]')
		if float(dictionaryConfig['dictionaryDensity']) > density:
			dictionaryConfig['dictionaryDensity'] = str(density)

	return dictionaryConfig