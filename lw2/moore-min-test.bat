@echo off

echo Run test 0...

main.exe moore ./moore/input/input0.csv ./moore/output/output0.csv
if %errorlevel% neq 0 (
    echo Test failed: input0
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 1...

main.exe moore ./moore/input/input1.csv ./moore/output/output1.csv
if %errorlevel% neq 0 (
    echo Test failed: input1
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...

main.exe moore ./moore/input/input2.csv ./moore/output/output2.csv
if %errorlevel% neq 0 (
    echo Test failed: input2
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 3...

main.exe moore ./moore/input/input3.csv ./moore/output/output3.csv
if %errorlevel% neq 0 (
    echo Test failed: input3
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 4...

main.exe moore ./moore/input/input4.csv ./moore/output/output4.csv
if %errorlevel% neq 0 (
    echo Test failed: input4
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 5...

main.exe moore ./moore/input/input5.csv ./moore/output/output5.csv
if %errorlevel% neq 0 (
    echo Test failed: input5
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 6...

main.exe moore ./moore/input/input6.csv ./moore/output/output6.csv
if %errorlevel% neq 0 (
    echo Test failed: input6
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 7...

main.exe moore ./moore/input/input7.csv ./moore/output/output7.csv
if %errorlevel% neq 0 (
    echo Test failed: input7
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 8...

main.exe moore ./moore/input/input8.csv ./moore/output/output8.csv
if %errorlevel% neq 0 (
    echo Test failed: input8
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 9...

main.exe moore ./moore/input/input9.csv ./moore/output/output9.csv
if %errorlevel% neq 0 (
    echo Test failed: input9
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo All tests completed successfully.
pause
