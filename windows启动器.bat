@echo off
cd %~dp0

:: 检查Python是否已经安装
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ 你的电脑不支持，请自行安装python3后重试！
    pause
    exit /b
)

:: 尝试运行Python脚本
python byxxp.py 2>nul
if errorlevel 1 (
    echo ⚠️ 组件安装中，请稍后！
    pip install os re datetime chardet openpyxl pandas
    python byxxp.py
)