@echo off
REM Build the j2534_interface shim DLL with MSVC.
REM Targets 32-bit (x86) because the real j2534_interface.dll is PE32 x86.

setlocal
pushd "%~dp0\.."

call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86 >nul
if errorlevel 1 goto fail

if not exist build mkdir build

cl /nologo /LD /O2 /MT /D_USRDLL /D_WINDLL /Fobuild\ ^
   src\dllmain.c src\log.c src\wrappers.c src\forwarders.c ^
   /link /DEF:src\j2534_interface.def /OUT:build\j2534_interface.dll ^
         /IMPLIB:build\j2534_interface.lib
if errorlevel 1 goto fail

echo.
echo === build OK: build\j2534_interface.dll ===
dir /B build\j2534_interface.dll
popd
endlocal
exit /b 0

:fail
echo === build FAILED ===
popd
endlocal
exit /b 1
