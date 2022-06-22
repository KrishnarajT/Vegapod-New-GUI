# Vegapod-New-GUI
GUI for the new pod by Vegapod

# Pre-Requisites
1. Windows or Linux x86 64 bit
2. Python Installed on Your system with pip

# Installation
1. In your Virtual python environment, or native one, clone this repo, and in navigate there. Run  
```pip install -r requirements.txt```
2. Run `python Source.py` and that should launch the GUI. 


# Editing and Running

Note: You will only have to do this if you make changes to the ui file, and end up generating a new ui file. 
All the functions and stuff for multithreading and other backend code is in `Source.py` to allow for this to happen. 
But even after generating the new file, there are still some graph ui elements that the QT Generator file wont be able to produce. 
So you have to add those things at the right place. It is a hassle for sure. But it lets you edit the UI anyway that you want in the 
QT Generator, and still be able to run backend code safely. If this approach doesnt end up working and causes a lot of problems, revert back 
to an older commit.

1. Open the latest ui file in qt designer
2. After editing, save the changes and navigate to where you saved the ui file and run: 
`pyuic5 -x Vegapod_new_gui.ui -o _MainWindow.py`
3. Go to the UI_MainWindow Class which will be somewhere around line 14 in the newly generated file, and change 
`class Ui_MainWindow(object):` to `class Ui_MainWindow(QMainWindow, object):`
4. Paste the Code from paste_this.py into the resulting .py file. 
5. Run `python Source.py` to run the code. 

# Screenshots
![](Screenshots/dashboard.gif)
![](Screenshots/graph.gif)
# DashBoard
![](Screenshots/dashboard.png)

# Graphs
![](Screenshots/graph.png)


# Credits
Base Code by [Krishnaraj](https://www.github.com/KrishnarajT)