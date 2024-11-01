#include "CMinimizer.h"
#include <algorithm>
#include <string>

string CreateUniqueStr(const vector<string>& uniques)
{
    string result;
    for (const auto& unique : uniques)
    {
        result += unique;
    }
    return result;
}

void CMinimizer::MealyMinimizer(CMealy &mealy)
{
    auto transitions = mealy.GetTransitions();
    auto statesOld = mealy.GetStates();
    auto states = SelectState(transitions, mealy.GetPaths().size(), statesOld.size());
    auto uniques = SelectUniqueState(states);

    string equivalentString;
    auto uniqueString = CreateUniqueStr(uniques);
    while (equivalentString != uniqueString)
    {
        equivalentString = uniqueString;
        auto newTransitions = CreateNewTransitions(mealy, uniques);
        auto newStates = SelectState(newTransitions, mealy.GetPaths().size(), mealy.GetStates().size());
        uniques = SelectUniqueState(newStates, uniques);
        uniqueString = CreateUniqueStr(uniques);
    }

    vector<string> newState;
    vector<int> indexVec;
    for (int i = 0; i < uniques.size(); ++i)
    {
        auto unique = uniques[i];
        if (find(newState.begin(), newState.end(), unique) == newState.end())
        {
            newState.push_back(unique);
            indexVec.push_back(i);
        }
    }

    vector<vector<Move>> newTransitions;
    for (int i = 0; i < mealy.GetPaths().size(); ++i)
    {
        vector<Move> newTransitionLine;
        for (const auto indexCurrent: indexVec)
        {
            auto item = transitions[i][indexCurrent];
            if (auto it = find(statesOld.begin(), statesOld.end(), item.s); it != statesOld.end())
            {
                auto index = it - statesOld.begin();
                newTransitionLine.push_back({uniques[index], item.y});
            }
        }
        newTransitions.push_back(newTransitionLine);
    }

    mealy.SetStates(newState);
    mealy.SetTransitions(newTransitions);
}

void CMinimizer::MooreMinimizer(CMoore &moore)
{
    auto transitions = moore.GetTransitions();
    auto statesOld = moore.GetStates();
    auto uniques = SelectUniqueState(moore.GetOutput());

    string equivalentString;
    auto uniqueString = CreateUniqueStr(uniques);
    while (equivalentString != uniqueString)
    {
        equivalentString = uniqueString;
        auto newTransitions = CreateNewTransitions(moore, uniques);
        auto newStates = SelectState(newTransitions, moore.GetPaths().size(), moore.GetStates().size());
        uniques = SelectUniqueState(newStates, uniques);
        uniqueString = CreateUniqueStr(uniques);
    }

    vector<string> newState;
    vector<int> indexVec;
    for (int i = 0; i < uniques.size(); ++i)
    {
        auto unique = uniques[i];
        if (find(newState.begin(), newState.end(), unique) == newState.end())
        {
            newState.push_back(unique);
            indexVec.push_back(i);
        }
    }

    vector<vector<string>> newTransitions;
    for (int i = 0; i < moore.GetPaths().size(); ++i)
    {
        vector<string> newTransitionLine;
        for (const auto indexCurrent: indexVec) {
            auto item = transitions[i][indexCurrent];
            if (auto it =find(statesOld.begin(), statesOld.end(), item); it != statesOld.end())
            {
                auto index = it - statesOld.begin();
                newTransitionLine.push_back(uniques[index]);
            } else
            {
                newTransitionLine.emplace_back("");
            }
        }
        newTransitions.push_back(newTransitionLine);
    }

    auto output = moore.GetOutput();
    vector<string> newOutput;
    for (const auto &state: newState)
    {
        if (auto it = find(uniques.begin(), uniques.end(), state); it != newState.end())
        {
            auto index = it - uniques.begin();
            newOutput.push_back(output[index]);
        }
    }

    moore.SetStates(newState);
    moore.SetOutput(newOutput);
    moore.SetTransitions(newTransitions);
}

vector<string> CMinimizer::SelectState(const vector<vector<Move>> &state, size_t rowCount, size_t columnCount)
{
    vector<string> result;

    for (int i = 0; i < columnCount; ++i)
    {
        string columnState;
        for (int j = 0; j < rowCount; ++j)
        {
            columnState += state[j][i].y;
        }
        result.push_back(columnState);
    }

    return result;
}

vector<string> CMinimizer::SelectUniqueState(const vector<string> &data)
{
    vector<string> result;
    string newPrefix(1, data[0][0] == 'A' ? 'B' : 'A');

    vector<string> uniques;
    vector<string> newResStates;
    for (const auto &item: data) {
        if (auto it = find(uniques.begin(), uniques.end(), item); it == uniques.end())
        {
            uniques.push_back(item);
            auto str = newPrefix + to_string(uniques.size());
            newResStates.push_back(str);
            result.push_back(str);
        } else
        {
            auto index = it - uniques.begin();
            result.push_back(newResStates[index]);
        }
    }

    return result;
}

vector<vector<string>> CMinimizer::CreateNewTransitions(const CMealy &mealy, const vector<string> &data)
{
    auto transitions = mealy.GetTransitions();
    auto states = mealy.GetStates();

    vector<vector<string>> result;
    for (auto &transition: transitions)
    {
        vector<string> line;
        for (auto &j: transition)
        {
            if (auto it = find(states.begin(), states.end(), j.s); it != states.end())
            {
                auto index = it - states.begin();
                line.push_back(data[index]);
            }
        }
        result.push_back(line);
    }
    return result;
}

vector<string> CMinimizer::SelectState(const vector<vector<string>> &transitions, size_t rowCount, size_t columnCount)
{
    vector<string> result;

    for (int i = 0; i < columnCount; ++i)
    {
        string columnState;
        for (int j = 0; j < rowCount; ++j)
        {
            columnState += transitions[j][i];
        }

        result.push_back(columnState);
    }

    return result;
}

vector<string> CMinimizer::SelectUniqueState(const vector<string> &data, const vector<string> &oldUnique)
{
    vector<string> result;
    string newPrefix(1, oldUnique[0][0] == 'A' ? 'B' : 'A');

    vector<string> newResStates;
    vector<string> newStrData;
    for (int i = 0; i < data.size(); ++i)
    {
        auto newStr = oldUnique[i] + data[i];
        if (auto it = find(newStrData.begin(), newStrData.end(), newStr); it == newStrData.end())
        {
            newStrData.push_back(newStr);
            auto str = newPrefix + to_string(newStrData.size());
            newResStates.push_back(str);
            result.push_back(str);
        } else
        {
            auto index = it - newStrData.begin();
            result.push_back(newResStates[index]);
        }
    }

    return result;
}

vector<vector<string>> CMinimizer::CreateNewTransitions(const CMoore &moore, const vector<string> &data)
{
    auto transitions = moore.GetTransitions();
    auto states = moore.GetStates();

    vector<vector<string>> result;
    for (auto &transition: transitions)
    {
        vector<string> line;
        for (auto &j: transition)
        {
            if (auto it = find(states.begin(), states.end(), j); it != states.end())
            {
                auto index = it - states.begin();
                line.push_back(data[index]);
            } else
            {
                line.emplace_back("");
            }
        }
        result.push_back(line);
    }
    return result;
}
