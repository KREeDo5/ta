@echo off

echo Run test 0...

main.exe mealy ./mealy/input/input0.csv ./mealy/output/output0.csv
if %errorlevel% neq 0 (
    echo Test failed: input0
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 1...

main.exe mealy ./mealy/input/input1.csv ./mealy/output/output1.csv
if %errorlevel% neq 0 (
    echo Test failed: input1
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...

main.exe mealy ./mealy/input/input2.csv ./mealy/output/output2.csv
if %errorlevel% neq 0 (
    echo Test failed: input2
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 3...

main.exe mealy ./mealy/input/input3.csv ./mealy/output/output3.csv
if %errorlevel% neq 0 (
    echo Test failed: input3
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 4...

main.exe mealy ./mealy/input/input4.csv ./mealy/output/output4.csv
if %errorlevel% neq 0 (
    echo Test failed: input4
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 5...

main.exe mealy ./mealy/input/input5.csv ./mealy/output/output5.csv
if %errorlevel% neq 0 (
    echo Test failed: input5
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 6...

main.exe mealy ./mealy/input/input6.csv ./mealy/output/output6.csv
if %errorlevel% neq 0 (
    echo Test failed: input6
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 7...

main.exe mealy ./mealy/input/input7.csv ./mealy/output/output7.csv
if %errorlevel% neq 0 (
    echo Test failed: input7
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 8...

main.exe mealy ./mealy/input/input8.csv ./mealy/output/output8.csv
if %errorlevel% neq 0 (
    echo Test failed: input8
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 9...

main.exe mealy ./mealy/input/input9.csv ./mealy/output/output9.csv
if %errorlevel% neq 0 (
    echo Test failed: input9
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 10...

main.exe mealy ./mealy/input/input10.csv ./mealy/output/output10.csv
if %errorlevel% neq 0 (
    echo Test failed: input10
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo All tests completed successfully.
pause
