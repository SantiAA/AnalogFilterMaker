class Zero:
    def __init__(self, im, n):
        self.im = im
        self.n = n
        self.used = False

    def get_msg(self):
        using = ""
        if self.used:
            using = " (used)"
        return f"fo: {abs(self.im):.1f}, n: {self.n}" + using

    def __eq__(self, other):
        return self.im == other.im