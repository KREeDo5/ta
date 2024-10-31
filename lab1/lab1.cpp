#include "lab1.h"
#include "CMealy.h"
#include "CMoore.h"

void MachineConverter::Convert(const string& mode, istream& input, ostream& output) {
    if (mode == "moore-to-mealy") {
        CMoore moore;
        moore.Read(input);
        moore.ConvertToMealy(output);
    }
    else if (mode == "mealy-to-moore") {
        CMealy mealy;
        mealy.Read(input);
        mealy.ConvertToMoore(output);
    }
    else {
        cerr << "Некорректный режим. Используйте mealy-to-moore или moore-to-mealy." << endl;
    }
}

int main(int argc, char* argv[]) {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    if (argc != 4) {
        cerr << argv[0] << " <mode> <input_file> <output_file>" << endl;
        return 1;
    }

    string mode = argv[1];
    ifstream input(argv[2]);
    ofstream output(argv[3]);

    MachineConverter::Convert(mode, input, output);

    return 0;
}
