#include "AutomatConverter.h"

enum class Mode
{
    MealyToMoore,
    MooreToMealy,
};

struct Args
{
    Mode mode;
    string input;
    string output;
};

Mode ParseMode(const string& mode)
{
    if (mode == MEALY_TO_MOORE)
    {
        return Mode::MealyToMoore;
    }
    if (mode == MOORE_TO_MEALY)
    {
        return Mode::MooreToMealy;
    }

    throw invalid_argument("Invalid type");
}

static Args ParseArgs(int argc, char* argv[])
{
    if (argc != 4)
    {
        throw invalid_argument("Invalid argument count");
    }

    return
    {
            .mode = ParseMode(argv[1]),
            .input = argv[2],
            .output = argv[3],
    };
}

static void CheckFileOpen(const ifstream& input, const ofstream& output)
{
    if (!input.is_open())
    {
        throw ios_base::failure("Error reading the file");
    }

    if (!output.is_open())
    {
        throw ios_base::failure("Error writing the file");
    }
}

static string ReadCSV(istream& istream)
{
    string result;
    string line;
    while (getline(istream, line))
    {
        result += line + "\n";
    }

    return result;
}

static void PrintData(ostream& ostream, const string& str)
{
    ostream << str;
}

static void ConvertMealyToMoore(istream& input, ostream& output)
{
    auto csv = ReadCSV(input);

    CMealy mealy;
    mealy.FromCSV(csv);

    CMoore moore;
    mealy.ToMoore(moore);
    PrintData(output, moore.ConvertToCSV());
}

static void ConvertMooreToMealy(istream& input, ostream& output)
{
    auto csv = ReadCSV(input);

    CMoore moore;
    moore.FromCSV(csv);

    CMealy mealy;
    moore.ToMealy(mealy);
    PrintData(output, mealy.ConvertToCSV());
}

static void Convert(const string& inputFileName, const string& outputFileName, Mode type)
{
    ifstream input(inputFileName);
    ofstream output(outputFileName);

    CheckFileOpen(input, output);

    if (type == Mode::MealyToMoore)
    {
        ConvertMealyToMoore(input, output);
    }
    if (type == Mode::MooreToMealy)
    {
        ConvertMooreToMealy(input, output);
    }
}

int main(int argc, char* argv[])
{
    try
    {
        auto args = ParseArgs(argc, argv);
        Convert(args.input, args.output, args.mode);

    }
    catch (const exception& e)
    {
        cout << e.what() << endl;
        return 1;
    }

    return 0;
}
