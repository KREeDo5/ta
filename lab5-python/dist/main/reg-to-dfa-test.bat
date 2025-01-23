@echo off

echo Run test 1...

main.exe ./input/input1.txt ./output/output1
if %errorlevel% neq 0 (
    echo Test failed: input1
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...

main.exe ./input/input2.txt ./output/output2
if %errorlevel% neq 0 (
    echo Test failed: input2
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 3...

main.exe ./input/input3.txt ./output/output3
if %errorlevel% neq 0 (
    echo Test failed: input3
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 4...

main.exe ./input/input4.txt ./output/output4
if %errorlevel% neq 0 (
    echo Test failed: input4
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 5...

main.exe ./input/input5.txt ./output/output5
if %errorlevel% neq 0 (
    echo Test failed: input5
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 6...

main.exe ./input/input6.txt ./output/output6
if %errorlevel% neq 0 (
    echo Test failed: input6
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 7...

main.exe ./input/input7.txt ./output/output7
if %errorlevel% neq 0 (
    echo Test failed: input7
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 8...

main.exe ./input/input8.txt ./output/output8
if %errorlevel% neq 0 (
    echo Test failed: input8
    pause
    exit /b %errorlevel%
)

echo _______________________________

echo All tests completed successfully.
pause
