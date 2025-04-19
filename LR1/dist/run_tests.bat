@echo off

echo Run test monkey1...
main.exe ./monkey1.txt ./monkey-output-1.txt monkey
if %errorlevel% neq 0 (
    echo Test failed monkey1.txt
    pause
    exit /b %errorlevel%
)


echo _______________________________
echo Run test monkey2...
main.exe ./monkey2.txt ./monkey-output-2.txt monkey
if %errorlevel% neq 0 (
    echo Test failed monkey2.txt
    pause
    exit /b %errorlevel%
)


echo _______________________________
echo Run test monkey3...
main.exe ./monkey3.txt ./monkey-output-3.txt monkey
if %errorlevel% neq 0 (
    echo Test failed monkey3.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test monkey4...
main.exe ./monkey4.txt ./monkey-output-4.txt monkey
if %errorlevel% neq 0 (
    echo Test failed monkey4.txt
    pause
    exit /b %errorlevel%
)

echo _______________________________
echo Run test monkey5...
main.exe ./monkey5.txt ./monkey-output-5.txt monkey
if %errorlevel% neq 0 (
    echo Test failed monkey5.txt
    pause
    exit /b %errorlevel%
)



echo _______________________________
echo All tests completed successfully.
pause
