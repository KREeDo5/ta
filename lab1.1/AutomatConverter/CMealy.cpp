#include "CMealy.h"

void CMealy::FromCSV(const string& csv)
{
    vector<string> lines;

    Split(csv, '\n', lines);

    for (int i = 0; i < lines.size(); ++i)
    {
        auto line = lines[i];
        if (i == 0)
        {
            ReadStatesCSV(line);
        }
        else
        {
            ReadTransitionsCSV(line);
        }
    }
}

void CMealy::FromData(
    const vector<string>& states,
    const vector<string>& paths,
    const vector<vector<SMealyItem>>& transitions
)
{
    m_states = states;
    m_paths = paths;
    m_transitions = transitions;
}

string CMealy::ConvertToCSV()
{
    string csv;
    for (const auto& st : m_states)
    {
        csv.append(";" + st);
    }
    csv.append("\n");
    for (int i = 0; i < m_paths.size(); ++i)
    {
        csv.append(m_paths[i]);
        for (auto& j : m_transitions[i])
        {
            csv.append(";" + j.to + "/" + j.out);
        }
        csv.append("\n");
    }
    return csv;
}

void CMealy::ToMoore(CMoore& moore)
{
    vector<string> ids;
    vector<string> statesTransitions;
    vector<string> outs;
    for (const auto& lines : m_transitions)
    {
        for (const auto& transition : lines)
        {
            auto id = transition.to + transition.out;
            if (find(ids.begin(), ids.end(), id) == ids.end())
            {
                ids.push_back(id);
                statesTransitions.push_back(transition.to);
                outs.push_back(transition.out);
            }
        }
    }

    vector<string> newStates;
    for (int i = 0; i < ids.size(); ++i)
    {
        newStates.push_back("S" + to_string(i));
    }

    vector<vector<string>> transitions;
    for (const auto& row : m_transitions)
    {
        vector<string> transitionsLine(statesTransitions.size());
        for (int i = 0; i < statesTransitions.size(); ++i)
        {
            if (auto it = find(m_states.begin(), m_states.end(), statesTransitions[i]); it != m_states.end())
            {
                auto index = it - m_states.begin();
                auto oldState = row[index];
                if (auto it2 = find(ids.begin(), ids.end(), oldState.to + oldState.out); it2 != ids.end())
                {
                    auto index2 = it2 - ids.begin();
                    transitionsLine[i] = newStates[index2];
                }
            }
        }
        transitions.push_back(transitionsLine);
    }

    moore.FromData(
        newStates,
        m_paths,
        outs,
        transitions
    );
}

void CMealy::ReadStatesCSV(const string& line)
{
    vector<string> states;
    Split(line, ';', states);
    for (const auto& state : states)
    {
        if (!state.empty())
        {
            m_states.push_back(state);
        }
    }
}

void CMealy::ReadTransitionsCSV(const string& line)
{
    vector<string> transitions;
    Split(line, ';', transitions);
    auto path = transitions[0];
    m_paths.push_back(path);
    vector<SMealyItem> transitionLine;
    for (int i = 1; i < transitions.size(); ++i)
    {
        auto transition = transitions[i];
        vector<string> items;
        Split(transition, '/', items);
        transitionLine.push_back(
            SMealyItem{ 
                items[0], 
                items[1]
            }
        );
    }
    m_transitions.push_back(transitionLine);
}
