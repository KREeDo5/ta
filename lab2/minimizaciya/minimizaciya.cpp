#include "minimizaciya.h"

static void MooreMin(istream& input, ostream& output)
{
	cout << "Минимизация Мура";
	Sleep(1000);
}

static void MealyMin(istream& input, ostream& output)
{
    cout << "Минимизация Мили";
    Sleep(1000);
}

int main(int argc, char* argv[])
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	if (argc != 4)
	{
		cerr << argv[0] << " <mode> <input_file>.csv <output_file>.csv" << endl;
		return 1;
	}

	string mode = argv[1];
	ifstream input(argv[2]);
	ofstream output(argv[3]);

	if (mode == "moore")
	{
		MooreMin(input, output);
	}
	else if (mode == "mealy")
	{
		MealyMin(input, output);
	}
	else
	{
		cerr << "Некорректный режим. Введите mealy или moore." << endl;
		return 1;
	}

	return 0;
}
