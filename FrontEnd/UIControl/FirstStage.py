from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class FirstStage(QMainWindow):

    def __init__(self, ui_manager):  # Conecta los componentes del .ui realizado en QT con el programa en python
        self.ui_manager = ui_manager


    def start(self):
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/firststage.ui', self)
        self.setWindowTitle("Instrument Automation")
        self.show()
        self.graphButton.clicked.connect(self.graph)
        self.sliderRange.valueChanged.connect(self.slider_changed)
        self.comboGraph.currentIndexChanged.connect(self.graph)
        self.graph_widget = self.graphWidget  # GraphWidget instance.

    def graph(self):
        self.graph_widget.canvas.axes.clear()
        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
        self.graph_widget.canvas.axes.scatter([0,10,15,20,25],
                                         [40,50,60,90,120],
                                         color='b')
        self.graph_widget.canvas.axes.set_xscale('log')
        self.graph_widget.canvas.axes.grid(True, which="both")

        self.graph_widget.canvas.draw()  # Redraws
    def slider_changed(self):
        val = self.sliderRange.value()
        self.sliderValue.setText(str(val))

