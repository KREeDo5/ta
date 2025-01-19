@echo off

echo Run test 1...
main.exe
if %errorlevel% neq 0 (
    echo Test failed main.exe
    pause
    exit /b %errorlevel%
)

echo
@REM main.exe ./tests/test.csv ./tests/output.csv
@REM if %errorlevel% neq 0 (
@REM     echo Test failed: test.csv
@REM     pause
@REM     exit /b %errorlevel%
@REM )

@REM echo _______________________________

echo All tests completed successfully.
pause
