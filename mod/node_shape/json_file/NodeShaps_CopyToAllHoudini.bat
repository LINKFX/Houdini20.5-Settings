@echo off
setlocal enabledelayedexpansion

:: 检查管理员权限，如无则提权
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

cd /d "%~dp0"
set "scriptDir=%~dp0"

:: 检查有没有 .json 文件
set "hasJson=0"
for %%f in ("%scriptDir%*.json") do (
    set hasJson=1
    goto :hasJson
)
:hasJson
if "%hasJson%"=="0" (
    echo 未检测到任何 .json 文件，请将 .json 文件与本脚本放在同一文件夹下
    pause
    exit /b
)

echo 正在查找 C:\Program Files\Side Effects Software 下的 Houdini 20.5 及以上版本...

for /D %%a in ("C:\Program Files\Side Effects Software\Houdini *") do (
    set "folderName=%%~nxa"
    set "fullPath=%%a"
    :: 提取版本号
    for /f "tokens=2" %%v in ("%%~nxa") do (
        set "version=%%v"
        for /f "tokens=1,2 delims=." %%x in ("!version!") do (
            set /a "ver_major=%%x"
            set /a "ver_minor=%%y"
            set /a "vercode=100*%%x+%%y"
            if !vercode! geq 2005 (
                echo ----------------------------------------
                echo 找到 Houdini 版本文件夹：!fullPath!

                set "targetDir=!fullPath!\houdini\config\NodeShapes"
                if not exist "!targetDir!" (
                    echo 未检测到子目录 !targetDir!，正在创建...
                    mkdir "!targetDir!"
                )
                echo 正在复制 .json 文件到 !targetDir!
                copy /Y "%scriptDir%*.json" "!targetDir!"
            ) else (
                echo 跳过版本：!fullPath!
            )
        )
    )
)

echo.
echo 复制操作完成，若有错漏请查看上方输出。
pause
