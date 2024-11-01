#include "lab1.h"

void MachineConverter::MinimizeMealy(istream& input, ostream& output)
{
    CMealy mealy;
    mealy.Read(input);
    mealy.Minimize(output);
}

void MachineConverter::MinimizeMoore(istream& input, ostream& output)
{
    CMoore moore;
    moore.Read(input);
    moore.Minimize(output);
}

void MachineConverter::Convert(const string& mode, istream& input, ostream& output)
{
    if (mode == "moore-to-mealy")
    {
        CMoore moore;
        moore.Read(input);
        moore.ConvertToMealy(output);
    }
    else if (mode == "mealy-to-moore")
    {
        CMealy mealy;
        mealy.Read(input);
        mealy.ConvertToMoore(output);
    }
    else if (mode == "mealy-minimize")
    {
        MinimizeMealy(input, output);
    }
    else if (mode == "moore-minimize")
    {
        MinimizeMoore(input, output);
    }
    else
    {
        cerr << "Некорректный режим. Используйте mealy-to-moore, moore-to-mealy, mealy-minimize или moore-minimize." << endl;
    }
}

int main(int argc, char* argv[])
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    if (argc != 4)
    {
        cerr << argv[0] << " <mode> <input_file> <output_file>" << endl;
        return 1;
    }

    string mode = argv[1];
    ifstream input(argv[2]);
    ofstream output(argv[3]);

    MachineConverter::Convert(mode, input, output);

    return 0;
}
