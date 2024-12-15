@echo off

echo Run test 1...

main.exe ./tests/left.txt ./tests/output-left.csv
if %errorlevel% neq 0 (
    echo Test failed: tests/left.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 2...

main.exe tests/right.txt tests/output-right.csv
if %errorlevel% neq 0 (
    echo Test failed: tests/right.txt
    pause
    exit /b %errorlevel%
)

echo All tests completed successfully.
pause
