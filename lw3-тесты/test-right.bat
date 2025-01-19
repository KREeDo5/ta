@echo off

echo Run test 0...

main.exe ./right/input/input0.txt ./right/output/output0.csv
if %errorlevel% neq 0 (
    echo Test failed: input0.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 1...

main.exe ./right/input/input1.txt ./right/output/output1.csv
if %errorlevel% neq 0 (
    echo Test failed: input1.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...

main.exe ./right/input/input2.txt ./right/output/output2.csv
if %errorlevel% neq 0 (
    echo Test failed: input2.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________

echo All tests completed successfully.
pause
