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

from src.dictionary       import generateDictionary
from data.signalGenerator import generateTestSignal , defaultValues
from src.processing       import calculateMP

import matplotlib.pyplot as plt
import numpy             as np


if __name__ == '__main__':
	# create a syntetic signal
	(gaborParams , sinusParams , noiseRatio, samplingFrequency) = defaultValues()
	(signal,time) = generateTestSignal(gaborParams,sinusParams,noiseRatio)

	# generate dictionary
	flags = {}
	flags['useAsymA'] = 1
	flags['useRectA'] = 1
	config = {}
	config['flags']   = flags
	config['minS']    = 10
	config['maxS']    = 30
	config['density'] = 0.01

	dictionary = generateDictionary(time , config)


	# calculate Matching Pursuit
	config['maxNumberOfIterations']            = 15
	config['minEnergyExplained']               = 0.99
	config['samplingFrequency']                = samplingFrequency
	config['minNFFT']                          = 2*samplingFrequency
	config['flags']['useGradientOptimization'] = 1

	wynik = calculateMP(dictionary , signal , config) 



	# envelope = dictionary[7]['timeCourse']
	# plt.plot(envelope)
	# plt.show()

