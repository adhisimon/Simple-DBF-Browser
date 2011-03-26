set python=C:\Python27\python.exe
set iscc="C:\Program Files\Inno Setup 5\ISCC.exe"

%python% setup.py build
%iscc% simpledbfbrowser.iss

pause
