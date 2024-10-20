
@echo off
chcp 65001 >nul
REM 先執行 rename_files.py
python rename_files.py 2> error_log.txt
if %ERRORLEVEL%==0 (
    python judge_all.py 2>> error_log.txt
) else (
    echo "rename_files.py 執行失敗，請檢查錯誤"
    type error_log.txt
)
pause