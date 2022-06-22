# This is where you will be writing most of the stuff, the worker class is here, and all the additional functions are here


import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets, QtCore
from MainWindow import Ui_MainWindow
 
 
# Importing Basic Modules
import sys, os, time
from datetime import datetime
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint

# Importing PyQt5 Modules
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, QObject, pyqtSignal

# Defining color css for Actuator States. If you wanna change the color, then just change the RGB Values here. 
red_color = "background-color: rgb(246, 97, 81);"
green_color = "background-color: rgb(143, 240, 164);"


class Worker(QObject):
    """
    # This is the class that runs threads. Most of your code will be here. There are functions in this that are going to be executed as threads run. 
    # For an example, 2 functions are given, both of which will do some task based on the thread that you call them with. 
    """
    
    
    # Defining signals. 
    finished_1 = pyqtSignal()
    progress_1 = pyqtSignal(int) # you can have anything as a parameter. 
    
    # Defining Signals for second thread. 
    finished_2 = pyqtSignal()
    progress_2 = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # Basic variables can be defined here. 

    def function_thread_1(self):
        '''
        This function will be executed upon making the first thread. 
        It just runs a for loop 60 times after .1 seconds. After each iteration
        it calls a function to update some stuff on the GUI. This is the demo. 
        '''
        for i in range(60):
            print('running Demo')
            time.sleep(0.1)
            # this step is important, coz ur communicating value of i to the GUI. 
            self.progress_1.emit(i) # emitting a signal
            
        # Sending a signal that this thread's task is complete. 
        self.finished_1.emit()



    def function_thread_2(self):
        '''
        This function just runs some random loop. More DEMO. 
        '''        

        for i in range(5):
            print('running the task')
            time.sleep(1)
            self.progress_2.emit(i)
        self.finished_2.emit()
 
 

class Gui(Ui_MainWindow):
    def __init__(self):
        super().__init__()


    def runLongTask_with_thread_1(self):
        '''
        A function to create and manage the first thread. 
        It calls the function from the worker class.         
        '''
        
        # Create a QThread object
        self.thread = QThread()
        
        # Create a worker object
        self.worker = Worker()
        
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        
        # Connect signals and slots
        self.thread.started.connect(self.worker.function_thread_1)
        self.worker.finished_1.connect(self.thread.quit)
        self.worker.finished_1.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress_1.connect(self.reportProgress_thread_1) # this is the function that is called every time the worker calss emits something (line 88)

        
        # Start the thread
        self.thread.start()
        
        self.random_btn_1.setEnabled(False)
        
        # Final resets
        self.thread.finished.connect(
            lambda: self.random_btn_1.setEnabled(True)
        )       

    def reportProgress_thread_1(self, i):
        '''
        This is the function that runs when the worker class function emits 
        or reports some progress to this class. Its the function that updates ur GUI
        And therefore a very important function. 
        '''
        
        ### !DEMO CODE on updating stuff on the GUI. ### 
        
        print('reported from thread one', i)
        if i % 2 == 0:
            self.actuator_box_1.setStyleSheet(green_color)
            self.actuator_box_2.setStyleSheet(red_color)
            self.actuator_box_3.setStyleSheet(green_color)
            self.actuator_box_4.setStyleSheet(red_color)
            self.progress_bar.setValue(i*5)
            self.acc_dial.setValue(i*2)
            self.velo_dial.setValue(i*4)
            self.current_dial.setValue(i*3)
            self.comm_status_radio_btn.setChecked(False)
            self.status_radio_btn_1.setChecked(True)
            self.status_radio_btn_2.setChecked(False)
            self.status_radio_btn_3.setChecked(True)
            self.status_radio_btn_4.setChecked(False)
            self.status_radio_btn_5.setChecked(True)
            self.checkbox_1.setChecked(True)
            self.checkbox_2.setChecked(False)
            
        elif i == 3: 
            self.error_val_lbl.setText("03")            
            
        else: 
            self.actuator_box_1.setStyleSheet(red_color)
            self.actuator_box_2.setStyleSheet(green_color)
            self.actuator_box_3.setStyleSheet(red_color)
            self.actuator_box_4.setStyleSheet(green_color)
            self.progress_bar.setValue(i*5)
            self.acc_dial.setValue(i*2)
            self.velo_dial.setValue(i*4)
            self.current_dial.setValue(i*3)
            self.comm_status_radio_btn.setChecked(True)
            self.status_radio_btn_1.setChecked(False)
            self.status_radio_btn_2.setChecked(True)
            self.status_radio_btn_3.setChecked(False)
            self.status_radio_btn_4.setChecked(True)
            self.status_radio_btn_5.setChecked(False)
            self.checkbox_1.setChecked(False)
            self.checkbox_2.setChecked(True)

    def runLongTask_with_thread_2(self):
        # Create a QThread object
        self.thread_2 = QThread()
        
        # Create a worker object
        self.worker_2 = Worker()
        
        # Move worker to the thread
        self.worker_2.moveToThread(self.thread_2)
        
        # Connect signals and slots
        self.thread_2.started.connect(self.worker_2.function_thread_2)
        self.worker_2.finished_2.connect(self.thread_2.quit)
        self.worker_2.finished_2.connect(self.worker_2.deleteLater)
        self.thread_2.finished.connect(self.thread_2.deleteLater)
        self.worker_2.progress_2.connect(self.reportProgress_thread_2)
        # self.worker_2.gimme_values.connect(self.give_val)
        # self.stop_signal.connect(self.worker_2.stop_immediately)
        
        # Start the thread_2
        self.thread_2.start()
        self.random_btn_2.setEnabled(False)
        
        # Final resets
        self.thread_2.finished.connect(
            lambda: self.random_btn_2.setEnabled(True)
        )
      
    def reportProgress_thread_2(self, i):
        print('Reported Progress from two', i)

    def gen_Graph(self):
        '''
        Starts a timer, and on an interval of 50 ms updates the graph. 
        Im assuming this timer thing creats a thread of its own and manages it on its own. 
        but not sure.
        '''
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):
        '''
        Updates the graph by changing the values of x and y. 
        If you are changing the values, then this is where you should 
        either get the values from the sensor or from a csv file. 
        '''
    
    
        # Updating data for the Velocity Graph
        # -------------------------------------------------------------------------
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.velo_data_line.setData(self.x, self.y)  # Update the data.
        # -------------------------------------------------------------------------


        # Updating data for Acceleration Graph. 
        # -------------------------------------------------------------------------
        # self.x1 = self.x1[1:]  # Remove the first y element.
        self.x1.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        # self.y1 = self.y1[1:]  # Remove the first
        self.y1.append( randint(0,100))  # Add a new random value.

        self.acc_data_line.setData(self.x1, self.y1)  # Update the data.
        # -------------------------------------------------------------------------




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Gui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())