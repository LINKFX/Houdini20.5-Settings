@echo off
:: 若没有管理员权限，自动以管理员身份重新启动脚本
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

:: 切换工作目录至脚本所在目录
cd /d "%~dp0"
set "scriptDir=%~dp0"

:: 需要复制的文件
set "file1=3DSceneColors.bw"

:: 如果文件不存在就退出
if not exist "%scriptDir%%file1%" (
    echo 未找到 %file1% 文件，请将 %file1% 与本脚本放在同一文件夹下
    pause
    exit /b
)

echo 正在查找安裝在 "C:\Program Files\Side Effects Software" 下的 Houdini 版本...

:: 遍历 "C:\Program Files\Side Effects Software" 下与 "Houdini " 开头匹配的文件夹
for /D %%a in ("C:\Program Files\Side Effects Software\Houdini *") do (
    if /I not "%%~nxa"=="Houdini Server" (
        echo ----------------------------------------
        echo 找到 Houdini 版本文件夹：%%~a

        :: 如果没有 config 文件夹，就创建一下
        if not exist "%%~a\houdini\config" (
            echo 未检测到子目录 %%~a\houdini\config，正在创建...
            mkdir "%%~a\houdini\config"
        )

        echo 正在复制 %file1% 到 %%~a\houdini\config
        copy /Y "%scriptDir%%file1%" "%%~a\houdini\config"
    ) else (
        echo 跳过文件夹：%%~a
    )
)

echo.
echo 复制操作完成，若有错漏请查看上方输出。
pause
