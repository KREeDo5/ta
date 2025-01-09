@echo off

echo Run test 1...
main.exe
if %errorlevel% neq 0 (
    echo Test failed main.exe
    pause
    exit /b %errorlevel%
)

echo
@REM main.exe ./tests/mealy-input.txt ./tests/output-mealy.csv
@REM if %errorlevel% neq 0 (
@REM     echo Test failed: tests/mealy-input.txt
@REM     pause
@REM     exit /b %errorlevel%
@REM )

@REM echo _______________________________
@REM echo Run test 2...

@REM main.exe tests/moore-input.txt tests/output-moore.csv
@REM if %errorlevel% neq 0 (
@REM     echo Test failed: tests/moore-input.txt
@REM     pause
@REM     exit /b %errorlevel%
@REM )

echo All tests completed successfully.
pause
