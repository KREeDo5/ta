#pragma once

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <Windows.h>
#include <algorithm>

#include "CMealy.h"
#include "CMoore.h"
#include "CMinimizer.h"

using namespace std;

class MachineConverter
{
    private:
        static void MinimizeMealy(istream& input, ostream& output);
        static void MinimizeMoore(istream& input, ostream& output);

    public:
        static void Convert(const string& mode, istream& input, ostream& output);
};