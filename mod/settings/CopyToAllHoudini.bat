@echo off
:: ��û�й���ԱȨ�ޣ��Զ��Թ���Ա������������ű�
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

:: �л�����Ŀ¼���ű�����Ŀ¼
cd /d "%~dp0"
set "scriptDir=%~dp0"

:: ��Ҫ���Ƶ��ļ�
set "file1=3DSceneColors.bw"

:: ����ļ������ھ��˳�
if not exist "%scriptDir%%file1%" (
    echo δ�ҵ� %file1% �ļ����뽫 %file1% �뱾�ű�����ͬһ�ļ�����
    pause
    exit /b
)

echo ���ڲ��Ұ��b�� "C:\Program Files\Side Effects Software" �µ� Houdini �汾...

:: ���� "C:\Program Files\Side Effects Software" ���� "Houdini " ��ͷƥ����ļ���
for /D %%a in ("C:\Program Files\Side Effects Software\Houdini *") do (
    if /I not "%%~nxa"=="Houdini Server" (
        echo ----------------------------------------
        echo �ҵ� Houdini �汾�ļ��У�%%~a

        :: ���û�� config �ļ��У��ʹ���һ��
        if not exist "%%~a\houdini\config" (
            echo δ��⵽��Ŀ¼ %%~a\houdini\config�����ڴ���...
            mkdir "%%~a\houdini\config"
        )

        echo ���ڸ��� %file1% �� %%~a\houdini\config
        copy /Y "%scriptDir%%file1%" "%%~a\houdini\config"
    ) else (
        echo �����ļ��У�%%~a
    )
)

echo.
echo ���Ʋ�����ɣ����д�©��鿴�Ϸ������
pause
