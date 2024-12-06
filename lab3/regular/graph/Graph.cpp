#include "Graph.h"

// Функция для экспорта графа в таблицу CSV
std::vector<std::vector<std::string>> DumpGraphToCSVTable(const CGraph<std::string, std::string>& graph)
{
	// Создание карты для сопоставления сигналов с их позициями в таблице
	std::map<std::string, std::size_t> signalToPosition;
	std::size_t i = 0;
	for (const auto& signal : graph.GetSignals())
	{
		signalToPosition.emplace(signal, i++);
	}

	// Создание карты для сопоставления узлов с их позициями в таблице
	std::map<std::string, std::size_t> nodeToPosition;
	i = 0;
	for (const auto& node : graph.GetNodes())
	{
		nodeToPosition.emplace(node, i++);
	}

	// Определение размеров таблицы
	const std::size_t columnSize = graph.GetSignals().size() + 1;
	const std::size_t rowSize = graph.GetNodes().size() + 1;

	// Создание вектора для хранения столбцов таблицы
	std::vector<std::vector<std::string>> columns(rowSize);

	// Создание первого столбца с сигналами
	std::vector<std::string> signalsColumn(columnSize, "");
	for (const auto& [signal, position] : signalToPosition)
	{
		signalsColumn[position + 1] = signal;
	}
	columns[0] = signalsColumn;

	// Заполнение таблицы переходами
	for (const auto& from : graph.GetNodes())
	{
		std::vector<std::string> column(columnSize, "");
		column[0] = from;

		std::map<std::string, std::string> transitions;
		bool ok;
		std::tie(transitions, ok) = graph.GetTransitionsFromNode(from);

		for (const auto& [to, signal] : transitions)
		{
			std::string& cell = column[signalToPosition[signal] + 1];
			if (!cell.empty())
			{
				cell.append(",");
			}
			cell.append(to);
		}

		columns[nodeToPosition[from] + 1] = column;
	}

	return columns;
}
