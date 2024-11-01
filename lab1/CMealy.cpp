#include "CMealy.h"

template <typename T>
typename vector<T>::iterator FindMoveInVector(vector<T>& vec, const T& value)
{
    return find(vec.begin(), vec.end(), value);
}

vector<string> CMealy::ReadSignals(istream& input)
{
    string tempStr;
    vector<string> listOfY;
    string item;

    getline(input, tempStr);
    size_t pos = tempStr.find(';');
    if (pos != string::npos)
    {
        tempStr = tempStr.substr(pos + 1);
    }

    stringstream ss(tempStr);

    while (getline(ss, item, ';'))
    {
        listOfY.push_back(item);
    }
    return listOfY;
}

vector<vector<Move>> CMealy::ReadMealyTable(istream& input)
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

void CMealy::AddInitialState(const string& initialState, const string& defaultOutput)
{
    Move initialMove = { initialState, defaultOutput };
    listOfQ.insert(listOfQ.begin(), initialMove);
}

void CMealy::WriteMooreTable(ostream& output)
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
            Move tempMove = table[i][distance(listOfS.begin(), find(listOfS.begin(), listOfS.end(), listOfQ[j].s))];
            int index = GetMoveIndex(tempMove);
            output << "q" << index << ";";
        }
        output << endl;
    }
}

int CMealy::GetMoveIndex(const Move& move) const
{
    for (int i = 0; i < listOfQ.size(); ++i)
    {
        if (listOfQ[i].s == move.s && listOfQ[i].y == move.y)
        {
            return i;
        }
    }
    return -1;
}

void CMealy::Read(istream& input)
{
    listOfS = ReadSignals(input);
    table = ReadMealyTable(input);
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
        AddInitialState(listOfS[0], "-");
    }
    sort(
        listOfQ.begin(),
        listOfQ.end(),
        [](const Move& a, const Move& b) {
            return a.s < b.s;
        }
    );
}

void CMealy::Write(ostream& output)
{
    WriteMooreTable(output);
}

void CMealy::ConvertToMoore(ostream& output)
{
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
        AddInitialState(listOfS[0], "-");
    }
    sort(
        listOfQ.begin(),
        listOfQ.end(),
        [](const Move& a, const Move& b)
        {
            return a.s < b.s;
        }
    );

    WriteMooreTable(output);
}

void CMealy::Minimize(ostream& output)
{
    CMinimizer::MealyMinimizer(*this);
    Write(output);
}
