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

using namespace std;

class MachineConverter {
public:
    static void Convert(const string& mode, istream& input, ostream& output);
};