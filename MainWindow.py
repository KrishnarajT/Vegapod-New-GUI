



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys, os
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import time
from datetime import datetime



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list, list, float, int)
    gimme_values = pyqtSignal()

    def __init__(self, direction_text, step_val, end_val, interval_val):
        super().__init__()
        if direction_text == 'Forward':
            self.direction = 1
        else: self.direction = str(2)
        
        self.step_val = str(step_val)
        self.end_val = str(end_val)
        self.interval_val = str(interval_val)

    def run(self):
        print('motor code was invoked. ')
        
                
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.bind((socket.gethostname(), 1234))
        # s.listen(5)
        # clientsocket, address = s.accept()
        # print(f"connection from {address} has been established!")

        # clientsocket.send(bytes(self.direction, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.end_val, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.step_val, "utf-8"))
        # time.sleep(0.5)
        # clientsocket.send(bytes(self.interval_val, "utf-8"))
        # time.sleep(0.5)
            
        # s.close()
        # clientsocket.close
        # clientsocket.detach
        # time.sleep(1)        
        
        # #Connecting as client
        # a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # a.connect(('169.254.201.77', 1234))
        # print(f"connection from {address} has been established AGAIN as client !!!")

        # Take values for approx 20/25 seconds
        x = time.time()
        samay = 0
        while (samay < 7):
            b = time.time()
            samay = b - x
            print("inside recv loop")
            
            ### RECEIVING VALUES FROM PI and PARSING JSON

            # Taking data from the PI as a dict. 
            # raw_data = a.recv(1024)
            # if not raw_data:
            #     break;
            # raw_data = raw_data.decode("utf-8")

            # raw_data = json.loads(raw_data) # is now a dictionary. 

            # accel_data = raw_data['Acceleration']
            # gyro_data = raw_data['Gyroscope']
            # rpm_data = raw_data['RPM']
            # pressure_data = raw_data['Pressure']
            
            ### DUMMY VALUES  ###
            
            accel_data = [datetime.today().second * 2, datetime.today().second - 1, datetime.today().second]
            gyro_data = [datetime.today().second * 5, datetime.today().second, datetime.today().second * 7]
            rpm_data = 5000
            pressure_data = 100.00

            
            ### Sending values to GUI for updating ###
            
            self.progress.emit(accel_data, gyro_data, pressure_data, rpm_data)
            time.sleep(0.1)
            
            
            
        
        print("Session finished...")
                
        self.finished.emit()

    def stop_immediately(self):
        # Maybe ask the pi to break? 
        print('breaking. ')
        # self.maybeconnectionserver.close() and b4 that send break. 
        self.finished.emit()



class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("NEW POD GUI")
        self.resize(1920, 1080)
        self.setupUi()

        # # Defining basic values

        # self.start_value = 1
        # self.end_value = 20
        # self.step_value = 5
        # self.interval = 500
        
    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self.direction_combo_box.currentText(), int(self.step_value_line_edit.text()),\
            int(self.end_value_line_edit.text()), int(self.interval_line_edit.text()))
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.worker.gimme_values.connect(self.give_val)
        self.stop_signal.connect(self.worker.stop_immediately)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        # self.longRunningBtn.setEnabled(False)
        # self.thread.finished.connect(
        #     lambda: self.longRunningBtn.setEnabled(True)
        # )
        # self.thread.finished.connect(
        #     lambda: self.stepLabel.setText("Long-Running Step: 0")
        # )
    
    def stop_thread(self):
        self.stop_signal.emit()
    
    def give_val(self):
        return 1
        
    def start_pod(self):
        
        
        if 'Forward' == self.direction_combo_box.currentText():
            self.start_value = 1
        else: self.start_value = 2
        
        self.end_value = self.end_value_line_edit.text()
        self.step_value = self.step_value_line_edit.text()
        self.end_value = self.end_value_line_edit.text()
        self.interval = self.interval_line_edit.text()
        
        # Calling the function to run the motors. 
        mtcr.input_and_control(self.start_value, self.end_value, self.step_value, self.interval)

        # # switching tab to data tab
        # self.navigation_tab_widget.setCurrentIndex(2)
        
        
        # self.thread = QThread()
        # self.worker = Worker(parent=self)
        # self.worker.asx.connect(self.updateit)
        # # self.stop_signal.connect(self.worker.stop)  # connect stop signal to worker stop method
        # # self.worker.moveToThread(self.thread)

        # # self.thread.started.connect(lambda: self.worker.do_work(self.navigation_tab_widget, self.acc_x_value_lbl))
        # # self.worker.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        # # self.worker.finished.connect(self.worker.deleteLater)  # connect the workers finished signal to clean up worker
        # # self.thread.finished.connect(self.thread.deleteLater)  # connect threads finished signal to clean up thread

        # # self.thread.finished.connect(self.worker.stop)
        # self.thread.start()

    def stop_pod(self):
        self.stop_signal.emit()

    def reportProgress(self, n, b, p, r):
        self.navigation_tab_widget.setCurrentIndex(2)
        self.step_value_lbl.setText(f"Long-Running Step: {n[0]}")
        self.gyro_x_value_lbl.setText(str(round(n[0], 3)))
        self.gyro_y_value_lbl.setText(str(round(n[1], 3)))
        self.gyro_z_value_lbl.setText(str(round(n[2], 3)))        
        self.acc_x_value_lbl.setText(str(round(b[0], 3)))
        self.acc_y_value_lbl.setText(str(round(b[1], 3)))
        self.acc_z_value_lbl.setText(str(round(b[2], 3))) 
        self.pressure_value_lbl.setText(str(p))
        self.rpm_value_lbl.setText(str(r))

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.MainFrame = QtWidgets.QFrame(self.centralwidget)
        self.MainFrame.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.MainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MainFrame.setObjectName("MainFrame")
        self.progress_bar = QtWidgets.QProgressBar(self.MainFrame)
        self.progress_bar.setGeometry(QtCore.QRect(270, 620, 1600, 31))
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.data_fields_list_widget = QtWidgets.QListWidget(self.MainFrame)
        self.data_fields_list_widget.setGeometry(QtCore.QRect(0, 49, 250, 1031))
        self.data_fields_list_widget.setObjectName("data_fields_list_widget")
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.data_fields_list_widget.addItem(item)
        self.acc_graph_frame = QtWidgets.QFrame(self.MainFrame)
        self.acc_graph_frame.setGeometry(QtCore.QRect(1150, 80, 711, 171))
        self.acc_graph_frame.setStyleSheet("background-color: rgb(153, 193, 241);")
        self.acc_graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.acc_graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.acc_graph_frame.setObjectName("acc_graph_frame")
        self.velo_graph_frame = QtWidgets.QFrame(self.MainFrame)
        self.velo_graph_frame.setGeometry(QtCore.QRect(1150, 350, 711, 171))
        self.velo_graph_frame.setStyleSheet("background-color: rgb(143, 240, 164);")
        self.velo_graph_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.velo_graph_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.velo_graph_frame.setObjectName("velo_graph_frame")
        self.current_dial = QtWidgets.QDial(self.MainFrame)
        self.current_dial.setGeometry(QtCore.QRect(560, 80, 241, 181))
        self.current_dial.setObjectName("current_dial")
        self.acc_dial = QtWidgets.QDial(self.MainFrame)
        self.acc_dial.setGeometry(QtCore.QRect(290, 270, 361, 311))
        self.acc_dial.setObjectName("acc_dial")
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
        self.actuator_box_1 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_1.setGeometry(QtCore.QRect(310, 720, 91, 81))
        self.actuator_box_1.setStyleSheet("background-color: rgb(246, 97, 81);")
        self.actuator_box_1.setText("")
        self.actuator_box_1.setObjectName("actuator_box_1")
        self.actuator_box_2 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_2.setGeometry(QtCore.QRect(410, 720, 91, 81))
        self.actuator_box_2.setStyleSheet("background-color: rgb(246, 97, 81);")
        self.actuator_box_2.setText("")
        self.actuator_box_2.setObjectName("actuator_box_2")
        self.actuator_box_4 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_4.setGeometry(QtCore.QRect(310, 810, 91, 81))
        self.actuator_box_4.setStyleSheet("background-color: rgb(143, 240, 164);")
        self.actuator_box_4.setText("")
        self.actuator_box_4.setObjectName("actuator_box_4")
        self.actuator_box_3 = QtWidgets.QLabel(self.MainFrame)
        self.actuator_box_3.setGeometry(QtCore.QRect(410, 810, 91, 81))
        self.actuator_box_3.setStyleSheet("background-color: rgb(143, 240, 164);")
        self.actuator_box_3.setText("")
        self.actuator_box_3.setObjectName("actuator_box_3")
        self.actuator_lbl = QtWidgets.QLabel(self.MainFrame)
        self.actuator_lbl.setGeometry(QtCore.QRect(290, 670, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.actuator_lbl.setFont(font)
        self.actuator_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.actuator_lbl.setObjectName("actuator_lbl")
        self.launch_btn = QtWidgets.QPushButton(self.MainFrame)
        self.launch_btn.setGeometry(QtCore.QRect(1150, 690, 261, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.launch_btn.setFont(font)
        self.launch_btn.setObjectName("launch_btn")
        self.brake_btn = QtWidgets.QPushButton(self.MainFrame)
        self.brake_btn.setGeometry(QtCore.QRect(1150, 850, 591, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.brake_btn.setFont(font)
        self.brake_btn.setObjectName("brake_btn")
        self.arm_btn = QtWidgets.QPushButton(self.MainFrame)
        self.arm_btn.setGeometry(QtCore.QRect(1480, 690, 251, 141))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.arm_btn.setFont(font)
        self.arm_btn.setObjectName("arm_btn")
        self.current_lbl = QtWidgets.QLabel(self.MainFrame)
        self.current_lbl.setGeometry(QtCore.QRect(600, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.current_lbl.setFont(font)
        self.current_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.current_lbl.setObjectName("current_lbl")
        self.acc_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_lbl.setGeometry(QtCore.QRect(340, 210, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.acc_lbl.setFont(font)
        self.acc_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_lbl.setObjectName("acc_lbl")
        self.comm_lbl = QtWidgets.QLabel(self.MainFrame)
        self.comm_lbl.setGeometry(QtCore.QRect(270, 910, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.comm_lbl.setFont(font)
        self.comm_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.comm_lbl.setObjectName("comm_lbl")
        self.velo_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_lbl.setGeometry(QtCore.QRect(760, 210, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.velo_lbl.setFont(font)
        self.velo_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_lbl.setObjectName("velo_lbl")
        self.acc_graph_lbl = QtWidgets.QLabel(self.MainFrame)
        self.acc_graph_lbl.setGeometry(QtCore.QRect(1340, 20, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.acc_graph_lbl.setFont(font)
        self.acc_graph_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.acc_graph_lbl.setObjectName("acc_graph_lbl")
        self.velo_grpah_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_grpah_lbl.setGeometry(QtCore.QRect(1330, 280, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.velo_grpah_lbl.setFont(font)
        self.velo_grpah_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.velo_grpah_lbl.setObjectName("velo_grpah_lbl")
        self.comm_status_radio_btn = QtWidgets.QRadioButton(self.MainFrame)
        self.comm_status_radio_btn.setGeometry(QtCore.QRect(360, 950, 148, 28))
        self.comm_status_radio_btn.setChecked(True)
        self.comm_status_radio_btn.setAutoExclusive(False)
        self.comm_status_radio_btn.setObjectName("comm_status_radio_btn")
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
        self.velo_dial = QtWidgets.QDial(self.MainFrame)
        self.velo_dial.setGeometry(QtCore.QRect(700, 270, 361, 311))
        self.velo_dial.setObjectName("velo_dial")
        self.velo_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.velo_val_lbl.setGeometry(QtCore.QRect(810, 350, 141, 111))
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
        self.status_radio_btn_2 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_2.setGeometry(QtCore.QRect(1300, 950, 148, 28))
        self.status_radio_btn_2.setCheckable(True)
        self.status_radio_btn_2.setChecked(False)
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
        self.spin_box_1 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_1.setGeometry(QtCore.QRect(1300, 550, 75, 32))
        self.spin_box_1.setObjectName("spin_box_1")
        self.spin_box_2 = QtWidgets.QSpinBox(self.MainFrame)
        self.spin_box_2.setGeometry(QtCore.QRect(1770, 550, 75, 32))
        self.spin_box_2.setObjectName("spin_box_2")
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
        self.error_val_lbl = QtWidgets.QLabel(self.MainFrame)
        self.error_val_lbl.setGeometry(QtCore.QRect(1760, 680, 111, 111))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(55)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
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
        self.status_radio_btn_5 = QtWidgets.QRadioButton(self.MainFrame)
        self.status_radio_btn_5.setGeometry(QtCore.QRect(1760, 950, 148, 28))
        self.status_radio_btn_5.setChecked(True)
        self.status_radio_btn_5.setAutoExclusive(False)
        self.status_radio_btn_5.setObjectName("status_radio_btn_5")
        self.data_field_lbl = QtWidgets.QLabel(self.MainFrame)
        self.data_field_lbl.setGeometry(QtCore.QRect(0, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.data_field_lbl.setFont(font)
        self.data_field_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.data_field_lbl.setObjectName("data_field_lbl")
        self.random_btn_1 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_1.setGeometry(QtCore.QRect(1150, 980, 154, 32))
        self.random_btn_1.setObjectName("random_btn_1")
        self.random_btn_2 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_2.setGeometry(QtCore.QRect(1350, 980, 154, 32))
        self.random_btn_2.setObjectName("random_btn_2")
        self.random_btn_3 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_3.setGeometry(QtCore.QRect(1540, 980, 154, 32))
        self.random_btn_3.setObjectName("random_btn_3")
        self.random_btn_4 = QtWidgets.QPushButton(self.MainFrame)
        self.random_btn_4.setGeometry(QtCore.QRect(1730, 980, 154, 32))
        self.random_btn_4.setObjectName("random_btn_4")

        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "NEW POD GUI"))
        __sortingEnabled = self.data_fields_list_widget.isSortingEnabled()
        self.data_fields_list_widget.setSortingEnabled(False)
        item = self.data_fields_list_widget.item(0)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(1)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(2)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(3)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(4)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(5)
        item.setText(_translate("self", "New Item"))
        item = self.data_fields_list_widget.item(6)
        item.setText(_translate("self", "New Item"))
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
        self.velo_grpah_lbl.setText(_translate("self", "Velocity Time Curve"))
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
        self.random_btn_1.setText(_translate("self", "Button 1"))
        self.random_btn_2.setText(_translate("self", "Button 2"))
        self.random_btn_3.setText(_translate("self", "Button 3"))
        self.random_btn_4.setText(_translate("self", "Button 4"))


