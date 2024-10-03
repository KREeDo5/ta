#include "lab1.h"

struct Move
{
	string s;
	string y;
};

// Поиск хода в векторе
vector<Move>::iterator FindMoveInVector(vector<Move>& vector, const Move& move)
{
	for (int i = 0; i < vector.size(); i++)
	{
		if ((vector[i].s == move.s) && (vector[i].y == move.y)) // сравнение двух состояний
			return vector.begin() + i;
	}
	return vector.end();
}

int main(int argc, char* argv[])
{
	string mode = argv[1];
	if (mode == "moore-to-mealy")
	{
		ifstream input(argv[2]);
		ofstream output(argv[3]);
		map<string, string> moves;
		string tempStr;

		getline(input, tempStr);

		size_t pos = tempStr.find(';');
		if (pos != string::npos)
		{
			tempStr = tempStr.substr(pos + 1);  // Убираем всё до первого ';'
		}

		vector<string> listOfY;
		stringstream ss(tempStr);
		string item;

		while (getline(ss, item, ';'))
		{
			listOfY.push_back(item);
		}

		getline(input, tempStr);
		output << tempStr << endl; //вывод первой строки _|a0|a1|a2|a3|a4|

		while (getline(input, tempStr))
		{
			size_t pos = 0;
			int count = 0; // Счетчик для отслеживания количества ';'
			size_t yIndex = 0;

			while ((pos = tempStr.find(';', pos)) != string::npos)
			{
				count++;
				// Если это второй или последующий ';' и есть элементы в listOfY
				if (count > 1 && yIndex < listOfY.size())
				{
					tempStr.insert(pos, "/" + listOfY[yIndex]);
					pos += listOfY[yIndex].length() + 1;
					yIndex++;
				}
				pos++;
			}

			if (yIndex < listOfY.size()) {
				tempStr += "/" + listOfY[yIndex]; // Добавляем оставшийся элемент перед концом строки
			}

			output << tempStr << endl;
		}

		input.close();
		output.close();
		return 0;
	}
	else if (mode == "mealy-to-moore")
	{
        ifstream input(argv[2]);
        string tempStr;
        getline(input, tempStr);

		size_t pos = tempStr.find(';');
		if (pos != string::npos) 
		{
			tempStr = tempStr.substr(pos + 1);  // Убираем всё до первого ';'
		}

        vector<string> listOfS;
        stringstream ss(tempStr);
        string state;
        while (getline(ss, state, ';')) 
		{
            listOfS.push_back(state);  // Храним состояния
        }

        vector<vector<Move>> table;
        vector<string> listOfX;
        vector<Move> listOfQ;  // Список состояний автомата Мура
        while (getline(input, tempStr)) 
		{
            vector<Move> string;
            stringstream rowStream(tempStr);
            std::string inputSignal;
            getline(rowStream, inputSignal, ';');
            listOfX.push_back(inputSignal);

            std::string tempMove;
            Move move;
            while (getline(rowStream, tempMove, ';'))
			{
                size_t pos = tempMove.find('/');
                move.s = tempMove.substr(0, pos);
                move.y = tempMove.substr(pos + 1);
                string.push_back(move);

                if (FindMoveInVector(listOfQ, move) == listOfQ.end())
				{
                    listOfQ.push_back(move);  // Добавляем уникальные состояния
                }
            }
            table.push_back(string);
        }
        input.close();

        // Сортировка состояний автомата Мура
        sort(
			listOfQ.begin(), 
			listOfQ.end(), 
			[](const Move& a, const Move& b) 
			{
				return a.s < b.s;
			}
		);

        ofstream output(argv[3]);
 
		// Вывод таблицы Мура
        output << ";";
        for (const auto& move : listOfQ)
		{
            output << move.y << ";";
        }
        output << endl;

        output << ";";
        for (size_t i = 0; i < listOfQ.size(); ++i)
		{
            output << "q" << i << ";";
        }
        output << endl;

        for (size_t i = 0; i < listOfX.size(); ++i)
		{
            output << listOfX[i] << ";";
            for (size_t j = 0; j < listOfQ.size(); ++j)
			{
                Move tempMove = table[i][distance(listOfS.begin(),
                    find(listOfS.begin(), listOfS.end(), listOfQ[j].s))];
                output << "q" << distance(listOfQ.begin(), FindMoveInVector(listOfQ, tempMove)) << ";";
            }
            output << endl;
        }

        output.close();
	}
	else
	{
		cerr << "Некорректный режим. Используйте mealy-to-moore или moore-to-mealy." << endl;
		return 1;
	}
}