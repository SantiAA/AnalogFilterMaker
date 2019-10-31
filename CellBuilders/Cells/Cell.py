"""
Cell base class
"""

# python native modules

# third-party modules

# AFM project modules


class Cell(object):

    def __init__(self):
        self.name = ""
        self.filter_type = ""
        self.images = []
        self.components = {}

    def get_components_value(self):
        pass

    def load_information(self):
        """
        Check what input do I need to work, Q-Xi-Gain-(Zero-Poles)???
        :return: bool
        """
        pass

    def get_sensibilities(self, component):
        pass

