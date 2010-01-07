# * Copyright (C) Tue Jan  5 10:10:19 GMT 2010 - Michele Mattioni:
# *  
# * This file is part of NeuronVisio
# * 
# * NeuronVisio is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
#
# * NeuronVisio is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
#
# * You should have received a copy of the GNU General Public License
# * along with NeuronVisio.  If not, see <http://www.gnu.org/licenses/>.

#@PydevCodeAnalysisIgnoren 
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
import sys
sys.path.append(os.path.dirname(__file__)) 

from PyQt4 import QtGui, QtCore, uic

# Pylab
import numpy as np
import matplotlib
matplotlib.use("Qt4Agg")
matplotlib.interactive(True)
import matplotlib.pyplot as plt

from neuron import h
h.load_file("stdrun.hoc")

# Visio

from visio2 import Visio


class Controls():
    """Main class Neuronvisio"""
    def __init__(self):
        app = QtGui.QApplication.instance()
        # Loading the UI
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__),
                                                "neuronvisio.ui"))
        
        # Connecting
        self.ui.Plot3D.connect(self.ui.Plot3D, 
                                     QtCore.SIGNAL('clicked()'), self.launch_visio)
        self.ui.pylab_test.connect(self.ui.pylab_test,
                                         QtCore.SIGNAL('clicked()'), self.plot_x)
        
        self.ui.def_col_btn.setColor(QtGui.QColor(255.,255.,255.))
        self.ui.sel_col_btn.setColor(QtGui.QColor(0.,0.,255.))
        self.ui.init_btn.connect(self.ui.init_btn, QtCore.SIGNAL('clicked()'), self.init)
        self.ui.run_btn.connect(self.ui.run_btn, QtCore.SIGNAL('clicked()'), self.run)
        self.ui.dtSpinBox.connect(self.ui.dtSpinBox, QtCore.SIGNAL('valueChanged(double)'), 
                                  self.dt_changed)
        self.ui.tstopSpinBox.connect(self.ui.tstopSpinBox, QtCore.SIGNAL('valueChanged(double)'), 
                                     self.tstop_changed)
        self.ui.vSpinBox.connect(self.ui.vSpinBox, QtCore.SIGNAL('valueChanged(double)'), 
                                     self.v_changed)
        
                                              
        self.ui.show()
        
        # Start the main event loop.
        app.exec_()
        
    def launch_visio(self):
        if not hasattr(self, 'visio'):
            self.visio = Visio()
            self.visio.draw_model(self.ui.def_col_btn.color)
            self.ui.def_col_btn.connect(self.ui.def_col_btn,
                                        QtCore.SIGNAL("colorChanged(QColor)"),
                                        self.visio.draw_model)
    
    def init(self):
        """Set the vm_init from the spin button and prepare the simulator"""
        
        v_init = self.ui.vSpinBox.value()
        
        # Set the v_init
        h.v_init = v_init
        h.finitialize(v_init)
        h.fcurrent()
        
        # Reset the time in the GUI
        self.ui.time_label.setNum(h.t)
    
    def run(self):
        """Run the simulator till tstop"""
        
        #Initializing
        self.init()
        # Run
        while h.t < h.tstop:
            h.fadvance()
            
            self.ui.time_label.setText("<b>" + str(h.t) + "</b>")
            
    def tstop_changed(self):
        
        h.tstop = self.ui.tstopSpinBox.value()
        
        
    def dt_changed(self):
        
        h.dt = self.ui.dtSpinBox.value()
    
    def v_changed(self):
        
        h.v_init = self.ui.vSpinBox.value()
    
    def plot_x(self):
        
        fig = plt.figure()
        x = np.linspace(0,10)
        plt.plot(x, np.sin(x))

#class Timeloop(qtcore.qthread):
#    """daemon thread to connect the console with the gui"""
#    def __init__(self):
#        qtcore.qthread.__init__(self)
#        self.interval = 0.5 # more relaxed
#        
#        
#    def run(self):
#        """update the gui interface calling the update method"""
#        while true:
#            time.sleep(self.interval)
#            gobject.idle_add(self.controls.update)