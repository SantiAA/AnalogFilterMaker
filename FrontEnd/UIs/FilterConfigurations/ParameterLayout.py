from PyQt5 import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QSlider


class ParameterLayout (QHBoxLayout):
    def __init__(self, name, widget):
        QHBoxLayout.__init__(self)
        self.name = name
        self.widget = widget
        self.label = QLabel(self.name)
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.addWidget(self.label)
        self.addWidget(self.widget)


class DefaultNumberEdit(QLineEdit):
    def __init__(self, min=0, max=100, decimals=2):
        QLineEdit.__init__(self)
        self.onlyNum = QDoubleValidator()
        self.onlyNum.setRange(min, max, decimals)
        self.setValidator(self.onlyNum)
        self.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")


class DefaultSlider(QHBoxLayout):
    def __init__(self, min = 0, max = 100):
        QHBoxLayout.__init__(self)
        self.slider = QSlider()
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.label = QLabel(" ")
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.addWidget(self.label)
        self.addWidget(self.widget)
        self.slider.valueChanged.connect(self.slider_changed)

    def slider_changed(self):
        val = self.slider.value()
        self.label.setText(str(val))

