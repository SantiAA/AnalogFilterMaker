"""
Approximation base class
"""

# python native modules

# third-party modules

# AFM project modules


class Approximation(object):

    def __init__(self):
        """ Useful to add in the GUI """
        self.name = ""  # The name of the approximation
        self.requirements = {}  # A dictionary with the parameters needed

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

    """ Search more useful functions to add """
