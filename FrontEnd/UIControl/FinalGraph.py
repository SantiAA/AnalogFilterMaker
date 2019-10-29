class FinalGraph:
    #properties = [name, value]
    #graphs = dict coming from backend get_graphs
    def __init__(self, graphs, properties, enabled=True):
        self.enabled = enabled
        self.properties = properties
        self.approximation_properties_string = ""
        self.change_approximation_string()
        self.graphs = []
        self.graphs = graphs

    def toggle_graph(self, enabled):
        self.enabled = enabled

    def change_approximation_string(self):
        self.approximation_properties_string = ""
        for prop_tuple in self.properties:
            if prop_tuple[0] == "Approximation":
                self.approximation_properties_string += prop_tuple[1] + "."
            else:
                self.approximation_properties_string += (" " + prop_tuple[0] + ": " + prop_tuple[1] + ".")


