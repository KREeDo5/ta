#pragma once

#include <iostream>
#include <fstream>
#include <sstream>
#include <Windows.h>
#include <vector>

using namespace std;

const string MEALY = "mealy";
const string MOORE = "moore";
const string ERROR_MODE = "Некорректный режим. Введите mealy или moore.";
const string ERROR_ARGC = " <mode> <input_file>.csv <output_file>.csv";