#include "utils.h"

void Split(string const& str, char separator, vector<string>& out)
{
    stringstream ss(str);
    string s;
    while (getline(ss, s, separator))
    {
        out.push_back(s);
    }
}
