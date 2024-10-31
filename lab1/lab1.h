#pragma once

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <string>
#include <Windows.h>
#include <algorithm>

using namespace std;

class MachineConverter {
public:
    static void Convert(const string& mode, istream& input, ostream& output);
};