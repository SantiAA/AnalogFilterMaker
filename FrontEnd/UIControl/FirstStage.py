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
