class ApproximationTesting:
    def __init__(self, name, dict_of_features, extra_combos=0):
        self.name = name
        self.dict = dict_of_features
        self.extra_combos = extra_combos  # For transitional approximations (extra_combos would be equal to 2)
