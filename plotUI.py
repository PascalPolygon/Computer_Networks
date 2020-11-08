import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import matplotlib
import random
import MAC_module as MAC_module
import time
matplotlib.use('Qt5Agg')

MAC = MAC_module.MAC_network()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Simple MAC protol simulation (Project 1)")
        self.setGeometry(200, 200, 2000, 2000)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.centralWidget = self.setCentralWidget(self.canvas)

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

        self.Button1 = QtWidgets.QPushButton(self)
        self.Button1.setGeometry(QtCore.QRect(1100, 100, 89, 25))
        self.Button1.setObjectName("Button1")
        self.Button1.setText("Run Simulation")

        self.Button1.clicked.connect(self.onSubmit)

        self.statusLabel = QtWidgets.QLabel(self)
        # self.statusLabel.setText("Ready.")
        self.statusLabel.move(1100, 155)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("# of time slots")
        self.label1.move(100, 50)

        self.spinBox1 = QtWidgets.QSpinBox(self)
        self.spinBox1.setGeometry(QtCore.QRect(100, 100, 48, 26))
        self.spinBox1.setRange(1, 2500)
        self.spinBox1.setObjectName("spinBox1")

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("# of nodes")
        self.label2.move(350, 50)

        self.spinBox2 = QtWidgets.QSpinBox(self)
        self.spinBox2.setGeometry(QtCore.QRect(350, 100, 48, 26))
        self.spinBox2.setRange(1, 2500)
        self.spinBox2.setObjectName("spinBox2")

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("# of sims to run")
        self.label3.move(550, 50)

        self.spinBox3 = QtWidgets.QSpinBox(self)
        self.spinBox3.setGeometry(QtCore.QRect(550, 100, 48, 26))
        self.spinBox3.setRange(1, 2500)
        self.spinBox3.setObjectName("spinBox3")

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText("# of Samples to plot")
        self.label4.move(790, 50)

        self.spinBox4 = QtWidgets.QSpinBox(self)
        self.spinBox4.setGeometry(QtCore.QRect(790, 100, 48, 26))
        self.spinBox4.setRange(1, 2500)
        self.spinBox4.setObjectName("spinBox4")

        self.spinBox1.setValue(20)
        self.spinBox2.setValue(6)
        self.spinBox3.setValue(100)
        self.spinBox4.setValue(100)

        self.resizeItems()
        # self.retranslateUi(MainWindow)
        # self.update_plot()
        self.show()

    def resizeItems(self):
        self.label1.adjustSize()
        self.label2.adjustSize()
        self.label3.adjustSize()
        self.label4.adjustSize()
        self.statusLabel.adjustSize()
        self.spinBox1.adjustSize()
        self.spinBox2.adjustSize()
        self.spinBox3.adjustSize()
        self.spinBox4.adjustSize()
        self.Button1.adjustSize()

    def onSubmit(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.draw()
        # self.statusLabel.setText("Running...")
        self.resizeItems()
        self.update_network()
        # print(f"T: {MAC.T}, N: {MAC.N}, Nsims: {MAC.Nsims}, Samples: {MAC.Samples}")
        meanS, s = self.run_simulation()
        self.plot_res(meanS/MAC.T, s)

    def update_network(self):
        T = self.spinBox1.value()
        N = self.spinBox2.value()
        Nsims = self.spinBox3.value()
        Samples = self.spinBox4.value()

        MAC.T = T
        MAC.N = N
        MAC.Nsims = Nsims
        MAC.Samples = Samples
        MAC.probs = np.linspace(0, 1, Samples)
        # self.statusLabel.setText("Running...")
        self.show()

    def run_simulation(self):
        # Theoretical results
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.draw()
        s = MAC.computeThrRes()
        print("Running simulation...")
        start_time = time.time()
        meanS = MAC.computeSimRes()
        print("Simulation done in %.2f seconds." % (time.time()-start_time))
        self.statusLabel.setText(
            "Simulation done in %.2f seconds." % (time.time()-start_time))
        self.resizeItems()
        return meanS, s

    def plot_res(self, meanS, s):
        # self.plt.close("all")
        print(f"Simulation result for {MAC.Nsims} simulations")

        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(MAC.probs, meanS,
                              label=f"Result for {MAC.Nsims} simulations")
        self.canvas.axes.scatter(MAC.probs[np.argmax(meanS)],
                                 meanS[np.argmax(meanS)], s=100, label=f"Simulation max efficiencty p={MAC.probs[np.argmax(meanS)]:.4f}")

        self.canvas.axes.plot(MAC.probs, s, label='Theoretical (True) result')
        self.canvas.axes.scatter(MAC.probs[np.argmax(s)], s[np.argmax(s)],
                                 s=100, label=f"Theoretical max efficiency p={MAC.probs[np.argmax(s)]:.4f}")

        self.canvas.axes.set_title(
            'p Vs. Proportion of successful transmission slots')
        self.canvas.axes.set_xlabel('Success probability for one node (p)')
        self.canvas.axes.set_ylabel(
            'Proportion of successful transmission slots')
        self.canvas.axes.legend()
        self.canvas.draw()
