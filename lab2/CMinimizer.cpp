#include "CMinimizer.h"

void CMinimizer::MealyMinimizer(CMealy& mealy)
{
    auto transitions = mealy.GetTransitions();                                          // переходы автомата
    auto statesOld = mealy.GetStates();                                                 // состояния автомата
    auto states = SelectState(transitions, mealy.GetPaths().size(), statesOld.size());  // состояния на основе переходов
    auto uniques = SelectUniqueState(states);

    std::string equivalentString;
    auto uniqueString = CreateUniqueStr(uniques);
    // обновляем переходы и состояния до тех пор, пока уникальные состояния не перестанут изменяться
    while (equivalentString != uniqueString)
    {
        equivalentString = uniqueString;
        auto newTransitions = CreateNewTransitions(mealy, uniques);
        auto newStates = SelectState(newTransitions, mealy.GetPaths().size(), mealy.GetStates().size());
        uniques = SelectUniqueState(newStates, uniques);
        uniqueString = CreateUniqueStr(uniques);
    }

    // создаём новые состояния и переходы
    std::vector<std::string> newState;  // новые состояния
    std::vector<int> indexVec;          // индексы уникальных состояний

    for (int i = 0; i < uniques.size(); ++i)
    {
        auto unique = uniques[i];
        // если состояние уникальное, то добавляем его в новый вектор состояний
        if (std::find(newState.begin(), newState.end(), unique) == newState.end())
        {
            newState.push_back(unique);
            indexVec.push_back(i);
        }
    }

    // проходим по всем путям автомата
    std::vector<std::vector<SMealyItem>> newTransitions;
    for (int i = 0; i < mealy.GetPaths().size(); ++i)
    {
        std::vector<SMealyItem> newTransitionLine;

        // для каждого индекса уникального состояния находим соответствующий переход и добавляем его в новый вектор переходов
        for (const auto indexCurrent : indexVec)
        {
            auto item = transitions[i][indexCurrent];
            if (auto it = std::find(statesOld.begin(), statesOld.end(), item.to); it != statesOld.end())
            {
                auto index = it - statesOld.begin();
                newTransitionLine.push_back({ uniques[index], item.out });
            }
        }
        newTransitions.push_back(newTransitionLine);
    }

    mealy.SetStates(newState);
    mealy.SetTransitions(newTransitions);
}

void CMinimizer::MooreMinimizer(CMoore& moore)
{
    auto transitions = moore.GetTransitions();           //переходы автомата
    auto statesOld = moore.GetStates();                  //состояния автомата
    auto uniques = SelectUniqueState(moore.GetOutput());

    // обновляем переходы и состояния до тех пор, пока уникальные состояния не перестанут изменяться
    std::string equivalentString;
    auto uniqueString = CreateUniqueStr(uniques);
    while (equivalentString != uniqueString)
    {
        equivalentString = uniqueString;
        auto newTransitions = CreateNewTransitions(moore, uniques);
        auto newStates = SelectState(newTransitions, moore.GetPaths().size(), moore.GetStates().size());
        uniques = SelectUniqueState(newStates, uniques);
        uniqueString = CreateUniqueStr(uniques);
    }

    // Создание новых состояний, переходов и выходов:
    std::vector<std::string> newState;
    std::vector<int> indexVec;
    for (int i = 0; i < uniques.size(); ++i)
    {
        auto unique = uniques[i];

        // если состояние уникальное, то добавляем его в новый вектор состояний
        if (std::find(newState.begin(), newState.end(), unique) == newState.end())
        {
            newState.push_back(unique);
            indexVec.push_back(i);
        }
    }

    // проходим по всем путям
    std::vector<std::vector<std::string>> newTransitions;
    for (int i = 0; i < moore.GetPaths().size(); ++i)
    {
        std::vector<std::string> newTransitionLine;

        // для каждого индекса уникального состояния находим соответствующий переход и добавляем его в новый вектор переходов
        for (const auto indexCurrent : indexVec)
        {
            auto item = transitions[i][indexCurrent];
            if (auto it = std::find(statesOld.begin(), statesOld.end(), item); it != statesOld.end())
            {
                auto index = it - statesOld.begin();
                newTransitionLine.push_back(uniques[index]);
            }
            else
            {
                newTransitionLine.emplace_back("");
            }
        }
        newTransitions.push_back(newTransitionLine);
    }

    // создание нового выходного вектора
    auto output = moore.GetOutput();
    std::vector<std::string> newOutput;
    for (const auto& state : newState)
    {
        if (auto it = std::find(uniques.begin(), uniques.end(), state); it != uniques.end())
        {
            auto index = it - uniques.begin();
            newOutput.push_back(output[index]);
        }
    }

    moore.SetStates(newState);
    moore.SetOutput(newOutput);
    moore.SetTransitions(newTransitions);
}

std::vector<std::string> CMinimizer::SelectState(std::vector<std::vector<SMealyItem>> state, size_t rowCount, size_t columnCount)
{
    std::vector<std::string> result;

    // проходим по всем столбцам
    for (int i = 0; i < columnCount; ++i)
    {
        std::string columnState;

        // проходим по всем строкам и собираем выходы в строку
        for (int j = 0; j < rowCount; ++j)
        {
            columnState += state[j][i].out;
        }
        result.push_back(columnState);
    }

    return result;
}

std::vector<std::string> CMinimizer::SelectUniqueState(const std::vector<std::string>& data)
{
    std::vector<std::string> result;

    // Определяем отличающийся от первого символа префикс первого эл-та data
    std::string newPrefix(1, data[0][0] == FIRST_PREFIX ? SECOND_PREFIX : FIRST_PREFIX);

    std::vector<std::string> uniques;
    std::vector<std::string> newResStates;
    for (const auto& item : data)
    {
        // Если состояние уникально, добавляем его в вектор уникальных состояний
        if (auto it = std::find(uniques.begin(), uniques.end(), item); it == uniques.end())
        {
            uniques.push_back(item);
            // Создаем новое уникальное состояние с новым префиксом и добавляем его в вектор новых состояний
            auto str = newPrefix + std::to_string(uniques.size());
            newResStates.push_back(str);
            result.push_back(str);
        }
        // Если состояние не уникально, находим его индекс и добавляем соответствующее новое состояние в результат
        else
        {
            auto index = it - uniques.begin();
            result.push_back(newResStates[index]);
        }
    }

    return result;
}

std::vector<std::vector<std::string>> CMinimizer::CreateNewTransitions(const CMealy& mealy, const std::vector<std::string>& data)
{
    auto transitions = mealy.GetTransitions();
    auto states = mealy.GetStates();

    std::vector<std::vector<std::string>> result;
    for (auto& transition : transitions)
    {
        std::vector<std::string> line;
        for (auto& j : transition)
        {
            // Находим индекс состояния в векторе состояний
            if (auto it = std::find(states.begin(), states.end(), j.to); it != states.end())
            {
                auto index = it - states.begin();

                // Добавляем новое состояние в строку переходов
                line.push_back(data[index]);
            }
        }

        // Добавляем строку переходов в результат
        result.push_back(line);
    }
    return result;
}

std::vector<std::string> CMinimizer::SelectState(const std::vector<std::vector<std::string>>& transitions, size_t rowCount, size_t columnCount)
{
    std::vector<std::string> result;

    // Проходим по всем столбцам
    for (int i = 0; i < columnCount; ++i)
    {
        std::string columnState;

        // Проходим по всем строкам и собираем выходы в строку
        for (int j = 0; j < rowCount; ++j)
        {
            columnState += transitions[j][i];
        }

        // Добавляем строку состояний в результат
        result.push_back(columnState);
    }

    return result;
}

std::vector<std::string> CMinimizer::SelectUniqueState(const std::vector<std::string>& data, const std::vector<std::string>& oldUnique)
{
    std::vector<std::string> result;

    // Определяем отличающийся от первого символа префикс первого эл-та oldUnique
    std::string newPrefix(1, oldUnique[0][0] == FIRST_PREFIX ? SECOND_PREFIX : FIRST_PREFIX);

    std::vector<std::string> newResStates;
    std::vector<std::string> newStrData;
    for (int i = 0; i < data.size(); ++i)
    {
        // Создаем новую строку, объединяя старое уникальное состояние и текущее состояние
        auto newStr = oldUnique[i] + data[i];

        // Если новая строка уникальна, добавляем ее в вектор новых строк данных
        if (auto it = std::find(newStrData.begin(), newStrData.end(), newStr); it == newStrData.end())
        {
            newStrData.push_back(newStr);

            // Создаем новое уникальное состояние с новым префиксом и добавляем его в вектор новых состояний
            auto str = newPrefix + std::to_string(newStrData.size());
            newResStates.push_back(str);
            result.push_back(str);
        }
        else // Если новая строка не уникальна, находим ее индекс и добавляем соответствующее новое состояние в результат
        {
            auto index = it - newStrData.begin();
            result.push_back(newResStates[index]);
        }
    }

    return result;
}

std::vector<std::vector<std::string>> CMinimizer::CreateNewTransitions(const CMoore& moore, const std::vector<std::string>& data)
{
    auto transitions = moore.GetTransitions();
    auto states = moore.GetStates();

    std::vector<std::vector<std::string>> result;
    for (auto& transition : transitions)
    {
        std::vector<std::string> line;
        for (auto& j : transition)
        {
            // Находим индекс состояния в векторе состояний
            if (auto it = std::find(states.begin(), states.end(), j); it != states.end())
            {
                auto index = it - states.begin();

                // Добавляем новое состояние в строку переходов
                line.push_back(data[index]);
            }
            else  // Если состояние не найдено, добавляем пустую строку
            {
                line.emplace_back("");
            }
        }
        result.push_back(line);
    }
    return result;
}
