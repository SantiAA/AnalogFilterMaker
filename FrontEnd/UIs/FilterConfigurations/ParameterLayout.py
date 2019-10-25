from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QSlider, QWidget, QSizePolicy, QDoubleSpinBox


class ParameterLayout (QWidget):
    def __init__(self, name, widget):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.name = name
        self.widget = widget
        self.label = QLabel(self.name)
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")

        self.layout.setContentsMargins(40,10,10,5)
        self.layout.addWidget(self.label)
        self.layout.addStretch(10)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)


class DefaultNumberEdit(QDoubleSpinBox):
    def __init__(self, min=0, max=100, decimals=2):
        QDoubleSpinBox.__init__(self)
        self.setMaximum(max)
        self.setMinimum(min)
        self.setDecimals(decimals)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")


class DefaultSlider(QWidget):
    def __init__(self, min = 0, max = 100):
        QWidget.__init__(self)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.label = QLabel(" ")
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.layout = QHBoxLayout()

        self.slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.label.setContentsMargins(25,0,0,0)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.slider.valueChanged.connect(self.slider_changed)
        self.setLayout(self.layout)

    def slider_changed(self):
        val = self.slider.value()
        self.label.setText(str(val))

