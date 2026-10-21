@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Copy the trained LoRA into ComfyUI (folder: loras\krea2\trained)
echo  so the "Krea2 anime" workflows can pick it in the LoRA slot.
echo ============================================================
set SRC=%ROOT%\output
set DST=%MODELS%\loras\krea2\trained
copy /Y "%SRC%\*.safetensors" "%DST%\"
echo.
echo Copied to %DST%
echo Next: open the workflow, choose Krea2 LoRA slot, pick trained\mychar
echo (restart the ComfyUI window if the new LoRA is not listed yet)
pause
