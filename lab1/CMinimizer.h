#pragma once

#include "CMealy.h"
#include "CMoore.h"

struct Move
{
    string s;
    string y;

    bool operator==(const Move& other) const
    {
        return s == other.s && y == other.y;
    }
};

class CMinimizer
{
    private:
        static vector<string> SelectState(const vector<vector<Move>> &data, size_t rowCount, size_t columnCount);
        static vector<string> SelectState(const vector<vector<string>> &transitions, size_t rowCount, size_t columnCount);
        static vector<string> SelectUniqueState(const vector<string> &data);
        static vector<string> SelectUniqueState(const vector<string> &data, const vector<string> &oldUnique);
        static vector<vector<string>> CreateNewTransitions(const CMealy &mealy, const vector<string> &data);
        static vector<vector<string>> CreateNewTransitions(const CMoore &moore, const vector<string> &data);

    public:
        static void MealyMinimizer(CMealy &mealy);
        static void MooreMinimizer(CMoore &moore);
};
