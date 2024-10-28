#pragma once
#include "CMealy.h"
#include "utils.h"
#include <algorithm>
#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

class CMealy;

class CMoore
{
    public:
        CMoore() = default;
        void FromCSV(const string& csv);
        void FromData(
            const vector<string>& states,
            const vector<string>& paths,
            const vector<string>& output,
            const vector<vector<string>>& transitions
        );
        string ConvertToCSV();
        void ToMealy(CMealy& mealy);

    private:
        void ReadOutputsCSV(const string& line);
        void ReadStatesCSV(const string& line);
        void ReadTransitionsCSV(const string& line);

        vector<string> m_states;
        vector<string> m_paths;
        vector<string> m_output;
        vector<vector<string>> m_transitions;
};
