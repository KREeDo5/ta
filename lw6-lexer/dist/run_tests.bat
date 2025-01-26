@echo off

echo Run test example...
main.exe ./test.txt ./output.txt
if %errorlevel% neq 0 (
    echo Test failed test.txt
    pause
    exit /b %errorlevel%
)


echo _______________________________
echo All tests completed successfully.
pause
