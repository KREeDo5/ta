import csv
class Dfa:
    def __init__(self, SList, Alph, TransList, S0, FList):
        self.SList = SList
        self.Alph = Alph
        self.TransList = TransList
        self.S0 = S0
        self.FList = FList

    def to_csv(self, filename='output.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            final_states_row = [''] + ['F' if i in self.FList else '' for i in range(len(self.SList))]
            writer.writerow(final_states_row)
            header = [''] + [f'S{i}' for i in range(len(self.SList))]
            writer.writerow(header)
            for a in self.Alph:
                row = [a]
                for i in range(len(self.SList)):
                    if a in self.TransList[i]:
                        row.append(f'S{self.TransList[i][a]}')
                    else:
                        row.append('')
                writer.writerow(row)
