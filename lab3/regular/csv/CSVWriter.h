#ifndef CSVWRITER_H
#define CSVWRITER_H

#include "Types.h"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class CSVWriter
{
public:
	explicit CSVWriter(std::ostream& out, char delimiter = ';')
		: m_out(out) // Инициализация потока вывода
		, m_delimiter(delimiter){}; // Разделителя

	// Запись всех данных в CSV файл
	void WriteAll(const Vector2D& data)
	{
		// Проход по всем строкам данных
		for (const auto& row : data)
		{
			std::stringstream oss;
			// Проход по всем ячейкам строки
			for (const auto& cell : row)
			{
				oss << cell << m_delimiter; // Запись ячейки и разделителя в поток
			}
			auto resultRow = oss.str(); // Преобразование потока в строку
			// Запись строки в поток вывода без последнего разделителя
			m_out << resultRow.substr(0, resultRow.length() - 1) << std::endl;
			m_out.flush(); // Принудительная запись данных в поток
		}
	}

private:
	std::ostream& m_out; // Поток вывода
	char m_delimiter; // Разделитель
};

#endif
