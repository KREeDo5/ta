#include "lab1.h"

int main(int argc, char* argv[])
{
	std::string mode = argv[1];
	if (mode == "moore-to-mealy")
	{
		std::ifstream input(argv[2]);
		std::ofstream output(argv[3]);
		std::map<std::string, std::string> moves;
		std::string tempStr;

		{
			getline(input, tempStr);

			size_t pos = tempStr.find(';');
			if (pos != std::string::npos) {
				tempStr = tempStr.substr(pos + 1);  // Убираем всё до первого ';'
			}

			std::vector<std::string> listOfY;
			std::stringstream ss(tempStr);
			std::string item;

			while (getline(ss, item, ';')) {
				listOfY.push_back(item);
			}

			getline(input, tempStr);
			output << tempStr << std::endl;//вывод первой строки _|a0|a1|a2|a3|a4|

			while (getline(input, tempStr)) {
				size_t pos = 0;
				int count = 0; // Счетчик для отслеживания количества ';'
				size_t yIndex = 0;

				while ((pos = tempStr.find(';', pos)) != std::string::npos) {
					count++;
					// Если это второй или последующий ';' и есть элементы в listOfY
					if (count > 1 && yIndex < listOfY.size()) {
						tempStr.insert(pos, "/" + listOfY[yIndex]);
						pos += listOfY[yIndex].length() + 1;
						yIndex++;
					}
					pos++;
				}

				if (yIndex < listOfY.size()) {
					tempStr += "/" + listOfY[yIndex]; // Добавляем оставшийся элемент перед концом строки
				}

				output << tempStr << std::endl;
			}

		}

		input.close();
		output.close();
		return 0;
	}
	else
	{
		std::cout << "Wrong mode";
		return 1;
	}
}