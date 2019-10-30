from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QRadioButton, QWidget
from PyQt5.uic import loadUi

from BackEnd.BackEnd import BackEnd
from FrontEnd.UIs.Testing.BackEndTesting import BackEndTesting
from FrontEnd.UIs.UIConfigurations.StagesUILayout import StagesUILayout


class SecondStage(QMainWindow):

    def __init__(self, ui_manager):
        self.graph_widget = None
        self.ui_manager = ui_manager
        self.a = 0
        self.filters = {}
        self.backend = BackEnd()

    def start(self):
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/secondstage.ui', self)
        self.setWindowTitle("Filter Design Tool")

        self.__place_button_images__()
        self.__define_showing_group__()
        self.graph_widget = self.graphWidget
        self.stages_ui_layout = StagesUILayout()
        self.stagesLayout.addWidget(self.stages_ui_layout)
        self.create_button.clicked.connect(self.create_clicked)
        self.deleteButton.clicked.connect(self.delete_stages)
        self.show()


    def delete_stages(self):
        self.stages_ui_layout.delete_selected_stages()

    def create_clicked(self):
        self.stages_ui_layout.add_stage()


    def __place_button_images__(self):
        pixmap = QPixmap("FrontEnd/UIs/figs/button_figs/next.png")
        next_icon = QIcon(pixmap)
        pixmap2 = QPixmap("FrontEnd/UIs/figs/button_figs/prev.png")
        back_icon = QIcon(pixmap2)
        pixmap3 = QPixmap("FrontEnd/UIs/figs/button_figs/delete.png")
        delete_icon = QIcon(pixmap3)
        self.nextButton.setIcon(next_icon)
        self.backButton.setIcon(back_icon)
        self.deleteButton.setIcon(delete_icon)

    def __define_showing_group__(self):
        hbox = QHBoxLayout()
        self.showing_group.setLayout(hbox)

        radiobutton = QRadioButton("Individual")
        hbox.addWidget(radiobutton)
        radiobutton.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")

        radiobutton = QRadioButton("Accumulative")
        hbox.addWidget(radiobutton)
        radiobutton.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")

        radiobutton = QRadioButton("Overlapping Stages")
        hbox.addWidget(radiobutton)
        radiobutton.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")



