
# Paste this code *** AT THE END OF SetupUI() FUNCTION OF NEWLY GENERATED MAINWINDOW.PY, BUT BEFORE THE LAST 3 LINES ***

# These are just connecting the buttons to the functions, which you will change eventually. 
self.random_btn_1.clicked.connect(self.runLongTask_with_thread_1)
self.random_btn_2.clicked.connect(self.gen_Graph)
self.random_btn_3.clicked.connect(self.runLongTask_with_thread_2)

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

# Adding these things to the vertial layout. 

self.vertical_layout.addWidget(self.velo_graph_lbl)
self.vertical_layout.addWidget(self.velo_graph_pg_widget)
self.vertical_layout.addWidget(self.acc_graph_lbl)
self.vertical_layout.addWidget(self.acc_graph_pg_widget)



# PASTE THIS CODE AT THE TOP OF THE NEWLY GENERATED MAINWINDOW.PY FUNCTION


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

