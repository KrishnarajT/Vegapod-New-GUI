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
1. Open the latest ui file in qt designer
2. After editing, save the changes and navigate to where you saved the ui file and run: 
```
pyuic5 -x Vegapod_new_gui.ui -o _MainWindow.py                                                                                                              
```
3. Paste the Code from paste_this.py into the resulting .py file. 
4. Run `python Source.py` to run the code. 

# Screenshots
![](Screenshots/dashboard.gif)
![](Screenshots/graph.gif)
# DashBoard
![](Screenshots/dashboard.png)

# Graphs
![](Screenshots/graph.png)


# Credits
Base Code by [Krishnaraj](https://www.github.com/KrishnarajT)