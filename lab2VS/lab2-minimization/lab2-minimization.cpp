using namespace std;

#include "Windows.h"
#include "CMealy.h"
#include "CMinimizer.h"
#include <fstream>
#include <iostream>

void PrintData(std::ostream& ostream, const std::string& str)
{
    ostream << str;
}

void Convert(const string& mode, istream& input, ostream& output)
{
    if (mode == "mealy")
    {
        CMealy mealy;
        mealy.FromCSVFromStream(input);
        CMinimizer::MealyMinimizer(mealy);
        PrintData(output, mealy.ConvertToCSV());
    }
    else if (mode == "moore")
    {
        CMoore moore;
        moore.FromCSVFromStream(input);
        CMinimizer::MooreMinimizer(moore);
        PrintData(output, moore.ConvertToCSV());
    }
    else
    {
        cerr << "Некорректный режим. Для минимизации введите mealy или moore." << endl;
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

    Convert(mode, input, output);

    return 0;
}
