#pragma once

#include <iostream>
#include <vector>
#include <string>

using namespace std;

struct Move {
    string s;
    string y;

    bool operator==(const Move& other) const {
        return s == other.s && y == other.y;
    }
};

class CMealy {
public:
    void Read(istream& input);
    void Write(ostream& output);
    void ConvertToMoore(ostream& output);

private:
    vector<string> listOfS;
    vector<Move> listOfQ;
    vector<string> listOfX;
    vector<vector<Move>> table;

    vector<string> ReadSignals(istream& input);
    vector<vector<Move>> ReadMealyTable(istream& input);
    void AddInitialState(const string& initialState, const string& defaultOutput);
    void WriteMooreTable(ostream& output);
    int GetMoveIndex(const Move& move) const;
};
