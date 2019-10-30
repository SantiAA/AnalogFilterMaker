from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QLabel, QRadioButton, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from FrontEnd.UIs.graphwidget import GraphWidget


class StagesUILayout(QWidget):
    def __init__(self,changed_selected_amount_callback):
        QWidget.__init__(self)
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        groupbox = QGroupBox("Stages")
        self.changed_selected_amount_callback = changed_selected_amount_callback
        groupbox.setCheckable(False)
        groupbox.setStyleSheet("color:rgb(255, 255, 255)")
        hbox.addWidget(groupbox)
        self.group_box_layout = QHBoxLayout()
        groupbox.setLayout(self.group_box_layout)
        self.w_width = groupbox.frameGeometry().width()
        self.stages = []


    def left_click(self):
        for stage in self.stages:
            stage.set_checked(False)

    def add_stage(self, stage, i):
        new_stage = DefaultStageUI(len(self.stages)+1, self.w_width, self.left_click, stage, i, self.changed_selected_amount_callback)
        self.stages.append(new_stage)
        self.group_box_layout.addWidget(new_stage)

    def delete_all_stages(self):
        for stage in self.stages:
            self.stages.remove(stage)
            stage.setParent(None)

    def get_number_of_checked(self):
        checked = 0
        for stage in self.stages:
            if stage.is_checked():
                checked +=1

        return checked

    def get_selected_ids_array(self):
        selected_ids_array = []
        for stage in self.stages:
            if stage.is_checked():
                selected_ids_array.append(stage.get_id())
        return selected_ids_array

    def get_checked_array(self):
        checked_array = []
        for stage in self.stages:
            if stage.is_checked():
                checked_array.append(stage)
        return checked_array

'''    def delete_selected_stages(self):
        for stage in self.get_checked_array():
            self.stages.remove(stage)
            stage.setParent(None)

        #Renaming
        i= 1
        for active_stage in self.stages:
            active_stage.set_id(i)
            i+=1'''




class DefaultStageUI(QWidget):
    def __init__(self, width, left_click_callback, stage, i, changed_selected_amount):
        QWidget.__init__(self)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.width = width
        self.stage = stage
        self.id = i
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
        self.radioButton = RightRadioButton(left_click_callback, changed_selected_amount)

        self.radioButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        vbox.addWidget(self.radioButton)

    def __update_size__(self):
        self.graphWidget.setFixedWidth(int(self.width / 3.3))
        self.graphWidget.setFixedHeight(int(self.width / 3.3))
        self.graphWidget.setContentsMargins(0,0,0,0)

    def get_id(self):
        return self.id

    def set_label_text(self):
        self.label.setText("Stage "+ str(self.id + 1))

    def is_checked(self):
        return self.radioButton.isChecked()

    def set_checked(self, checked):
        self.radioButton.setChecked(checked)


class RightRadioButton (QRadioButton):
    def __init__(self, left_click, changed_selected_amount_callback):
        QRadioButton.__init__(self)
        self.left_click = left_click
        self.changed_selected_amount_callback = changed_selected_amount_callback

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.left_click()
            self.setChecked(True)
            self.changed_selected_amount_callback()

        elif QMouseEvent.button() == Qt.RightButton:
            self.setChecked(not self.isChecked())
            print("Right Button Clicked")
            self.changed_selected_amount_callback()

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


class UIStageData(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.enabled_text = ""



class HorizontalParameter(QWidget):
    def __init__(self, title, value, units):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.label_title = QLabel(title)
        self.value_label = QLabel(value)
        self.units_label = QLabel(units)
        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.units_label)






