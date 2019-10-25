from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


# GraphWidget. Promoted class from the widgets used in UIGraphPreview. Associated with a QWidget instance.
class GraphWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.x_label = "X"
        self.y_label = "Y"
        self.title = " "
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar(self.canvas, self)  # Toolbar to work on the graphs
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)  # Adding toolbar to the widget

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        self.setLayout(vertical_layout)
