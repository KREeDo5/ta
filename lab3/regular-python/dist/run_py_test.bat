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

echo _______________________________
echo Run test 3...

main.exe tests/right2.txt tests/output-right2.csv
if %errorlevel% neq 0 (
    echo Test failed: tests/right2.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test 4...

main.exe tests/inputRight1.txt tests/output-right3.csv
if %errorlevel% neq 0 (
    echo Test failed: tests/inputRight1.txt
    pause
    exit /b %errorlevel%
)

echo All tests completed successfully.
pause
