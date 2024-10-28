#pragma once
#include "CMoore.h"
#include "utils.h"
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

class CMoore;

struct SMealyItem
{
    string to;
    string out;
};

class CMealy
{
    public:
        CMealy() = default;
        void FromCSV(const string& csv);
        void FromData(
            const vector<string>& states,
            const vector<string>& paths,
            const vector<vector<SMealyItem>>& transitions
        );
        string ConvertToCSV();
        void ToMoore(CMoore& moore);

    private:
        void ReadStatesCSV(const string& line);
        void ReadTransitionsCSV(const string& line);

        vector<string> m_states;
        vector<string> m_paths;
        vector<vector<SMealyItem>> m_transitions;
};
