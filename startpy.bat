@echo off
REM 设置虚拟环境路径
set VENV_PATH=C:\Users\sunny\Documents\python_env\g10_env

REM 设置当前脚本所在目录为变量
set SCRIPT_DIR=%~dp0

REM 激活虚拟环境（注意这是 Windows 的 Scripts 目录）
call "%VENV_PATH%\Scripts\activate.bat"

REM 使用虚拟环境中的 python 运行脚本（确保 py 文件与 bat 文件在同一目录）
python %SCRIPT_DIR%russia_game.py
@REM python %SCRIPT_DIR%pdfhandler.py

REM 执行完毕后停留窗口（可选）
pause
