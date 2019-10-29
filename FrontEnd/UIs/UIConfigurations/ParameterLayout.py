from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QWidget, QSizePolicy, QDoubleSpinBox, QVBoxLayout, \
    QCheckBox, QComboBox


class FilterParameterLayout(QWidget):
    def __init__(self, name, widget):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.name = name
        self.widget = widget
        self.label = QLabel(self.name)
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(40, 10, 10, 5)
        self.layout.addWidget(self.label)
        self.layout.addStretch(10)
        self.layout.addWidget(self.widget)
        self.setLayout(self.layout)

    def get_value(self):
        return self.widget.get_value()

    def set_value(self):
        return self.widget.set_value()


class ApproximationParameterLayout(QWidget):
    def __init__(self, name, widget, toggleable):
        QWidget.__init__(self)
        self.toggleable = toggleable
        self.auto = False
        self.layout = QVBoxLayout()
        self.name = name
        self.widget = widget
        self.label = QLabel(self.name)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignCenter)
        self.check_box = QCheckBox()
        self.check_box.setStyleSheet("font-size: 12px; color:rgb(255, 255, 255);")
        self.check_box.setText("Manual")
        self.check_box.toggled.connect(self.check_box_toggled)
        self.rows = [InternalApproximationLayoutRow(self.label, self.check_box), self.widget]
        if not toggleable:
            self.check_box.hide()
        self.layout.addStretch()
        for row in self.rows:
            self.layout.addWidget(row)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_value(self, value):
        self.widget.set_value(value)

    def get_value(self):
        return self.widget.get_value()

    def get_min(self):
        return self.widget.get_min()

    def get_max(self):
        return self.widget.get_max()

    def get_default_value(self):
        return self.widget.get_default_value()

    def check_box_toggled(self):
        if self.check_box.isChecked():
            self.check_box.setText("Auto")
            self.rows[1].hide()
            self.auto = True

        else:
            self.check_box.setText("Manual")
            self.rows[1].show()
            self.auto = False


class InternalApproximationLayoutRow(QWidget):
    def __init__(self, widget1, widget2):
        QWidget.__init__(self)
        self.widget1 = widget1
        self.widget2 = widget2
        self.layout = QHBoxLayout()

        self.layout.addWidget(widget1)
        self.layout.addStretch(1)
        self.layout.addWidget(widget2)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class DefaultNumberEdit(QDoubleSpinBox):
    def __init__(self, min=0, max=100, decimals=2, default_value=0):
        QDoubleSpinBox.__init__(self)
        self.min = min
        self.max = max
        self.decimals = decimals
        self.default_value = default_value
        self.setMaximum(max)
        self.setMinimum(min)
        self.setValue(default_value)
        self.setDecimals(decimals)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")

    def get_value(self):
        return self.value()

    def set_value(self, value):
        self.setValue(int(value))

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_default_value(self):
        return self.default_value


class DefaultSlider(QWidget):
    def __init__(self, min=0, max=100, default_value=50):
        self.min = min
        self.max = max
        self.default_value = default_value
        QWidget.__init__(self)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setValue(default_value)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.label = QLabel(" ")
        self.slider_changed()
        self.label.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.layout = QHBoxLayout()

        self.slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.label.setContentsMargins(25, 0, 0, 0)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.slider.valueChanged.connect(self.slider_changed)
        self.setLayout(self.layout)

    def slider_changed(self):
        val = self.slider.value()
        self.label.setText(str(val))

    def get_value(self):
        return self.slider.value()

    def set_value(self, value):
        self.slider.setValue(int(value))
        self.label.setText(str(value))

    def get_min(self):
        return self.min

    def get_max(self):
        return self.max

    def get_default_value(self):
        return self.default_value


class DefaultComboBox(QWidget):
    def __init__(self, approxs):
        QWidget.__init__(self)
        self.combo = QComboBox()
        self.combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.combo.setStyleSheet("font-size: 14px; color:rgb(255, 255, 255);")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.combo)

        self.setLayout(self.layout)
        self.approxs = approxs
        for approx in self.approxs:
            self.combo.addItem(approx)

    def get_value(self):
        return self.combo.currentText()

    def set_value(self, value):
        index = self.combo.findText(value)
        if index != -1:
            self.combo.setCurrentIndex(index)

    def get_min(self):
        return None

    def get_max(self):
        return None

    def get_default_value(self):
        return None
