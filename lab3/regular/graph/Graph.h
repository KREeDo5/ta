#ifndef GRAPH_H
#define GRAPH_H

#include "CGraph.h"
#include <ostream>
#include <string>
#include <vector>

std::vector<std::vector<std::string>> DumpGraphToCSVTable(const CGraph<std::string, std::string>& graph);

#endif
