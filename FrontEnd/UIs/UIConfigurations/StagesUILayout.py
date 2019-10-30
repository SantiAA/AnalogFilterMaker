from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QLabel, QRadioButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from FrontEnd.UIs.graphwidget import GraphWidget


class StagesUILayout(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        groupbox = QGroupBox("Stages")
        groupbox.setCheckable(False)
        groupbox.setStyleSheet("color:rgb(255, 255, 255)")
        hbox.addWidget(groupbox)
        self.group_box_layout = QHBoxLayout()
        groupbox.setLayout(self.group_box_layout)
        self.w_width = groupbox.frameGeometry().width()
        self.stages = []


    def add_stage(self):
        new_stage = DefaultStageUI(len(self.stages)+1, self.w_width)
        self.stages.append(new_stage)
        self.group_box_layout.addWidget(new_stage)


    def get_number_of_checked(self):
        checked = 0
        for stage in self.stages:
            if stage.is_checked():
                checked +=1

        return checked

    def get_checked_array(self):
        checked_array = []
        for stage in self.stages:
            if stage.is_checked():
                checked_array.append(stage)
        return checked_array

    def delete_selected_stages(self):
        for stage in self.get_checked_array():
            self.stages.remove(stage)
            stage.setParent(None)

        #Renaming
        i= 1
        for active_stage in self.stages:
            active_stage.set_id(i)
            i+=1


class DefaultStageUI(QWidget):
    def __init__(self, id, width):
        QWidget.__init__(self)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.id = id
        self.width = width
        self.label = QLabel()
        self.set_label_text()
        self.name = self.label.text()

        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.label.setMargin(0)
        self.label.setContentsMargins(0,0,0,0)
        vbox.addWidget(self.label)
        self.graphWidget = StagesGraph()

        self.graphWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.__update_size__()
        vbox.addWidget(self.graphWidget)
        self.radioButton = QRadioButton("")

        self.radioButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        vbox.addWidget(self.radioButton)

    def __update_size__(self):
        self.graphWidget.setFixedWidth(int(self.width / 3.3))
        self.graphWidget.setFixedHeight(int(self.width / 3.3))
        self.graphWidget.setContentsMargins(0,0,0,0)

    def set_id(self, id):
        self.id = id
        self.set_label_text()

    def set_label_text(self):
        self.label.setText("Stage "+ str(self.id))

    def is_checked(self):
        return self.radioButton.isChecked()

class StagesGraph(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)


        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.figure.tight_layout()
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.axes.axis('off')
        self.setLayout(vertical_layout)




