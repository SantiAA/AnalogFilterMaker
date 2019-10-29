import webbrowser

import matplotlib as mpl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from FrontEnd.UIControl.FinalGraph import FinalGraph
from FrontEnd.UIs.FilterConfigurations.Config import Config
from FrontEnd.UIs.FilterConfigurations.Template import Template
from FrontEnd.UIs.Testing.ApproximationTesting import ApproximationTesting
from FrontEnd.UIs.Testing.BackEndTesting import BackEndTesting


class FirstStage(QMainWindow):

    def __init__(self, ui_manager):
        self.graph_widget = None
        self.ui_manager = ui_manager
        self.a = 0
        self.filters = {}
        self.backend = BackEndTesting()
        self.filters_received, self.approximations_received = self.backend.get_util()

        self.showingGraphs = []
        self.current_template = Template()

    def start(self):
        """
        Actions to perform when the window is shown.
        """
        QMainWindow.__init__(self)
        loadUi('FrontEnd/UIs/firststage.ui', self)
        self.setWindowTitle("Filter Design Tool")
        self.graph_widget = self.graphWidget
        self.comboFilter.clear()
        for filter in self.filters_received:
            self.comboFilter.addItem(filter)
            self.filters[filter] = Config(filter, self.filters_received[filter], self.approximations_received[filter])

        self.update_filter_type()
        self.show()
        self.addApproxButton.clicked.connect(self.add_approx)
        self.removeApproxButton.clicked.connect(self.remove_approx)
        self.filterTypeLabel.clicked.connect(self.filter_type_label_clicked)
        self.approximationLabel.clicked.connect(self.approximation_label_clicked)
        self.parametersLabels.clicked.connect(self.parameters_label_clicked)
        self.comboFilter.currentIndexChanged.connect(self.update_filter_type)
        self.approxCombo.currentIndexChanged.connect(self.update_approximation)
        self.plotTemplateButton.clicked.connect(self.plot_template_button_clicked)
        self.toggleApprox.toggled.connect(self.toggle_approximation)
        self.editApproximationButton.clicked.connect(self.edit_approx)
        self.activeApproxsCombo.currentIndexChanged.connect(self.approx_combo_changed)
        self.save_as_project_button.clicked.connect(self.save_as_current_state_clicked)
        self.save_project_button.clicked.connect(self.save_current_state_clicked)
        self.toggleApprox.hide()
        self.fill_combo_graph()
        self.comboGraph.currentIndexChanged.connect(self.combo_graph_changed)
        self.load_project_button.clicked.connect(self.load_project_clicked)
        self.templateCheckBox.toggled.connect(self.template_toggled)
        self.templateCheckBox.hide()

    def load_project_clicked(self):
        self.ui_manager.load_current_state()

    def load_current_state(self, configuration_dict):
        self.showingGraphs = []
        self.showingGraphs = configuration_dict["showing_graphs"]
        self.fill_combo_graph()
        self.redraw_graphs()

    def get_current_state_config(self):
        self.window_configuration = {}
        self.window_configuration["active_filter"] = self.comboFilter.currentText()
        requirements = []
        for requirement in self.filters[self.comboFilter.currentText()].parameter_list:
            requirements.append(requirement.get_value())
        self.window_configuration["requirement_values"] = requirements
        self.window_configuration["showing_graphs"] = self.showingGraphs
        return self.window_configuration

    def combo_graph_changed(self):
        self.redraw_graphs()

    def fill_combo_graph(self):
        self.comboGraph.clear()

        for graph in self.showingGraphs:
            for key in graph.graphs.keys():
                if self.comboGraph.findText(key) == -1:
                    self.comboGraph.addItem(key)

    def approx_combo_changed(self):
        for graph in self.showingGraphs:
            if graph.approximation_properties_string == self.activeApproxsCombo.currentText():
                if graph.enabled:
                    self.toggleApprox.setChecked(True)
                else:
                    self.toggleApprox.setChecked(False)

    def toggle_approximation(self):
        for graph in self.showingGraphs:
            if graph.get_total_string() == self.activeApproxsCombo.currentText():
                graph.toggle_graph(self.toggleApprox.isChecked())
                self.redraw_graphs()
        self.get_current_state_config()

    def edit_approx(self):
        approx_name = ""
        for graph in self.showingGraphs:
            if graph.get_total_string() == self.activeApproxsCombo.currentText():
                for property_tuple in graph.properties:
                    if property_tuple[0] == "Approximation":
                        approx_name = property_tuple[1]
                        index = self.approxCombo.findText(approx_name)
                        self.approxCombo.setCurrentIndex(index)
                    else:
                        self.filter = self.filters[self.comboFilter.currentText()]
                        for approximation in self.filter.approximation_list:
                            if approximation.name == approx_name:
                                for parameter in approximation.parameter_list:
                                    if parameter.name == property_tuple[0]:
                                        if property_tuple[1] == "Auto":

                                            parameter.rows[1].hide()
                                            parameter.check_box.show()
                                            parameter.check_box.setChecked(True)

                                            if not parameter.toggleable:
                                                parameter.check_box.hide()
                                        else:
                                            parameter.set_value(property_tuple[1])
                                            parameter.check_box.show()
                                            parameter.check_box.setChecked(False)
                                            if not parameter.toggleable:
                                                parameter.check_box.hide()

    def template_toggled(self):
        self.current_template.enabled = not self.current_template.enabled
        self.redraw_template()

    def redraw_template(self):
        if self.current_template.enabled:
            mpl_squares = self.current_template.get_matplotlib_squares()
            if mpl_squares is not None:
                for square in mpl_squares:
                    square.set_linewidth(3)
                    self.plot_rectangle(square)
        else:
            self.redraw_graphs()

    def plot_template_button_clicked(self):
        if len(self.current_template.squares) == 0:
            self.templateCheckBox.show()
        self.filter = self.filters[self.comboFilter.currentText()]
        dict = self.filter.make_feature_dictionary()
        validated, error_string = self.backend.validate_filter([self.filter.name, dict])
        if validated:
            squares = self.backend.get_template([self.filter.name, dict])
            self.current_template.squares = squares
            if self.templateCheckBox.isChecked():
                self.current_template.enabled = True
            else:
                self.current_template.enabled = False
            self.redraw_template()


        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(error_string)
            msg.setWindowTitle("Error")
            msg.exec_()

        '''
        me = pickle.load(open("Save File", "rb"))  # Loads the file
        uu = 0  # Prints the stats out to verify the load has successfully happened'''

    def save_as_current_state_clicked(self):
        self.ui_manager.save_as_current_state()

    def save_current_state_clicked(self):
        self.ui_manager.save_current_state()

    def approximation_label_clicked(self):
        webbrowser.open('http://dsp-book.narod.ru/HFTSP/8579ch12.pdf')

    def parameters_label_clicked(self):
        webbrowser.open('https://electronicspani.com/electric-filter-types-of-filter/')

    def filter_type_label_clicked(self):
        webbrowser.open('https://www.allaboutcircuits.com/technical-articles/an-introduction-to-filters/')

    def update_filter_type(self):
        """
        Changes the filter template image and requirements whenever the current selected filter type is changed.
        """
        self.current_template = Template()
        self.comboGraph.clear()
        self.showingGraphs = []
        self.__update_active_approx_combo__()
        self.templateCheckBox.setChecked(True)
        self.templateCheckBox.hide()
        self.redraw_graphs()
        # update plot
        for filters in self.filters.values():  # Clearing requirement widgets
            for parameters in filters.parameter_list:
                parameters.setParent(None)
            for approx in filters.approximation_list:
                for parameter in approx.parameter_list:
                    parameter.setParent(None)

        self.filter = self.filters[self.comboFilter.currentText()]
        self.approxCombo.clear()

        for approximation in self.filter.approximation_list:
            self.approxCombo.addItem(approximation.name)

        self.update_approximation()
        self.graphPic.setPixmap(QPixmap(self.filter.template_image))  # filter template image

        self.clear_layout(self.configurationLayout)
        for parameter in self.filter.parameter_list:  # Refilling requierement widgets
            self.configurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(50)  # space
        if len(self.showingGraphs) == 0:
            self.toggleApprox.hide()

    def update_approximation(self):
        for filters in self.filters.values():  # Clearing requirement widgets
            for approx in filters.approximation_list:
                for parameter in approx.parameter_list:
                    parameter.setParent(None)
        self.filter = self.filters[self.comboFilter.currentText()]
        self.clear_layout(self.approxConfigurationLayout)

        for approximation in self.filter.approximation_list:
            if approximation.name == self.approxCombo.currentText():
                for parameter in approximation.parameter_list:
                    self.approxConfigurationLayout.addWidget(parameter)
        self.configurationLayout.addStretch(2)  # space
        self.show()

    def remove_approx(self):
        """
        Removes graphs and text when an active approximation is removed by the user.
        """
        if self.activeApproxsCombo.currentText() is not None or self.activeApproxsCombo.currentText() != "":
            for approx in self.showingGraphs:
                if approx.get_total_string() == self.activeApproxsCombo.currentText():
                    self.showingGraphs.remove(approx)
            self.fill_combo_graph()
            self.__update_active_approx_combo__()
            self.redraw_graphs()
        if len(self.showingGraphs) == 0:
            self.toggleApprox.hide()

    def add_approx(self):
        """
        Appends user selected approximation to active approximations and applies it to the filter.
        """
        self.toggleApprox.show()
        properties = []
        self.graphics_returned = []
        self.filter = self.filters[self.comboFilter.currentText()]
        dict = self.filter.make_feature_dictionary()
        validated, error_string = self.backend.validate_filter([self.filter.name, dict])
        if validated:
            for approximation in self.filter.approximation_list:
                if approximation.name == self.approxCombo.currentText():
                    properties.append(["Approximation", approximation.name])
                    for prop in approximation.parameter_list:

                        if not prop.toggleable or not prop.check_box.isChecked():
                            properties.append([prop.name, str(prop.get_value())])
                        else:
                            properties.append([prop.name, "Auto"])
                    self.graphics_returned = self.backend.get_graphs([self.filter.name, dict],
                                                                     ApproximationTesting(approximation.name,
                                                                                          approximation.make_approx_dict(),
                                                                                          approximation.extra_combos))
                    self.existing = True
                    new_graph = FinalGraph(self.graphics_returned, properties, True)

                    found = False
                    for graph in self.showingGraphs:
                        if graph.approximation_properties_string == new_graph.approximation_properties_string:
                            found = True
                    if not found:
                        self.showingGraphs.append(new_graph)
            self.fill_combo_graph()
            self.__update_active_approx_combo__()
            self.redraw_graphs()



        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(error_string)
            msg.setWindowTitle("Error")
            msg.exec_()

    def __update_active_approx_combo__(self):
        self.activeApproxsCombo.clear()
        i = 0
        for approx in self.showingGraphs:
            approx.id = i
            i += 1
            self.activeApproxsCombo.addItem(approx.get_total_string())
        self.activeApproxsCombo.setCurrentIndex(self.activeApproxsCombo.count() - 1)

    def clear_layout(self, layout):
        """
        Clears widgets from a layout.
        :param layout: layout to clear
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

    def plot_rectangle(self, square):

        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
        self.graph_widget.canvas.axes.set_xscale('log')
        self.graph_widget.canvas.axes.grid(True, which="both")
        self.graph_widget.canvas.axes.add_patch(square)
        self.graph_widget.canvas.axes.set_xlim(self.current_template.find_axes_limits()[0])
        self.graph_widget.canvas.axes.set_ylim(self.current_template.find_axes_limits()[1])
        self.graph_widget.canvas.draw()  # Redraws

    def redraw_graphs(self):
        try:
            self.graph_widget.canvas.axes.clear()
            self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())

            self.graph_widget.canvas.axes.grid(True, which="both")

            self.graph_widget.canvas.draw()  # Redraws

            for graph in self.showingGraphs:
                if graph.enabled:
                    graph_values = graph.graphs[self.comboGraph.currentText()]
                    if graph_values is not None:
                        self.__plot_graph__(graph_values, "ID: " + str(graph.id) + ". ")

                        self.graph_widget.canvas.axes.grid(True, which="both")
                        self.graph_widget.canvas.axes.set_title(self.comboGraph.currentText())
                        self.graph_widget.canvas.draw()  # Redraws
            if self.current_template.enabled:
                self.redraw_template()
        except:
            a = 0

    def __plot_graph__(self, graph, legend_string):
        self.__fix_axes_titles_position__(self.graph_widget, graph[1][0], graph[1][1])
        for graph_data in graph[0]:
            if graph_data.log:
                self.graph_widget.canvas.axes.set_xscale('log')
            complete_legend = legend_string
            if graph_data.extra_information != "":
                complete_legend += "-" + graph_data.extra_information
            if not graph_data.scattered:
                if not graph_data.x_marks:
                    self.graph_widget.canvas.axes.plot(graph_data.x_values, graph_data.y_values, label=complete_legend)
                else:
                    self.graph_widget.canvas.axes.plot(graph_data.x_values, graph_data.y_values, marker='x',
                                                       label=complete_legend)

            else:
                if not graph_data.x_marks:
                    self.graph_widget.canvas.axes.scatter(graph_data.x_values, graph_data.y_values,
                                                          label=complete_legend)
                else:
                    self.graph_widget.canvas.axes.scatter(graph_data.x_values, graph_data.y_values, marker='x',
                                                          label=complete_legend)
        self.graph_widget.canvas.axes.legend(loc='best')

    # Funciones que configuran y muestran los titulos de los ejes.
    def __fix_axes_titles_position__(self, widget, label_x, label_y):
        self.__fix_y_title_position__(widget, label_y)
        self.__fix_x_title_position__(widget, label_x)

    def __fix_x_title_position__(self, widget, label):
        ticklabelpad = mpl.rcParams['xtick.major.pad']
        widget.canvas.axes.annotate(label, xy=(1, 0), xytext=(20, -ticklabelpad),
                                    ha='left', va='top',
                                    xycoords='axes fraction', textcoords='offset points')

    def __fix_y_title_position__(self, widget, label):
        ticklabelpad = mpl.rcParams['ytick.major.pad']
        widget.canvas.axes.annotate(label, xy=(0, 1), xytext=(-30, -ticklabelpad + 10),
                                    ha='left', va='bottom',
                                    xycoords='axes fraction', textcoords='offset points', rotation=0)
