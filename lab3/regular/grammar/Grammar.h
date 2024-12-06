// Защита от повторного включения файла
#ifndef GRAMMAR_H
#define GRAMMAR_H

#include "../graph/CGraph.h"
#include <map>
#include <set>
#include <string>

// Функция для парсинга правил грамматики из входного потока
std::map<std::string, std::set<std::string>> ParseRules(std::istream& in);

// Функция для построения графа левой грамматики на основе правил
CGraph<std::string, std::string> BuildLeftGrammarGraph(const std::map<std::string, std::set<std::string>>& rules);

// Функция для построения графа правой грамматики на основе правил
CGraph<std::string, std::string> BuildRightGrammarGraph(const std::map<std::string, std::set<std::string>>& rules);

#endif
