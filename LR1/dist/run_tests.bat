@echo off

echo Run test monkey0...
main.exe ./monkey0.txt ./rule0.txt ./rule1.txt
if %errorlevel% neq 0 (
    echo Test failed monkey0.txt
    pause
    exit /b %errorlevel%
)


echo _______________________________
echo Run test monkey1...
main.exe ./monkey1.txt ./rule0.txt ./rule1.txt
if %errorlevel% neq 0 (
    echo Test failed monkey1.txt
    pause
    exit /b %errorlevel%
)


echo _______________________________
echo Run test monkey2...
main.exe ./monkey2.txt ./rule0.txt ./rule1.txt
if %errorlevel% neq 0 (
    echo Test failed monkey2.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test monkey3...
main.exe ./monkey3.txt ./rule0.txt ./rule1.txt
if %errorlevel% neq 0 (
    echo Test failed monkey3.txt
    pause
    exit /b %errorlevel%
)
echo _______________________________
echo Run test monkey4...
main.exe ./monkey4.txt ./rule0.txt ./rule1.txt
if %errorlevel% neq 0 (
    echo Test failed monkey4.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo All tests completed successfully.
pause
