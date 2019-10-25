"""
Approximation base class
"""

# python native modules

# third-party modules

# AFM project modules
from Filters.Filters import Filter


class Approximation(object):

    def __init__(self, name):
        """ Useful to add in the GUI """
        self.name = name  # The name of the approximation
        self.application = []  # Approximation's filter type application

        """ Useful for internal working """
        self.poles = []
        self.zeros = []

    def validate_input(self):
        """
        Check if the information loaded was ok
        """
        pass

    def get_filter(self):
        """
        return: signal.lti object
        """
        pass

    def load_information(self, filter_in_use: Filter):
        pass

    def calculate(self, filter_in_use: Filter, n_max=20):
        pass
    """ Search more useful functions to add """
