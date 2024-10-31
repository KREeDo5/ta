#include "CMoore.h"
#include "CMealy.h"
#include <sstream>

vector<string> CMoore::ReadSignals(istream& input) {
    string tempStr;
    vector<string> listOfY;
    string item;

    getline(input, tempStr);
    size_t pos = tempStr.find(';');
    if (pos != string::npos) {
        tempStr = tempStr.substr(pos + 1);
    }

    stringstream ss(tempStr);

    while (getline(ss, item, ';')) {
        listOfY.push_back(item);
    }
    return listOfY;
}

void CMoore::Read(istream& input) {
    listOfY = ReadSignals(input);
    string tempStr;
    getline(input, tempStr);
    while (getline(input, tempStr)) {
        vector<string> row;
        stringstream ss(tempStr);
        string item;
        while (getline(ss, item, ';')) {
            row.push_back(item);
        }
        table.push_back(row);
    }
}

void CMoore::Write(ostream& output) {
    output << ";";
    for (const auto& y : listOfY) {
        output << y << ";";
    }
    output << endl;

    for (const auto& row : table) {
        for (const auto& item : row) {
            output << item << ";";
        }
        output << endl;
    }
}

void CMoore::ConvertToMealy(ostream& output) {
    output << ";";
    for (const auto& y : listOfY) {
        output << y << ";";
    }
    output << endl;

    for (const auto& row : table) {
        for (const auto& item : row) {
            output << item << ";";
        }
        output << endl;
    }

    string tempStr;
    for (const auto& row : table) {
        size_t pos = 0;
        int count = 0;
        size_t yIndex = 0;

        for (const auto& item : row) {
            if (count > 0 && yIndex < listOfY.size()) {
                tempStr += item + "/" + listOfY[yIndex] + ";";
                yIndex++;
            }
            else {
                tempStr += item + ";";
            }
            count++;
        }

        if (yIndex < listOfY.size()) {
            tempStr += "/" + listOfY[yIndex];
        }

        output << tempStr << endl;
        tempStr.clear();
    }
}
