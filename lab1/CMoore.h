#pragma once

#include <iostream>
#include <vector>
#include <string>
#include "CMealy.h" // Добавляем включение заголовочного файла CMealy.h

using namespace std;

class CMoore {
public:
    void Read(istream& input);
    void Write(ostream& output);
    void ConvertToMealy(ostream& output);

private:
    vector<string> listOfY;
    vector<vector<string>> table;

    vector<string> ReadSignals(istream& input);
};
