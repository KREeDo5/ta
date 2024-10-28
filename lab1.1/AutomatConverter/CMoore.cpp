#include "CMoore.h"

void CMoore::FromCSV(const string& csv)
{
    vector<string> lines;

    Split(csv, '\n', lines);
    for (int i = 0; i < lines.size(); ++i)
    {
        auto line = lines[i];
        if (i == 0)
        {
            ReadOutputsCSV(line);
        }
        else if (i == 1)
        {
            ReadStatesCSV(line);
        }
        else
        {
            ReadTransitionsCSV(line);
        }
    }
}

void CMoore::FromData(
    const vector<string>& states,
    const vector<string>& paths,
    const vector<string>& output,
    const vector<vector<string>>& transitions
)
{
    m_states = states;
    m_paths = paths;
    m_output = output;
    m_transitions = transitions;
}

string CMoore::ConvertToCSV()
{
    string csv;
    for (const auto& out : m_output)
    {
        csv.append(";" + out);
    }
    csv.append("\n");
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
            csv.append(";" + j);
        }
        csv.append("\n");
    }
    return csv;
}

void CMoore::ToMealy(CMealy& mealy)
{
    vector<vector<SMealyItem>> transitions;
    for (const auto& row : m_transitions)
    {
        vector<SMealyItem> transitionLine;
        for (const auto& item : row)
        {
            if (auto it = find(m_states.begin(), m_states.end(), item); it != m_states.end())
            {
                auto index = it - m_states.begin();
                transitionLine.push_back(
                    {
                        item,
                        m_output[index]
                    }
                );
            }
        }
        transitions.push_back(transitionLine);
    }
    mealy.FromData(
        m_states,
        m_paths,
        transitions
    );
}

void CMoore::ReadOutputsCSV(const string& line)
{
    vector<string> outputs;
    Split(line, ';', outputs);
    for (const auto& output : outputs)
    {
        if (!output.empty())
        {
            m_output.push_back(output);
        }
    }
}

void CMoore::ReadStatesCSV(const string& line)
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

void CMoore::ReadTransitionsCSV(const string& line)
{
    vector<string> transitions;
    Split(line, ';', transitions);
    auto path = transitions[0];
    m_paths.push_back(path);
    vector<string> transitionLine;
    for (int i = 1; i < transitions.size(); ++i)
    {
        transitionLine.push_back(transitions[i]);
    }
    m_transitions.push_back(transitionLine);
}
