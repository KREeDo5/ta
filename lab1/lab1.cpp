#include "lab1.h"

struct Move {
    string s;
    string y;
};

static vector<Move>::iterator FindMoveInVector(vector<Move>& vector, const Move& move)
{
    return find_if(
        vector.begin(),
        vector.end(), 
        [&](const Move& m)
        {
            return (m.s == move.s) && (m.y == move.y);
        }
    );
}

static void AddInitialState(vector<Move>& listOfQ, const string& initialState, const string& defaultOutput)
{
    Move initialMove = { initialState, defaultOutput };
    if (FindMoveInVector(listOfQ, initialMove) == listOfQ.end())
    {
        listOfQ.insert(listOfQ.begin(), initialMove);
    }
}


static int GetMoveIndex(const vector<Move>& list, const Move& move)
{
    for (int i = 0; i < list.size(); ++i)
    {
        if (list[i].s == move.s && list[i].y == move.y)
        {
            return i;
        }
    }
    return -1;
}

// Чтение первой строки с выходными сигналами
static vector<string> ReadSignals(istream& input)
{
    string tempStr;
    vector<string> listOfY;
    string item;

    getline(input, tempStr);
    size_t pos = tempStr.find(';');
    if (pos != string::npos)
    {
        tempStr = tempStr.substr(pos + 1);  // Убираем всё до первого ';'
    }

    stringstream ss(tempStr);

    while (getline(ss, item, ';'))
    {
        listOfY.push_back(item);
    }
    return listOfY;
}

// Чтение оставшейся части файла (состояния автомата)
static vector<vector<Move>> ReadMealyTable(istream& input, vector<string>& listOfX, vector<Move>& listOfQ)
{
    vector<vector<Move>> table;
    string tempStr;

    while (getline(input, tempStr))
    {
        vector<Move> row;
        string inputSignal;
        string tempMove;
        Move move;

        stringstream rowStream(tempStr);
        
        getline(rowStream, inputSignal, ';');
        listOfX.push_back(inputSignal);

        while (getline(rowStream, tempMove, ';'))
        {
            size_t pos = tempMove.find('/');
            move.s = tempMove.substr(0, pos);
            move.y = tempMove.substr(pos + 1);
            row.push_back(move);

            if (FindMoveInVector(listOfQ, move) == listOfQ.end())
            {
                listOfQ.push_back(move);
            }
        }
        table.push_back(row);
    }

    return table;
}

// Вывод таблицы автомата Мура
static void WriteMooreTable(ostream& output, const vector<Move>& listOfQ, const vector<string>& listOfX, const vector<vector<Move>>& table, const vector<string>& listOfS)
{
    output << ";";
    for (const auto& move : listOfQ)
    {
        output << move.y << ";";
    }
    output << endl;

    output << ";";
    for (size_t i = 0; i < listOfQ.size(); ++i)
    {
        output << "q" << i << ";";
    }
    output << endl;

    for (size_t i = 0; i < listOfX.size(); ++i)
    {
        output << listOfX[i] << ";";
        for (size_t j = 0; j < listOfQ.size(); ++j)
        {
            Move tempMove = table[i][
                distance(
                    listOfS.begin(), 
                    find(
                        listOfS.begin(), 
                        listOfS.end(), 
                        listOfQ[j].s
                    )
                )
            ];
            int index = GetMoveIndex(listOfQ, tempMove);
            output << "q" << index << ";";
        }
        output << endl;
    }
}

// Преобразование автомата Мили в Мура
static void MealyToMoore(istream& input, ostream& output)
{
    vector<string> listOfS = ReadSignals(input);
    vector<Move> listOfQ;
    vector<string> listOfX;
    vector<vector<Move>> table = ReadMealyTable(input, listOfX, listOfQ);
    bool foundInListOfQ = false;
    for (const auto& move : listOfQ)
    {
        if (move.s == listOfS[0])
        {
            foundInListOfQ = true;
            break;
        }
    }
    if (!foundInListOfQ)
    {
        AddInitialState(listOfQ, listOfS[0], "-");
    }
    // Сортировка состояний автомата Мура
    sort(
        listOfQ.begin(), 
        listOfQ.end(), 
        [](const Move& a, const Move& b)
        {
            return a.s < b.s;
        }
    );

    WriteMooreTable(output, listOfQ, listOfX, table, listOfS);
}

// Преобразование автомата Мура в Мили
static void MooreToMealy(istream& input, ostream& output)
{
    string tempStr;

    auto listOfY = ReadSignals(input);
    getline(input, tempStr);
    output << tempStr << endl;  // вывод первой строки _|a0|a1|a2|a3|a4|

    while (getline(input, tempStr))
    {
        size_t pos = 0;
        int count = 0;
        size_t yIndex = 0;

        while ((pos = tempStr.find(';', pos)) != string::npos)
        {
            count++;
            if (count > 1 && yIndex < listOfY.size())
            {
                tempStr.insert(pos, "/" + listOfY[yIndex]);
                pos += listOfY[yIndex].length() + 1;
                yIndex++;
            }
            pos++;
        }

        if (yIndex < listOfY.size())
        {
            tempStr += "/" + listOfY[yIndex];  // Добавляем оставшийся элемент перед концом строки
        }

        output << tempStr << endl;
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

    if (mode == "moore-to-mealy")
    {
        MooreToMealy(input, output);
    }
    else if (mode == "mealy-to-moore")
    {
        MealyToMoore(input, output);
    }
    else
    {
        cerr << "Некорректный режим. Используйте mealy-to-moore или moore-to-mealy." << endl;
        return 1;
    }

    return 0;
}
