#include "regular.h"

int main(int argc, char* argv[])
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	auto args = Args::ParseFromArgs(argc, argv);
	if (!args)
	{
		return EXIT_FAILURE;
	}

	std::map<std::string, std::set<std::string>> rules;
	{
		std::ifstream inputFile(args->GetInputFilePath());
		if (!inputFile.good())
		{
			std::cerr << "Ошибка: не удалось открыть входной файл" << std::endl;
			return EXIT_FAILURE;
		}

		rules = ParseRules(inputFile);

		inputFile.close();
	}

	CGraph<std::string, std::string> graph;

	switch (args->GetGrammarType())
	{
	case GrammarType::LEFT:
		graph = BuildLeftGrammarGraph(rules);
		break;
	case GrammarType::RIGHT:
		graph = BuildRightGrammarGraph(rules);
		break;
	}

	auto table = DumpGraphToCSVTable(graph);

	{
		std::ofstream outputFile(args->GetOutputFilePath());
		if (!outputFile.good())
		{
			std::cerr << "Ошибка: не удалось открыть выходной файл" << std::endl;
			return EXIT_FAILURE;
		}

		CSVWriter csvWriter(outputFile);
		csvWriter.WriteAll(table);
		outputFile.close();
	}

	return EXIT_SUCCESS;
}