@echo off
setlocal enabledelayedexpansion

:: ������ԱȨ�ޣ���������Ȩ
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

cd /d "%~dp0"
set "scriptDir=%~dp0"

:: �����û�� .json �ļ�
set "hasJson=0"
for %%f in ("%scriptDir%*.json") do (
    set hasJson=1
    goto :hasJson
)
:hasJson
if "%hasJson%"=="0" (
    echo δ��⵽�κ� .json �ļ����뽫 .json �ļ��뱾�ű�����ͬһ�ļ�����
    pause
    exit /b
)

echo ���ڲ��� C:\Program Files\Side Effects Software �µ� Houdini 20.5 �����ϰ汾...

for /D %%a in ("C:\Program Files\Side Effects Software\Houdini *") do (
    set "folderName=%%~nxa"
    set "fullPath=%%a"
    :: ��ȡ�汾��
    for /f "tokens=2" %%v in ("%%~nxa") do (
        set "version=%%v"
        for /f "tokens=1,2 delims=." %%x in ("!version!") do (
            set /a "ver_major=%%x"
            set /a "ver_minor=%%y"
            set /a "vercode=100*%%x+%%y"
            if !vercode! geq 2005 (
                echo ----------------------------------------
                echo �ҵ� Houdini �汾�ļ��У�!fullPath!

                set "targetDir=!fullPath!\houdini\config\NodeShapes"
                if not exist "!targetDir!" (
                    echo δ��⵽��Ŀ¼ !targetDir!�����ڴ���...
                    mkdir "!targetDir!"
                )
                echo ���ڸ��� .json �ļ��� !targetDir!
                copy /Y "%scriptDir%*.json" "!targetDir!"
            ) else (
                echo �����汾��!fullPath!
            )
        )
    )
)

echo.
echo ���Ʋ�����ɣ����д�©��鿴�Ϸ������
pause
