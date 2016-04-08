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

# libraries imports #
import os
import time
from platform  import system
from functools import partial
from os.path   import expanduser
from PyQt4     import QtCore, QtGui


# gui imports #
from settingsGraphics import mainWindowUI

# modules imports #
import data.dataLoader as dl 


class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        
        print '#################'
        print 'Application starting'
        
        print 'Window creation...'
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindowUI()
        self.ui.setupUi(self)
        print '- done'

        print 'Variables initialization...'
        self.initializeFlags()
        self.setVariablesState(0)
        print '- done'

        print 'Setting widgets initial states...'
        self.setWidgetsState()
        print '- done'
        
        print 'Signals and slots connecting...'
        self.setConnections()
        print '- done'
        
        print 'Application started'
        print '###################'

# WIDGETS STATE
###############
    def setConnections(self):
        self.ui.btn_settingsData.clicked.connect(self.resizeWindow)
        self.ui.btn_addData.clicked.connect(self.selectDataFiles)

    def initializeFlags(self):
        self.flags = {}
        self.flags['groupBoxDataResized'] = 0

    def setVariablesState(self , flag):
        self.informationTextColor = QtCore.Qt.green
        self.warrningTextColor    = QtCore.Qt.red

        self.warnings = {}
        self.warnings['openData_err_1'] = 'Field "data" was not found in the file '
        self.warnings['openData_err_2'] = '"Channels" or "trials" did not match the shape of "data", in '
        self.warnings['openData_err_3'] = 'Data matrix has more than three dimensions, in '

        self.warrningDisplayTime = 5000     # in [ms]

        self.dataMatrixes = {}

    def setWidgetsState(self):

        self.ui.groupBoxErrors.setHidden(True)

        self.algorithmTypes = {}
        self.algorithmTypes['SMP']       = 0
        self.algorithmTypes['MMP']       = 1
        
        keys = self.algorithmTypes.keys()
        for position in keys:
            self.ui.cmb_algorithmType.addItem(position)
        self.ui.cmb_algorithmType.setCurrentIndex(1)

        self.ui.btn_calculate.setEnabled(False)
        self.ui.btn_saveSelectedBooks.setEnabled(False)
        self.ui.btn_openVisualisationTool.setEnabled(False)
        self.ui.btn_dictionarySave.setEnabled(False)
        self.ui.btn_removeData.setEnabled(False)

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerEvent)


# WIDGETS BEHAVIOUR
##################
    def selectDataFiles(self):

        dialog = QtGui.QFileDialog.getOpenFileNames(self , 'Open data files' , expanduser('~') , 'Matlab files (*.mat);;Python pickles (*.p);;All Files (*)')

        warningCollector = ''
        for filePath in dialog:
            if filePath != '':
                self.displayInformation('Opening file '+ filePath + '. Please wait...' , 'new')
                if filePath[-4:] == '.mat':
                    (dataMatrix , dataInfo , message) = dl.loadSigmalFromMatlabFile(filePath)
                    if message == 'ok':
                        self.dataMatrixes[filePath] = (dataMatrix , dataInfo)
                        # item = QListWidgetItem("Item %i" % i)
                        # listWidget.addItem(item)
                    else:
                        warningCollector = warningCollector + self.warnings['openData_'+message] + filePath + '\n'

                elif filePath[-2:] == '.p':
                    pass

        self.displayInformation('' , 'new')
        if warningCollector != '':
            self.warrning('on' , warningCollector)

    def displayInformation(self , text , flag='new'):
        # possible flags: new, add, remove_last
        palette = QtGui.QPalette()
        if text == '':
            self.ui.lbl_errors.setText('')
            palette.setColor(QtGui.QPalette.Foreground, self.warrningTextColor)
            self.ui.lbl_errors.setPalette(palette)
            self.ui.groupBoxErrors.hide()
        else:
            palette.setColor(QtGui.QPalette.Foreground, self.informationTextColor)
            self.ui.lbl_errors.setPalette(palette)
            if flag == 'new':
                self.ui.lbl_errors.setText(text)
                self.ui.groupBoxErrors.show()
            elif flag == 'add':
                newtext = self.ui.lbl_errors.text() + ' ' + text
                self.ui.lbl_errors.setText(newtext)
            elif flag == 'remove_last':
                t1 = self.ui.lbl_errors.text().find(' ')
                newtext = self.ui.lbl_errors.text()[0:t1]
                self.ui.lbl_errors.setText(newtext)
        QtGui.QApplication.instance().processEvents()   # Important!

    def warrning(self , flag='off' , errorMsg=''):
        if flag == 'on':
            palette = QtGui.QPalette()
            self.ui.lbl_errors.setText(errorMsg)
            palette.setColor(QtGui.QPalette.Foreground, self.warrningTextColor)
            self.ui.lbl_errors.setPalette(palette)
            self.ui.groupBoxErrors.show()
            self.timer.singleShot(self.warrningDisplayTime , self.timerEvent)
        elif flag == 'off':
            self.ui.lbl_errors.setText('')
            self.ui.groupBoxErrors.hide()
        QtGui.QApplication.instance().processEvents()   # Important!

### PROCESSING EVENTS:
######################
    def timerEvent(self):
        self.warrning('off')


# ANIMATIONS AND WINDOW RESIZING
################################
    def resizeWindow(self):

        animationDuration = 750     # in [ms]

    	self.animation = QtCore.QParallelAnimationGroup(self)
    	self.animation.finished.connect(self.setProperWindowSize)

    	self.animationWindow = QtCore.QPropertyAnimation(self, "size")
        self.animationWindow.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationWindow.setDuration(animationDuration)

        self.animationGroupBoxBooks = QtCore.QPropertyAnimation(self.ui.groupBoxBooks, "geometry")
        self.animationGroupBoxBooks.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxBooks.setDuration(animationDuration)        

        self.animationGroupBoxDataInfo = QtCore.QPropertyAnimation(self.ui.groupBoxDataInfo, "size")
        self.animationGroupBoxDataInfo.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDataInfo.setDuration(animationDuration)

        self.animationGroupBoxAlgorithm = QtCore.QPropertyAnimation(self.ui.groupBoxAlgorithm, "size")
        self.animationGroupBoxAlgorithm.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxAlgorithm.setDuration(animationDuration)

        self.animationGroupBoxDictionary = QtCore.QPropertyAnimation(self.ui.groupBoxDictionary, "geometry")
        self.animationGroupBoxDictionary.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDictionary.setDuration(animationDuration)

        self.animationGroupBoxErrors = QtCore.QPropertyAnimation(self.ui.groupBoxErrors, "size")
        self.animationGroupBoxErrors.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxErrors.setDuration(animationDuration)

        if self.flags['groupBoxDataResized'] == 0:
            self.animationWindow.setEndValue(QtCore.QSize(1000,450))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(710,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(180,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(180,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(980,60))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(495,10,200,370))
            self.setMaximumSize(QtCore.QSize(1000, 450))
            self.flags['groupBoxDataResized'] = 1
        else:
            self.animationWindow.setEndValue(QtCore.QSize(600,450))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(310,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(0,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(0,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(580,60))
            #self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(305,10,0,370))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(305,10,0,370))
            self.setMinimumSize(QtCore.QSize(600, 450))
            self.flags['groupBoxDataResized'] = 0

        self.animation.addAnimation(self.animationWindow)
        self.animation.addAnimation(self.animationGroupBoxBooks)
        self.animation.addAnimation(self.animationGroupBoxDataInfo)
        self.animation.addAnimation(self.animationGroupBoxAlgorithm)
        self.animation.addAnimation(self.animationGroupBoxDictionary)
        self.animation.addAnimation(self.animationGroupBoxErrors)

        self.animation.start()

    def setProperWindowSize(self):
    	if self.flags['groupBoxDataResized'] == 0:
    		self.setMaximumSize(QtCore.QSize(600, 450))
    	else:
    		self.setMinimumSize(QtCore.QSize(1000, 450))

