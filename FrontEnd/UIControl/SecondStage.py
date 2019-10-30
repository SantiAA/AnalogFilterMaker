from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QRadioButton, QWidget, QVBoxLayout, QMessageBox
from PyQt5.uic import loadUi
from sympy.physics.quantum.tests.test_circuitplot import mpl

from BackEnd.BackEnd import BackEnd
from FrontEnd.UIs.Testing.BackEndTesting import BackEndTesting
from FrontEnd.UIs.UIConfigurations.StagesUILayout import StagesUILayout, HorizontalParameter
from StagesManager.StagesManager import StagesManager


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
        self.stages_ui_layout = StagesUILayout(self.selected_amount_changed)
        self.stagesLayout.addWidget(self.stages_ui_layout)
        self.create_button.clicked.connect(self.create_clicked)
        self.deleteButton.clicked.connect(self.delete_stages)
        self.autostage.clicked.connect(self.auto_stage)
        self.reloadv.clicked.connect(self.update_rd)
        self.nextButton.clicked.connect(self.right_shift)
        self.backButton.clicked.connect(self.left_shift)
        self.goGain.clicked.connect(self.set_gain)
        self.stages_manager = StagesManager()
        self.__plot_p_z_graph__()
        self.poles_and_zeros_dict = self.stages_manager.get_z_p_dict()
        self.__fill_poles_and_zeros_combos__()
        self.all_loaded = False
        self.param_vbox = QVBoxLayout()
        self.param_group_box.setLayout(self.param_vbox)
        self.selected_amount_changed()
        self.showing_options = []
        self.show()

    def update_rd(self):
        rd_answer = self.stages_manager.get_dr(self.vminSpin.value(), self.vmaxSpin.value())
        if rd_answer[0] == False:
            self.__show_error__(rd_answer[1])
        else:
            self.rd.setText(str(round(rd_answer[1],2)))

    def __show_error__(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(error)
        msg.setWindowTitle("Error")
        msg.exec_()


    def selected_amount_changed(self):
        if self.stages_ui_layout.get_number_of_checked() == 1:
            self.gainSpin.show()
            self.goGain.setText("GO")
            self.goGain.setSyleSheet("font: 63 9pt; color:rgb(255, 255, 255);")
        else:
            self.gainSpin.hide()
            self.goGain.setText("N/A")
            self.goGain.setSyleSheet("font: 63 10pt;color:rgb(255, 255, 255);border: 0px solid blue;")

    def set_gain(self):
        self.stages_manager.set_gain(self.stages_ui_layout.get_selected_ids_array()[0], self.gainSpin.value())
        params = self.stages_manager.get_const_data(self.stages_ui_layout.get_selected_ids_array())
        self.clear_layout(self.param_vbox)
        for key, value in params:
            self.param_vbox.addWidget(HorizontalParameter(key, value[0], value[1]))

    def right_shift(self):
        self.stages_manager.shift_stages(self.stages_ui_layout.get_selected_ids_array(), False)
        self.stages_ui_layout.delete_all_stages()
        self.__reload_stages__()

    def left_shift(self):
        self.stages_manager.shift_stages(self.stages_ui_layout.get_selected_ids_array(), True)
        self.stages_ui_layout.delete_all_stages()
        self.__reload_stages__()

    def __plot_poles_and_zeros__(self):
        z_p_plot = self.stages_manager.get_z_p_plot()
        self.__plot_p_z_graph__(z_p_plot)

    def __plot_p_z_graph__(self, graphs):
        self.__fix_axes_titles_position__(self.graph_widget, graphs[1][0], graphs[1][1])
        for graph_data in graphs[0]:
            if graph_data.log:
                self.z_p_diagram.canvas.axes.set_xscale('log')
            n_array_text = []
            for n in graph_data.n_array:
                string_gen = ""
                if n > 1:
                    string_gen += str(n)
                n_array_text.append(string_gen)
            if not graph_data.x_marks:
                self.z_p_diagram.canvas.axes.scatter(graph_data.x_values, graph_data.y_values)
                for i in range(0, len(n_array_text)):
                    self.z_p_diagram.canvas.axes.annotate(n_array_text[i],
                                                          (graph_data.x_values[i], graph_data.y_values[i]))
            else:
                self.z_p_diagram.canvas.axes.scatter(graph_data.x_values, graph_data.y_values, marker='x')
                for i in range(0, len(n_array_text)):
                    self.z_p_diagram.canvas.axes.annotate(n_array_text[i],
                                                          (graph_data.x_values[i], graph_data.y_values[i]))

    # Funciones que configuran y muestran los titulos de los ejes.
    def __fix_axes_titles_position__(self, widget, label_x, label_y):
        self.__fix_y_title_position__(widget, label_y)
        self.__fix_x_title_position__(widget, label_x)

    def __fix_x_title_position__(self, widget, label):
        ticklabelpad = mpl.rcParams['xtick.major.pad']
        widget.canvas.axes.annotate(label, xy=(1, 0), xytext=(-15, -ticklabelpad),
                                    ha='left', va='top',
                                    xycoords='axes fraction', color="w", textcoords='offset points')

    def __fix_y_title_position__(self, widget, label):
        ticklabelpad = mpl.rcParams['ytick.major.pad']
        widget.canvas.axes.annotate(label, xy=(0, 1), xytext=(15, -ticklabelpad + 5),
                                    ha='left', va='bottom',
                                    xycoords='axes fraction', color="w", textcoords='offset points', rotation=0)

    def delete_stages(self):
        self.stages_manager.delete_stages(self.stages_ui_layout.get_selected_ids_array())
        self.stages_ui_layout.delete_all_stages()
        self.__reload_stages__()



    def auto_stage(self):
        self.stages_manager.auto_max_rd(self.vminSpin.value(), self.vmaxSpin.value())
        self.stages_ui_layout.delete_all_stages()
        self.__reload_stages__()

    def create_clicked(self):
        self.stages_manager.add_stage(self.combo1.currentText(), self.combo2.currentText())
        self.stages_ui_layout.delete_all_stages()
        self.__reload_stages__()

    def __reload_stages__(self):
        current_stages = self.stages_manager.get_stages()
        i = 0
        for stage in current_stages:
            self.stages_ui_layout.add_stage(stage,i )
            i+=1

    def __fill_poles_and_zeros_combos__(self):
        # self.comboFilter.model().item(1).setEnabled(False)
        self.combo1.clear()
        self.combo2.clear()
        self.combo2.addItem("")
        self.combo2.model().item(0).setEnabled(False)
        self.title_combo_1.setText(self.poles_and_zeros_dict.keys()[0])
        self.title_combo_2.setText(self.poles_and_zeros_dict.keys()[1])

        for i in range(0, 2):
            for key in self.poles_and_zeros_dict.keys()[i]:
                if i == 0:
                    self.combo1.addItem(key)
                    self.combo1.model().item(self.combo1.findText(key)).setEnabled(False)
                    for sing in self.poles_and_zeros_dict[key]:
                        self.combo1.addItem(sing.get_msg())
                if i == 1:
                    self.combo2.addItem(key)
                    self.combo2.model().item(self.combo2.findText(key)).setEnabled(False)
                    for sing in self.poles_and_zeros_dict[key]:
                        self.combo1.addItem(sing.get_msg())

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
        self.showing_options.clear()
        hbox = QHBoxLayout()
        self.showing_group.setLayout(hbox)

        radiobutton = QRadioButton("Selected")
        hbox.addWidget(radiobutton)
        radiobutton.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")
        self.showing_options.append(radiobutton)

        radiobutton2 = QRadioButton("Accumulative")
        hbox.addWidget(radiobutton2)
        radiobutton2.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")
        self.showing_options.append(radiobutton2)

        radiobutton3 = QRadioButton("Overlapping Stages")
        hbox.addWidget(radiobutton3)
        radiobutton3.setStyleSheet("font: 63 7pt ; color:rgb(255, 255, 255);")
        self.showing_options.append(radiobutton3)

    def clear_layout(self, layout):
        """
        Clears widgets from a layout.
        :param layout: layout to clear
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

