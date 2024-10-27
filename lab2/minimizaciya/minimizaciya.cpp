#include "minimizaciya.h"

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

static void MooreMin(istream& input, ostream& output)
{
	cout << "Минимизация Мура";
	Sleep(1000);
}

static void MealyMin(istream& input, ostream& output)
{
    cout << "Минимизация Мили";
    Sleep(1000);
}

static void Minimize(istream& input, ostream& output, const string& mode)
{
    if (mode == MOORE)
    {
        MooreMin(input, output);
        return;
    }
    if (mode == MEALY)
    {
        MealyMin(input, output);
        return;
    }
    throw std::ios_base::failure(ERROR_MODE);
}

int main(int argc, char* argv[])
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	if (argc != 4)
	{
		cerr << argv[0] << ERROR_ARGC << endl;
		return 1;
	}

	string mode = argv[1];
	ifstream input(argv[2]);
	ofstream output(argv[3]);

    try
    {
        Minimize(input, output, mode);
    }
    catch (const exception& e)
    {
        cout << e.what() << endl;
        return 1;
    }

	return 0;
}
