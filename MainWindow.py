



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys, os
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import time
from datetime import datetime
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint


red_color = "background-color: rgb(246, 97, 81);"
green_color = "background-color: rgb(143, 240, 164);"


class Worker(QObject):
    finished_1 = pyqtSignal()
    progress_1 = pyqtSignal(int)
    finished_2 = pyqtSignal()
    progress_2 = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Basic variables can be defined here. 

    def function_thread_1(self):
        # This will just run everything for demo purposes. 
        for i in range(60):
            print('running the task')
            time.sleep(0.1)
            self.progress_1.emit(i)
        self.finished_1.emit()


    def function_thread_2(self):
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.progress_2.emit)
        self.timer.start()
        
        # for i in range(5):
        #     print('running the task')
        #     time.sleep(1)
        #     self.progress_2.emit(i)
        # self.finished_2.emit()


class Ui_MainWindow(QMainWindow): 
       
    def __init__(self):
        super().__init__()
        self.setObjectName("NEW POD GUI")
        self.resize(1920, 1080)
        self.setupUi()

    def runLongTask_with_thread_1(self):
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
        self.worker.progress_1.connect(self.reportProgress_thread_1)
        # self.worker.gimme_values.connect(self.give_val)
        # self.stop_signal.connect(self.worker.stop_immediately)
        
        # Start the thread
        self.thread.start()
        
        self.random_btn_1.setEnabled(False)
        
        # Final resets
        self.thread.finished.connect(
            lambda: self.random_btn_1.setEnabled(True)
        )       

    def reportProgress_thread_1(self, i):
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
        self.worker_2.progress_2.connect(self.update_plot_data)
        # self.worker_2.gimme_values.connect(self.give_val)
        # self.stop_signal.connect(self.worker_2.stop_immediately)
        
        # Start the thread_2
        self.thread_2.start()
        self.random_btn_2.setEnabled(False)
        
        # Final resets
        self.thread_2.finished.connect(
            lambda: self.random_btn_2.setEnabled(True)
        )
        
        self.graphWidget = pg.PlotWidget()
        # self.setCentralWidget(self.graphWidget)
        self.graphWidget.setParent(self.acc_graph_frame)

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        
        
    def reportProgress_thread_2(self, i):
        print('Reported Progress from two', i)

    def makegraph(self):
        self.graphWidget = pg.PlotWidget(self.acc_graph_frame)
        self.setCentralWidget(self.graphWidget)
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points

        self.graphWidget.setBackground('w')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        # self.data_line.setGeometry(0, 0, 100, 100)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    def update_plot_data(self):
    
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append( randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.


    def setupUi(self):
        
        # BASIC WIDGET STUFF
        # -----------------------------------------------------------------------------------------------------
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        self.MainFrame = QtWidgets.QFrame(self.centralwidget)
        self.MainFrame.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        # -----------------------------------------------------------------------------------------------------


        # PROGRESS BAR
        # -----------------------------------------------------------------------------------------------------
        self.progress_bar = QtWidgets.QProgressBar(self.MainFrame)
        self.progress_bar.setGeometry(QtCore.QRect(270, 620, 1600, 31))
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
        
        
        # ACCELERATION GRAPH
        # -----------------------------------------------------------------------------------------------------
        self.acc_graph_frame = QtWidgets.QFrame(self.MainFrame)
        self.acc_graph_frame.setGeometry(QtCore.QRect(1150, 80, 711, 171))
        self.acc_graph_frame.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.acc_graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.acc_graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.acc_graph_frame.setObjectName("acc_graph_frame")


        self.acc_graph_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_graph_lbl.setGeometry(QtCore.QRect(1340, 20, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.acc_graph_lbl.setFont(font)
        self.acc_graph_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_graph_lbl.setObjectName("acc_graph_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        # VELOCITY GRAPH
        # -----------------------------------------------------------------------------------------------------
        self.velo_graph_frame = QtWidgets.QFrame(self.MainFrame)
        self.velo_graph_frame.setGeometry(QtCore.QRect(1150, 350, 711, 171))
        self.velo_graph_frame.setStyleSheet("background-color: rgb(143, 240, 164);")
        self.velo_graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.velo_graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.velo_graph_frame.setObjectName("velo_graph_frame")


        self.velo_graph_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_graph_lbl.setGeometry(QtCore.QRect(1330, 280, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.velo_graph_lbl.setFont(font)
        self.velo_graph_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_graph_lbl.setObjectName("velo_graph_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        
        # DIALS / GAUGES 
        # -----------------------------------------------------------------------------------------------------
        
        # CURRENT --------------------------------------------------------------
        self.current_dial = QtWidgets.QDial(self.MainFrame)
        self.current_dial.setGeometry(QtCore.QRect(560, 80, 241, 181))
        self.current_dial.setObjectName("current_dial")

        self.current_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_val_lbl.setGeometry(QtCore.QRect(640, 120, 81, 71))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        self.current_val_lbl.setFont(font)
        self.current_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_val_lbl.setWordWrap(True)
        self.current_val_lbl.setObjectName("current_val_lbl")
        self.current_unit_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_unit_lbl.setGeometry(QtCore.QRect(640, 170, 81, 21))
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.current_unit_lbl.setFont(font)
        self.current_unit_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_unit_lbl.setObjectName("current_unit_lbl")
        
        self.current_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_lbl.setGeometry(QtCore.QRect(600, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.current_lbl.setFont(font)
        self.current_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_lbl.setObjectName("current_lbl")
        # ----------------------------------------------------------- 
        
        # ACCELERATION -----------------------------------------------------------
        self.acc_dial = QtWidgets.QDial(self.MainFrame)
        self.acc_dial.setGeometry(QtCore.QRect(290, 270, 361, 311))
        self.acc_dial.setObjectName("acc_dial")
        
        self.acc_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_lbl.setGeometry(QtCore.QRect(340, 210, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.acc_lbl.setFont(font)
        self.acc_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_lbl.setObjectName("acc_lbl")
        
        self.acc_unit_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_unit_lbl.setGeometry(QtCore.QRect(410, 440, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(22)
        self.acc_unit_lbl.setFont(font)
        self.acc_unit_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_unit_lbl.setObjectName("acc_unit_lbl")
        self.acc_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_val_lbl.setGeometry(QtCore.QRect(400, 350, 141, 111))
        
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
        self.velo_dial.setGeometry(QtCore.QRect(700, 270, 361, 311))
        self.velo_dial.setObjectName("velo_dial")
        self.velo_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_val_lbl.setGeometry(QtCore.QRect(810, 350, 141, 111))
        
        self.velo_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_lbl.setGeometry(QtCore.QRect(760, 210, 251, 51))
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
        self.velo_unit_lbl.setGeometry(QtCore.QRect(820, 440, 111, 31))
        
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
        self.temp_val_lbl_1.setGeometry(QtCore.QRect(590, 730, 241, 41))
        self.temp_val_lbl_1.setObjectName("temp_val_lbl_1")
        self.temp_val_lbl_2 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_2.setGeometry(QtCore.QRect(590, 770, 241, 41))
        self.temp_val_lbl_2.setObjectName("temp_val_lbl_2")
        self.temp_val_lbl_3 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_3.setGeometry(QtCore.QRect(590, 810, 241, 41))
        self.temp_val_lbl_3.setObjectName("temp_val_lbl_3")
        self.temp_val_lbl_4 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_4.setGeometry(QtCore.QRect(590, 850, 241, 41))
        self.temp_val_lbl_4.setObjectName("temp_val_lbl_4")
        self.temp_val_lbl_5 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_5.setGeometry(QtCore.QRect(590, 890, 241, 41))
        self.temp_val_lbl_5.setObjectName("temp_val_lbl_5")
        self.temp_val_lbl_6 = QtWidgets.QLabel(self.MainFrame)
        self.temp_val_lbl_6.setGeometry(QtCore.QRect(590, 930, 241, 41))
        self.temp_val_lbl_6.setObjectName("temp_val_lbl_6")
        self.temp_lbl = QtWidgets.QLabel(self.MainFrame)
        self.temp_lbl.setGeometry(QtCore.QRect(570, 670, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.temp_lbl.setFont(font)
        self.temp_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_lbl.setObjectName("temp_lbl")
        # -----------------------------------------------------------------------------------------------------
        
        
        # PRESSURE DATA FIELDS
        # -----------------------------------------------------------------------------------------------------
        self.pres_val_lbl_2 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_2.setGeometry(QtCore.QRect(860, 770, 241, 41))
        self.pres_val_lbl_2.setObjectName("pres_val_lbl_2")
        self.pressure_lbl = QtWidgets.QLabel(self.MainFrame)
        self.pressure_lbl.setGeometry(QtCore.QRect(820, 670, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pressure_lbl.setFont(font)
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.pressure_lbl.setObjectName("pressure_lbl")
        self.pres_val_lbl_3 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_3.setGeometry(QtCore.QRect(860, 810, 241, 41))
        self.pres_val_lbl_3.setObjectName("pres_val_lbl_3")
        self.pres_val_lbl_5 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_5.setGeometry(QtCore.QRect(860, 890, 241, 41))
        self.pres_val_lbl_5.setObjectName("pres_val_lbl_5")
        self.pres_val_lbl_1 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_1.setGeometry(QtCore.QRect(860, 730, 241, 41))
        self.pres_val_lbl_1.setObjectName("pres_val_lbl_1")
        self.pres_val_lbl_6 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_6.setGeometry(QtCore.QRect(860, 930, 241, 41))
        self.pres_val_lbl_6.setObjectName("pres_val_lbl_6")
        self.pres_val_lbl_4 = QtWidgets.QLabel(self.MainFrame)
        self.pres_val_lbl_4.setGeometry(QtCore.QRect(860, 850, 241, 41))
        self.pres_val_lbl_4.setObjectName("pres_val_lbl_4")
        # -----------------------------------------------------------------------------------------------------
        
        # ACTUATOR BOX
        # -----------------------------------------------------------------------------------------------------
        red_color = "background-color: rgb(246, 97, 81);"
        green_color = "background-color: rgb(143, 240, 164);"
        
        self.actuator_box_1 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_1.setGeometry(QtCore.QRect(310, 720, 91, 81))
        self.actuator_box_1.setStyleSheet(red_color) # This is how you set the color
        self.actuator_box_1.setText("")
        self.actuator_box_1.setObjectName("actuator_box_1")
        self.actuator_box_2 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_2.setGeometry(QtCore.QRect(410, 720, 91, 81))
        self.actuator_box_2.setStyleSheet(red_color) 
        self.actuator_box_2.setText("")
        self.actuator_box_2.setObjectName("actuator_box_2")
        self.actuator_box_4 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_4.setGeometry(QtCore.QRect(310, 810, 91, 81))
        self.actuator_box_4.setStyleSheet(green_color)
        self.actuator_box_4.setText("")
        self.actuator_box_4.setObjectName("actuator_box_4")
        self.actuator_box_3 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_3.setGeometry(QtCore.QRect(410, 810, 91, 81))
        self.actuator_box_3.setStyleSheet(green_color)
        self.actuator_box_3.setText("")
        self.actuator_box_3.setObjectName("actuator_box_3")
        self.actuator_lbl = QtWidgets.QLabel(self.MainFrame)
        self.actuator_lbl.setGeometry(QtCore.QRect(290, 670, 241, 41))
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
        self.launch_btn.setGeometry(QtCore.QRect(1150, 690, 261, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.launch_btn.setFont(font)
        self.launch_btn.setObjectName("launch_btn")
        
        # BRAKE
        self.brake_btn = QtWidgets.QPushButton(self.MainFrame)
        self.brake_btn.setGeometry(QtCore.QRect(1150, 850, 591, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.brake_btn.setFont(font)
        self.brake_btn.setObjectName("brake_btn")
        
        # ARM
        self.arm_btn = QtWidgets.QPushButton(self.MainFrame)
        self.arm_btn.setGeometry(QtCore.QRect(1480, 690, 251, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.arm_btn.setFont(font)
        self.arm_btn.setObjectName("arm_btn")
        
        # Power Slider
        self.power_slider = QtWidgets.QSlider(self.MainFrame)
        self.power_slider.setGeometry(QtCore.QRect(1760, 900, 131, 21))
        self.power_slider.setOrientation(QtCore.Qt.Horizontal)
        self.power_slider.setObjectName("power_slider")
        self.power_lbl = QtWidgets.QLabel(self.MainFrame)
        self.power_lbl.setGeometry(QtCore.QRect(1740, 860, 161, 31))
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
        self.comm_lbl.setGeometry(QtCore.QRect(270, 910, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.comm_lbl.setFont(font)
        self.comm_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.comm_lbl.setObjectName("comm_lbl")
        self.comm_status_radio_btn = QtWidgets.QRadioButton(self.MainFrame)
        self.comm_status_radio_btn.setGeometry(QtCore.QRect(360, 950, 148, 28))
        self.comm_status_radio_btn.setChecked(True)
        self.comm_status_radio_btn.setAutoExclusive(False)
        self.comm_status_radio_btn.setObjectName("comm_status_radio_btn")
        # -----------------------------------------------------------------------------------------------------
        
        
        # STATUS LEDS as RADIO BUTTONS
        # -----------------------------------------------------------------------------------------------------
        self.status_radio_btn_2 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_2.setGeometry(QtCore.QRect(1300, 950, 148, 28))
        self.status_radio_btn_2.setCheckable(True)
        self.status_radio_btn_2.setChecked(True) # This is how you check them, or make them appear ON. 
        self.status_radio_btn_2.setAutoRepeat(False)
        self.status_radio_btn_2.setAutoExclusive(False)
        self.status_radio_btn_2.setObjectName("status_radio_btn_2")
        self.status_radio_btn_3 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_3.setGeometry(QtCore.QRect(1460, 950, 148, 28))
        self.status_radio_btn_3.setCheckable(True)
        self.status_radio_btn_3.setChecked(True)
        self.status_radio_btn_3.setAutoExclusive(False)
        self.status_radio_btn_3.setObjectName("status_radio_btn_3")
        self.status_radio_btn_1 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_1.setGeometry(QtCore.QRect(1160, 950, 148, 28))
        self.status_radio_btn_1.setChecked(True)
        self.status_radio_btn_1.setAutoExclusive(False)
        self.status_radio_btn_1.setObjectName("status_radio_btn_1")
        self.status_radio_btn_4 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_4.setGeometry(QtCore.QRect(1610, 950, 148, 28))
        self.status_radio_btn_4.setChecked(True)
        self.status_radio_btn_4.setAutoExclusive(False)
        self.status_radio_btn_4.setObjectName("status_radio_btn_4")
        self.status_radio_btn_5 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_5.setGeometry(QtCore.QRect(1760, 950, 148, 28))
        self.status_radio_btn_5.setChecked(True)
        self.status_radio_btn_5.setAutoExclusive(False)
        self.status_radio_btn_5.setObjectName("status_radio_btn_5")
        # -----------------------------------------------------------------------------------------------------
        
        
        # SPIN AND CHECK BOXES
        # -----------------------------------------------------------------------------------------------------
        self.spin_box_1 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_1.setGeometry(QtCore.QRect(1300, 550, 75, 32))
        self.spin_box_1.setObjectName("spin_box_1")
        self.spin_box_2 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_2.setGeometry(QtCore.QRect(1770, 550, 75, 32))
        self.spin_box_2.setObjectName("spin_box_2")
        
        self.spin_box_2_lbl = QtWidgets.QLabel(self.MainFrame)
        self.spin_box_2_lbl.setGeometry(QtCore.QRect(1610, 550, 161, 31))
        self.spin_box_2_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spin_box_2_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_2_lbl.setObjectName("spin_box_2_lbl")
        self.spin_box_1_lbl = QtWidgets.QLabel(self.MainFrame)
        self.spin_box_1_lbl.setGeometry(QtCore.QRect(1130, 550, 161, 31))
        self.spin_box_1_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spin_box_1_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_1_lbl.setObjectName("spin_box_1_lbl")
        
        
        self.checkbox_1 = QtWidgets.QCheckBox(self.MainFrame)
        self.checkbox_1.setGeometry(QtCore.QRect(1150, 650, 141, 28))
        self.checkbox_1.setObjectName("checkbox_1")
        self.checkbox_2 = QtWidgets.QCheckBox(self.MainFrame)
        self.checkbox_2.setGeometry(QtCore.QRect(1490, 650, 151, 28))
        self.checkbox_2.setObjectName("checkbox_2")
        # -----------------------------------------------------------------------------------------------------
        
        # ERRORS 
        # -----------------------------------------------------------------------------------------------------
        self.error_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.error_val_lbl.setGeometry(QtCore.QRect(1760, 680, 111, 111))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(55)
        font.setWeight(50)
        self.error_val_lbl.setFont(font)
        self.error_val_lbl.setStyleSheet("color: rgb(237, 51, 59);")
        self.error_val_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.error_val_lbl.setObjectName("error_val_lbl")
        self.error_lbl = QtWidgets.QLabel(self.MainFrame)
        self.error_lbl.setGeometry(QtCore.QRect(1750, 780, 141, 71))
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
        self.random_btn_1.setGeometry(QtCore.QRect(1150, 980, 154, 32))
        self.random_btn_1.setObjectName("random_btn_1")
        self.random_btn_1.clicked.connect(self.runLongTask_with_thread_1)
        
        self.random_btn_2 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_2.setGeometry(QtCore.QRect(1350, 980, 154, 32))
        self.random_btn_2.setObjectName("random_btn_2")
        self.random_btn_2.clicked.connect(self.runLongTask_with_thread_2)

        
        self.random_btn_3 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_3.setGeometry(QtCore.QRect(1540, 980, 154, 32))
        self.random_btn_3.setObjectName("random_btn_3")
        self.random_btn_3.clicked.connect(self.makegraph)
        
        self.random_btn_4 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_4.setGeometry(QtCore.QRect(1730, 980, 154, 32))
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
        self.acc_graph_lbl.setText(_translate("self", "Acceleration Time Curve"))
        self.velo_graph_lbl.setText(_translate("self", "Velocity Time Curve"))
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


 