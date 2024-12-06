#ifndef CSVREADER_H
#define CSVREADER_H

#include "Types.h"
#include <sstream>
#include <string>
#include <vector>

class CSVReader
{
public:
	explicit CSVReader(std::istream& in, char delimiter = ';')
		: m_in(in) // Инициализация потока ввода
		, m_delimiter(delimiter) // разделитель
	{
	}

	// Чтение всех данных из CSV файла
	[[nodiscard]]
	Vector2D ReadAll()
	{
		Vector2D result; // Результирующий вектор

		// Чтение строк из потока ввода
		for (std::string line; std::getline(m_in, line);)
		{
			std::stringstream lineStream(line); // Создание строкового потока
			std::vector<std::string> row; // Вектор для хранения строки
			// Чтение ячеек строки
			for (std::string cell; std::getline(lineStream, cell, m_delimiter);)
			{
				row.push_back(cell); // Добавление ячейки в строку
			}
			result.push_back(row); // Добавление строки в результирующий вектор
		}

		return std::move(result); // Возврат результирующего вектора
	}

private:
	std::istream& m_in; // Поток ввода
	char m_delimiter; // Разделитель
};

#endif
