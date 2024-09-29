#include "lab1.h"

using namespace std;

// уточнить про использование STL

vector<vector<string>> readCSV(const string& filename)
{
    ifstream file(filename);
    vector<vector<string>> table;
    string line;

    while (getline(file, line))
    {
        stringstream stream(line);
        string cell;
        vector<string> row;
        //сортируем строку
        while (getline(stream, cell, ';'))
        {
            row.push_back(cell);
        }
        table.push_back(row);
    }

    return table;

    /*
           X
    ------->
    |      
    |
    |
 Y  V 

    y = row = [x0,.., xn]
    table = [y0,..,yk]

    [        [   
      y0,      [x0,..,xn]0,
      ..., =   ..,
      yk       [x0,..,xn]k
    ]        ]

    */
}

void writeCSV(const string& filename, const vector<vector<string>>& table)
{
    ofstream file(filename);
    // проход по `y`
    for (const auto& row : table)
    {
        // проход по `x`
        for (size_t i = 0; i < row.size(); ++i)
        {
            file << row[i];
            //проверяем последняя это ячейка или нет
            if (i < row.size() - 1)
                file << ";";
        }
        file << endl;
    }
}

vector<vector<string>> mealyToMoore(const vector<vector<string>>& mealyTable)
{
    vector<vector<string>> mooreTable;

    return mooreTable;
}

vector<vector<string>> mooreToMealy(const vector<vector<string>>& mooreTable)
{
    vector<vector<string>> mealyTable;

    return mealyTable;
}

int main(int argc, char* argv[]) 
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    if (argc != 4) 
    {
        cerr << "Введите команду в формате: " << argv[0] << " [mealy-to-moore/moore-to-mealy] inputFileName.csv outputFileName.csv" << endl;
        return 1;
    }

    string mode = argv[1];
    string inputFileName = argv[2];
    string outputFileName = argv[3];

    vector<vector<string>> inputTable = readCSV(inputFileName);
    vector<vector<string>> outputTable;

    if (mode == "mealy-to-moore")
    {
        outputTable = mealyToMoore(inputTable);
    } else if (mode == "moore-to-mealy")
    {
        outputTable = mooreToMealy(inputTable);
    } else
    {
        cerr << "Некорректный режим. Используйте mealy-to-moore или moore-to-mealy." << endl;
        return 1;
    }

    writeCSV(outputFileName, outputTable);

    return 0;
}
