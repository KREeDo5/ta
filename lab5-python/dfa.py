class Dfa:
    def __init__(self, SList, Alph, TransList, S0, FList):
        self.SList = SList
        self.Alph = Alph
        self.TransList = TransList
        self.S0 = S0
        self.FList = FList

    def write(self):
        print("write")
