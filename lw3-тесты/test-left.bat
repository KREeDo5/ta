@echo off

echo Run test 1...

main.exe ./left/input/input0.txt ./left/output/output0.csv
if %errorlevel% neq 0 (
    echo Test failed: input0.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________

echo All tests completed successfully.
pause
