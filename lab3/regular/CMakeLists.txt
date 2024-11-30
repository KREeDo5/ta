cmake_minimum_required (VERSION 3.8)

project (regular)

set(CMAKE_CXX_STANDARD 20)

add_executable (
	regular
	regular.cpp
	regular.h
	args.h
	csv/CSVReader.h
	csv/CSVWriter.h
	grammar/Grammar.cpp
	grammar/Grammar.h
	grammar/GrammarType.h
	graph/CGraph.h
	graph/Graph.cpp
	graph/Graph.h
)
