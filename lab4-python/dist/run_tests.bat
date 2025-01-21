@echo off

echo Run test 1...
main.exe ./tests/test.csv ./tests/output/output-test.csv
if %errorlevel% neq 0 (
    echo Test failed test.csv
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...
main.exe ./tests/input0.csv ./tests/output/output0.csv
if %errorlevel% neq 0 (
    echo Test failed input0.csv
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 3...
main.exe ./tests/input1.csv ./tests/output/output1.csv
if %errorlevel% neq 0 (
    echo Test failed input1.csv
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 4...
main.exe ./tests/input2.csv ./tests/output/output2.csv
if %errorlevel% neq 0 (
    echo Test failed input2.csv
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 5...
main.exe ./tests/input3.csv ./tests/output/output3.csv
if %errorlevel% neq 0 (
    echo Test failed input3.csv
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo All tests completed successfully.
pause
