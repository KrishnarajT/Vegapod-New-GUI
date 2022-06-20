####################################################################
# This is the GUI for Vegapod's New Pod.
# Base Code by KrishnarajT
# Base Repo on https://www.github.com/KrishnarajT/Vegapod-New-Gui.git
# Made in PyQt5 



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


### MULTITHREADING ###
'''
The Basic Way of working is explained in as brief as possible here. 
So the reason you need multithreading is that in a GUI, code has to be run to check how the user is interacting with the UI. And if you run something on the backend
Then the GUI wont respond to the user coz its busy running that backend code. To avoid this we use different threads. 

Now you can do this with python's multithreading module, or Qt's personal threads. 
In this case Qt's threads are better, as they are more integrated. 


So you basically have a worker class. That class has certain functions. 
To communicate with that class, you create a worker object, To give values
to that object, you will just give the values the moment the class is defined in its 
constructor. 

To send values from this worker class to your main GUI class to display, you need
to send a signal. And there needs to be a slot in ur GUI class to receive that signal. This system of signals and slots is what multithreading in GUI is reliant on. 

What we will do essentially, is that on press of a button or some trigger, 
you can call a function that creats a new thread, and then gives necessary variables
to the backend worker class to run its code. You then have to connect the signals and
slots to certain functions. Then we just call the function from the worker class, 
which then runs simultaineously as ur GUI. After doing that task, it returns a value
via the signal and slot, and upon catching that value you can call another function
in your main class, that will show the necessary changes in your GUI.

'''



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


class Ui_MainWindow(QMainWindow): 
    """
    Main GUI Class. Everything is defined and done here. 
    """
    def __init__(self):
        super().__init__()
        self.setObjectName("NEW POD GUI")
        self.resize(1920, 1080)
        self.setupUi()

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

    def setupUi(self):
        '''
        This is the function that defines all the widgets. 
        Other than connecting functions, and changing the graph,
        most of the stuff here is GUI related and better left without messing with.         
        '''
        
        # BASIC WIDGET STUFF
        # -----------------------------------------------------------------------------------------------------
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        # Defining the Basic Tab        
        self.navigation_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.navigation_tab_widget.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.navigation_tab_widget.setObjectName("navigation_tab_widget")
        
        # Defining Tabs
        self.dashboard_tab = QtWidgets.QWidget()
        self.dashboard_tab.setObjectName("dashboard_tab")
        self.navigation_tab_widget.addTab(self.dashboard_tab, "")

        self.graph_tab = QtWidgets.QWidget()
        self.graph_tab.setObjectName("graph_tab")
        self.navigation_tab_widget.addTab(self.graph_tab, "")
        
        # Creating a layout for graphs. 
        self.layout_widget = QtWidgets.QWidget(self.graph_tab)
        self.layout_widget.setGeometry(QtCore.QRect(0, 0, 1920, 1000))
        self.layout_widget.setObjectName("layout_widget")
        
        # Adding vertical Layout to graphs. 
        self.vertical_layout = QtWidgets.QVBoxLayout(self.layout_widget)
        self.vertical_layout.setContentsMargins(50, 0, 50, 50)
        self.vertical_layout.setObjectName("vertical_layout")
        
        # Creating Current graph and Acceleration Graph widgets. 
        font = QtGui.QFont()
        font.setPointSize(22)
        self.velo_graph_lbl = QtWidgets.QLabel(self.layout_widget)
        self.velo_graph_lbl.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.velo_graph_lbl.setFont(font)
        self.velo_graph_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_graph_lbl.setObjectName("velo_graph_lbl")
        self.velo_graph_lbl.setText("Current Live Graph")
        
        # Creating Current graph and Acceleration Graph widgets. 
        self.acc_graph_lbl = QtWidgets.QLabel(self.layout_widget)
        self.acc_graph_lbl.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.acc_graph_lbl.setFont(font)
        self.acc_graph_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_graph_lbl.setObjectName("acc_graph_lbl")
        self.acc_graph_lbl.setText("Acceleration Live Graph")
        

        # Creating the Graph
        
        self.velo_graph_pg_widget = pg.PlotWidget()

        # Demo Data
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.velo_graph_pg_widget.setBackground('black')
        self.velo_graph_pg_widget.showGrid(True, True)
        pen_1 = pg.mkPen(color='#11c2c4', width=2)
        self.velo_data_line =  self.velo_graph_pg_widget.plot(self.x, self.y, pen=pen_1)
        
        self.acc_graph_pg_widget = pg.PlotWidget()
        self.vertical_layout.addWidget(self.acc_graph_pg_widget)

        self.x1 = list(range(100))  # 100 time points
        self.y1 = [randint(0,50) for _ in range(100)]  # 100 data points

        self.acc_graph_pg_widget.setBackground('black')
        self.acc_graph_pg_widget.showGrid(True, True)
        pen_2 = pg.mkPen(color='#ec8734', width = 2)
        self.acc_data_line =  self.acc_graph_pg_widget.plot(self.x1, self.y1, pen=pen_2)
        

        
        self.vertical_layout.addWidget(self.velo_graph_lbl)
        self.vertical_layout.addWidget(self.velo_graph_pg_widget)
        self.vertical_layout.addWidget(self.acc_graph_lbl)
        self.vertical_layout.addWidget(self.acc_graph_pg_widget)

        self.MainFrame = QtWidgets.QFrame(self.dashboard_tab)
        self.MainFrame.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        # -----------------------------------------------------------------------------------------------------


        # PROGRESS BAR
        # -----------------------------------------------------------------------------------------------------
        self.progress_bar = QtWidgets.QProgressBar(self.MainFrame)
        self.progress_bar.setGeometry(QtCore.QRect(270, 460, 1600, 31))
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        # -----------------------------------------------------------------------------------------------------
        
        
        
        # DATA FIELDS
        # -----------------------------------------------------------------------------------------------------
        self.data_fields_list_widget = QtWidgets.QListWidget(self.MainFrame)
        self.data_fields_list_widget.setGeometry(QtCore.QRect(0, 49, 250, 1031))
        self.data_fields_list_widget.setObjectName("data_fields_list_widget")
        
        self.data_field_lbl = QtWidgets.QLabel(self.MainFrame)
        self.data_field_lbl.setGeometry(QtCore.QRect(0, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.data_field_lbl.setFont(font)
        self.data_field_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.data_field_lbl.setObjectName("data_field_lbl")
        
        # This is how you add new items. Follow these 4 lines given here for each new item. 
        
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item.setText("Some Text")
        item = self.data_fields_list_widget.item(0)
        # -----------------------------------------------------------------------------------------------------

        
        # DIALS / GAUGES 
        # -----------------------------------------------------------------------------------------------------
        
        # CURRENT --------------------------------------------------------------
        self.current_dial = QtWidgets.QDial(self.MainFrame)
        self.current_dial.setGeometry(QtCore.QRect(970, 80, 241, 181))
        self.current_dial.setObjectName("current_dial")

        self.current_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_val_lbl.setGeometry(QtCore.QRect(1050, 120, 81, 71))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.current_val_lbl.setFont(font)
        self.current_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_val_lbl.setWordWrap(True)
        self.current_val_lbl.setObjectName("current_val_lbl")
        self.current_unit_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_unit_lbl.setGeometry(QtCore.QRect(1050, 170, 81, 21))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.current_unit_lbl.setFont(font)
        self.current_unit_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_unit_lbl.setObjectName("current_unit_lbl")
        
        self.current_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_lbl.setGeometry(QtCore.QRect(1010, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.current_lbl.setFont(font)
        self.current_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_lbl.setObjectName("current_lbl")
        # ----------------------------------------------------------- 
        
        # ACCELERATION -----------------------------------------------------------
        self.acc_dial = QtWidgets.QDial(self.MainFrame)
        self.acc_dial.setGeometry(QtCore.QRect(600, 110, 361, 311))
        self.acc_dial.setObjectName("acc_dial")
        
        self.acc_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_lbl.setGeometry(QtCore.QRect(650, 50, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.acc_lbl.setFont(font)
        self.acc_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_lbl.setObjectName("acc_lbl")
        
        self.acc_unit_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_unit_lbl.setGeometry(QtCore.QRect(720, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(22)
        self.acc_unit_lbl.setFont(font)
        self.acc_unit_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_unit_lbl.setObjectName("acc_unit_lbl")
        self.acc_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_val_lbl.setGeometry(QtCore.QRect(710, 190, 141, 111))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(35)
        self.acc_val_lbl.setFont(font)
        self.acc_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_val_lbl.setWordWrap(True)
        self.acc_val_lbl.setObjectName("acc_val_lbl")
        # -----------------------------------------------------------
        
        # VELOCITY  -----------------------------------------------------------
        self.velo_dial = QtWidgets.QDial(self.MainFrame)
        self.velo_dial.setGeometry(QtCore.QRect(1210, 120, 361, 311))
        self.velo_dial.setObjectName("velo_dial")
        self.velo_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_val_lbl.setGeometry(QtCore.QRect(1320, 200, 141, 111))
        
        self.velo_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_lbl.setGeometry(QtCore.QRect(1270, 60, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.velo_lbl.setFont(font)
        self.velo_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_lbl.setObjectName("velo_lbl")
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(35)
        self.velo_val_lbl.setFont(font)
        self.velo_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_val_lbl.setWordWrap(True)
        self.velo_val_lbl.setObjectName("velo_val_lbl")
        self.velo_unit_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_unit_lbl.setGeometry(QtCore.QRect(1330, 290, 111, 31))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(22)
        self.velo_unit_lbl.setFont(font)
        self.velo_unit_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_unit_lbl.setObjectName("velo_unit_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        
        # TEMPERATURE DATA FIELDS
        # -----------------------------------------------------------------------------------------------------
        
        self.temp_val_lbl_1 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_1.setGeometry(QtCore.QRect(590, 600, 241, 41))
        self.temp_val_lbl_1.setObjectName("temp_val_lbl_1")
        self.temp_val_lbl_2 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_2.setGeometry(QtCore.QRect(590, 640, 241, 41))
        self.temp_val_lbl_2.setObjectName("temp_val_lbl_2")
        self.temp_val_lbl_3 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_3.setGeometry(QtCore.QRect(590, 680, 241, 41))
        self.temp_val_lbl_3.setObjectName("temp_val_lbl_3")
        self.temp_val_lbl_4 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_4.setGeometry(QtCore.QRect(590, 720, 241, 41))
        self.temp_val_lbl_4.setObjectName("temp_val_lbl_4")
        self.temp_val_lbl_5 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_5.setGeometry(QtCore.QRect(590, 760, 241, 41))
        self.temp_val_lbl_5.setObjectName("temp_val_lbl_5")
        self.temp_val_lbl_6 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_6.setGeometry(QtCore.QRect(590, 800, 241, 41))
        self.temp_val_lbl_6.setObjectName("temp_val_lbl_6")
        self.temp_lbl = QtWidgets.QLabel(self.MainFrame)
        self.temp_lbl.setGeometry(QtCore.QRect(570, 540, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.temp_lbl.setFont(font)
        self.temp_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_lbl.setObjectName("temp_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        
        # PRESSURE DATA FIELDS
        # -----------------------------------------------------------------------------------------------------
        self.pres_val_lbl_2 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_2.setGeometry(QtCore.QRect(860, 640, 241, 41))
        self.pres_val_lbl_2.setObjectName("pres_val_lbl_2")
        self.pressure_lbl = QtWidgets.QLabel(self.MainFrame)
        self.pressure_lbl.setGeometry(QtCore.QRect(820, 540, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pressure_lbl.setFont(font)
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.pressure_lbl.setObjectName("pressure_lbl")
        self.pres_val_lbl_3 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_3.setGeometry(QtCore.QRect(860, 680, 241, 41))
        self.pres_val_lbl_3.setObjectName("pres_val_lbl_3")
        self.pres_val_lbl_5 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_5.setGeometry(QtCore.QRect(860, 760, 241, 41))
        self.pres_val_lbl_5.setObjectName("pres_val_lbl_5")
        self.pres_val_lbl_1 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_1.setGeometry(QtCore.QRect(860, 600, 241, 41))
        self.pres_val_lbl_1.setObjectName("pres_val_lbl_1")
        self.pres_val_lbl_6 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_6.setGeometry(QtCore.QRect(860, 800, 241, 41))
        self.pres_val_lbl_6.setObjectName("pres_val_lbl_6")
        self.pres_val_lbl_4 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_4.setGeometry(QtCore.QRect(860, 720, 241, 41))
        self.pres_val_lbl_4.setObjectName("pres_val_lbl_4")
        # -----------------------------------------------------------------------------------------------------
        
        # ACTUATOR BOX
        # -----------------------------------------------------------------------------------------------------
        red_color = "background-color: rgb(246, 97, 81);"
        green_color = "background-color: rgb(143, 240, 164);"
        
        self.actuator_box_1 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_1.setGeometry(QtCore.QRect(310, 590, 91, 81))
        self.actuator_box_1.setStyleSheet(red_color) # This is how you set the color
        self.actuator_box_1.setText("")
        self.actuator_box_1.setObjectName("actuator_box_1")
        self.actuator_box_2 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_2.setGeometry(QtCore.QRect(410, 590, 91, 81))
        self.actuator_box_2.setStyleSheet(red_color) 
        self.actuator_box_2.setText("")
        self.actuator_box_2.setObjectName("actuator_box_2")
        self.actuator_box_4 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_4.setGeometry(QtCore.QRect(310, 680, 91, 81))
        self.actuator_box_4.setStyleSheet(green_color)
        self.actuator_box_4.setText("")
        self.actuator_box_4.setObjectName("actuator_box_4")
        self.actuator_box_3 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_3.setGeometry(QtCore.QRect(410, 680, 91, 81))
        self.actuator_box_3.setStyleSheet(green_color)
        self.actuator_box_3.setText("")
        self.actuator_box_3.setObjectName("actuator_box_3")
        self.actuator_lbl = QtWidgets.QLabel(self.MainFrame)
        self.actuator_lbl.setGeometry(QtCore.QRect(290, 540, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.actuator_lbl.setFont(font)
        self.actuator_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.actuator_lbl.setObjectName("actuator_lbl")
        # -----------------------------------------------------------------------------------------------------

        
        # LAUNCH, BRAKE, ARM BUTTON
        # -----------------------------------------------------------------------------------------------------
        
        # LAUNCH
        self.launch_btn = QtWidgets.QPushButton(self.MainFrame)
        self.launch_btn.setGeometry(QtCore.QRect(1150, 560, 261, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.launch_btn.setFont(font)
        self.launch_btn.setObjectName("launch_btn")
        
        # BRAKE
        self.brake_btn = QtWidgets.QPushButton(self.MainFrame)
        self.brake_btn.setGeometry(QtCore.QRect(1150, 720, 591, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.brake_btn.setFont(font)
        self.brake_btn.setObjectName("brake_btn")
        
        # ARM
        self.arm_btn = QtWidgets.QPushButton(self.MainFrame)
        self.arm_btn.setGeometry(QtCore.QRect(1480, 560, 251, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.arm_btn.setFont(font)
        self.arm_btn.setObjectName("arm_btn")
        
        # Power Slider
        self.power_slider = QtWidgets.QSlider(self.MainFrame)
        self.power_slider.setGeometry(QtCore.QRect(1760, 770, 131, 21))
        self.power_slider.setOrientation(QtCore.Qt.Horizontal)
        self.power_slider.setObjectName("power_slider")
        self.power_lbl = QtWidgets.QLabel(self.MainFrame)
        self.power_lbl.setGeometry(QtCore.QRect(1740, 730, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.power_lbl.setFont(font)
        self.power_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.power_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.power_lbl.setObjectName("power_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        
        # COMMUNICATION STATES AND LED
        # -----------------------------------------------------------------------------------------------------
        self.comm_lbl = QtWidgets.QLabel(self.MainFrame)
        self.comm_lbl.setGeometry(QtCore.QRect(270, 780, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.comm_lbl.setFont(font)
        self.comm_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.comm_lbl.setObjectName("comm_lbl")
        self.comm_status_radio_btn = QtWidgets.QRadioButton(self.MainFrame)
        self.comm_status_radio_btn.setGeometry(QtCore.QRect(360, 820, 148, 28))
        self.comm_status_radio_btn.setChecked(True)
        self.comm_status_radio_btn.setAutoExclusive(False)
        self.comm_status_radio_btn.setObjectName("comm_status_radio_btn")
        # -----------------------------------------------------------------------------------------------------
        
        
        # STATUS LEDS as RADIO BUTTONS
        # -----------------------------------------------------------------------------------------------------
        self.status_radio_btn_2 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_2.setGeometry(QtCore.QRect(1760, 30, 148, 28))
        self.status_radio_btn_2.setCheckable(True)
        self.status_radio_btn_2.setChecked(True) # This is how you check them, or make them appear ON. 
        self.status_radio_btn_2.setAutoRepeat(False)
        self.status_radio_btn_2.setAutoExclusive(False)
        self.status_radio_btn_2.setObjectName("status_radio_btn_2")
        self.status_radio_btn_3 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_3.setGeometry(QtCore.QRect(1610, 70, 148, 28))
        self.status_radio_btn_3.setCheckable(True)
        self.status_radio_btn_3.setChecked(True)
        self.status_radio_btn_3.setAutoExclusive(False)
        self.status_radio_btn_3.setObjectName("status_radio_btn_3")
        self.status_radio_btn_1 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_1.setGeometry(QtCore.QRect(1610, 30, 148, 28))
        self.status_radio_btn_1.setChecked(True)
        self.status_radio_btn_1.setAutoExclusive(False)
        self.status_radio_btn_1.setObjectName("status_radio_btn_1")
        self.status_radio_btn_4 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_4.setGeometry(QtCore.QRect(1760, 70, 148, 28))
        self.status_radio_btn_4.setChecked(True)
        self.status_radio_btn_4.setAutoExclusive(False)
        self.status_radio_btn_4.setObjectName("status_radio_btn_4")
        self.status_radio_btn_5 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_5.setGeometry(QtCore.QRect(1610, 110, 148, 28))
        self.status_radio_btn_5.setChecked(True)
        self.status_radio_btn_5.setAutoExclusive(False)
        self.status_radio_btn_5.setObjectName("status_radio_btn_5")
        # -----------------------------------------------------------------------------------------------------
        
        
        # SPIN AND CHECK BOXES
        # -----------------------------------------------------------------------------------------------------
        self.spin_box_1 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_1.setGeometry(QtCore.QRect(1770, 350, 75, 32))
        self.spin_box_1.setObjectName("spin_box_1")
        self.spin_box_2 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_2.setGeometry(QtCore.QRect(1770, 390, 75, 32))
        self.spin_box_2.setObjectName("spin_box_2")
        
        self.spin_box_2_lbl = QtWidgets.QLabel(self.MainFrame)
        self.spin_box_2_lbl.setGeometry(QtCore.QRect(1610, 390, 161, 31))
        self.spin_box_2_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spin_box_2_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_2_lbl.setObjectName("spin_box_2_lbl")
        self.spin_box_1_lbl = QtWidgets.QLabel(self.MainFrame)
        self.spin_box_1_lbl.setGeometry(QtCore.QRect(1600, 350, 161, 31))
        self.spin_box_1_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spin_box_1_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_1_lbl.setObjectName("spin_box_1_lbl")
        
        
        self.checkbox_1 = QtWidgets.QCheckBox(self.MainFrame)
        self.checkbox_1.setGeometry(QtCore.QRect(1150, 520, 141, 28))
        self.checkbox_1.setObjectName("checkbox_1")
        self.checkbox_2 = QtWidgets.QCheckBox(self.MainFrame)
        self.checkbox_2.setGeometry(QtCore.QRect(1490, 520, 151, 28))
        self.checkbox_2.setObjectName("checkbox_2")
        # -----------------------------------------------------------------------------------------------------
        
        # ERRORS 
        # -----------------------------------------------------------------------------------------------------
        self.error_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.error_val_lbl.setGeometry(QtCore.QRect(1760, 550, 111, 111))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(55)
        font.setWeight(50)
        self.error_val_lbl.setFont(font)
        self.error_val_lbl.setStyleSheet("color: rgb(237, 51, 59);")
        self.error_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.error_val_lbl.setObjectName("error_val_lbl")
        self.error_lbl = QtWidgets.QLabel(self.MainFrame)
        self.error_lbl.setGeometry(QtCore.QRect(1750, 650, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.error_lbl.setFont(font)
        self.error_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.error_lbl.setObjectName("error_lbl")
        # -----------------------------------------------------------------------------------------------------

        # RANDOM BUTTONS
        # -----------------------------------------------------------------------------------------------------
        self.random_btn_1 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_1.setGeometry(QtCore.QRect(1150, 820, 154, 32))
        self.random_btn_1.setObjectName("random_btn_1")
        self.random_btn_1.clicked.connect(self.runLongTask_with_thread_1)
        
        self.random_btn_2 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_2.setGeometry(QtCore.QRect(1350, 820, 154, 32))
        self.random_btn_2.setObjectName("random_btn_2")
        self.random_btn_2.clicked.connect(self.gen_Graph)

        
        self.random_btn_3 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_3.setGeometry(QtCore.QRect(1540, 820, 154, 32))
        self.random_btn_3.setObjectName("random_btn_3")
        self.random_btn_3.clicked.connect(self.runLongTask_with_thread_2)
        
        self.random_btn_4 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_4.setGeometry(QtCore.QRect(1730, 820, 154, 32))
        self.random_btn_4.setObjectName("random_btn_4")
        # -----------------------------------------------------------------------------------------------------



        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "NEW POD GUI"))
        __sortingEnabled = self.data_fields_list_widget.isSortingEnabled()
        self.data_fields_list_widget.setSortingEnabled(False)
        # item = self.data_fields_list_widget.item(0)
        # item.setText(_translate("self", "New Item 0"))
        self.navigation_tab_widget.setTabText(self.navigation_tab_widget.indexOf(self.dashboard_tab), _translate("self", "Dashboard"))
        self.navigation_tab_widget.setTabText(self.navigation_tab_widget.indexOf(self.graph_tab), _translate("self", "Graphs"))
        self.data_fields_list_widget.setSortingEnabled(__sortingEnabled)
        self.temp_val_lbl_1.setText(_translate("self", "Temperature Value 1"))
        self.temp_val_lbl_2.setText(_translate("self", "Temperature Value 2"))
        self.temp_val_lbl_3.setText(_translate("self", "Temperature Value 3"))
        self.temp_val_lbl_4.setText(_translate("self", "Temperature Value 4"))
        self.temp_val_lbl_5.setText(_translate("self", "Temperature Value 5"))
        self.temp_val_lbl_6.setText(_translate("self", "Temperature Value 6"))
        self.temp_lbl.setText(_translate("self", "Temperature"))
        self.pres_val_lbl_2.setText(_translate("self", "Pressure Value 2"))
        self.pressure_lbl.setText(_translate("self", "Pressure"))
        self.pres_val_lbl_3.setText(_translate("self", "Pressure Value 3"))
        self.pres_val_lbl_5.setText(_translate("self", "Pressure Value 5"))
        self.pres_val_lbl_1.setText(_translate("self", "Pressure Value 1"))
        self.pres_val_lbl_6.setText(_translate("self", "Pressure Value 6"))
        self.pres_val_lbl_4.setText(_translate("self", "Pressure Value 4"))
        self.actuator_lbl.setText(_translate("self", "Actuator States"))
        self.launch_btn.setText(_translate("self", "Launch"))
        self.brake_btn.setText(_translate("self", "Brake"))
        self.arm_btn.setText(_translate("self", "Arm"))
        self.current_lbl.setText(_translate("self", "Current"))
        self.acc_lbl.setText(_translate("self", "Acceleration"))
        self.comm_lbl.setText(_translate("self", "Communication State"))
        self.velo_lbl.setText(_translate("self", "Velocity"))
        self.comm_status_radio_btn.setText(_translate("self", "Status"))
        self.current_val_lbl.setText(_translate("self", "23.52"))
        self.current_unit_lbl.setText(_translate("self", "mA"))
        self.acc_unit_lbl.setText(_translate("self", "m/s/s"))
        self.acc_val_lbl.setText(_translate("self", "11.12"))
        self.velo_val_lbl.setText(_translate("self", "49.22"))
        self.velo_unit_lbl.setText(_translate("self", "m/s"))
        self.status_radio_btn_2.setText(_translate("self", "Status 2"))
        self.status_radio_btn_3.setText(_translate("self", "Status 3"))
        self.status_radio_btn_1.setText(_translate("self", "Status 1"))
        self.status_radio_btn_4.setText(_translate("self", "Status 4"))
        self.power_lbl.setText(_translate("self", "Power"))
        self.spin_box_2_lbl.setText(_translate("self", "Set Value"))
        self.spin_box_1_lbl.setText(_translate("self", "Counter Val 1"))
        self.checkbox_1.setText(_translate("self", "Check box 1"))
        self.checkbox_2.setText(_translate("self", "Check Box 2"))
        self.error_val_lbl.setText(_translate("self", "04"))
        self.error_lbl.setText(_translate("self", "Error"))
        self.status_radio_btn_5.setText(_translate("self", "Status 5"))
        self.data_field_lbl.setText(_translate("self", "Data Fields"))
        self.random_btn_1.setText(_translate("self", "Demo"))
        self.random_btn_2.setText(_translate("self", "Graph"))
        self.random_btn_3.setText(_translate("self", "Add Field"))
        self.random_btn_4.setText(_translate("self", "Dials"))


 