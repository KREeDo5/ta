#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <sstream>

#include "CMealy.h"
#include "CMinimizer.h"

using namespace std;

class CMoore
{
    private:
        vector<string> ReadSignals(istream& input);

    public:
        void Read(istream& input);
        void Write(ostream& output);
        void ConvertToMealy(ostream& output);
        void Minimize();
};
