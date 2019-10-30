class Pole:
    def __init__(self, p: complex):
        self.p = p
        self.used = False

    def get_msg(self):
        using = ""
        if not self.used:
            using = " (used)"
        fo = abs(self.p)
        q = fo/(2*self.p.real)
        return "fo: " + str(fo) + " - n: " + str(q) + using
