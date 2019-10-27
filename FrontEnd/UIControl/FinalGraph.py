class FinalGraph:
    def __init__(self, graphs, properties, enabled=True):
        self.enabled = enabled
        self.properties = properties
        self.approximation_properties_string = ""
        self.change_approximation_string()
        self.graphs = graphs

    def toggle_graph(self):
        self.enabled = not self.enabled

    def change_approximation_string(self):
        self.approximation_properties_string = ""
        for prop_tuple in self.properties:
            if prop_tuple[0] == "Approximation":
                self.approximation_properties_string += prop_tuple[1] + "."
            else:
                self.approximation_properties_string += (" " + prop_tuple[0] + ": " + prop_tuple[1] + ".")
