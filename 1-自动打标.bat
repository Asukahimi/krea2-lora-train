@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Step 1 / 4 : auto-caption dataset\character with Qwen3-VL
echo  (you can skip this and write the .txt files by hand)
echo ============================================================
"%PY%" "%ROOT%\musubi-tuner\caption_images_by_qwen_vl.py" ^
  --image_dir "%DATASET%" ^
  --model_path "%QWEN_BF16%" ^
  --output_file "%DATASET%\captions.jsonl" ^
  --max_new_tokens 256
if errorlevel 1 goto fail
echo.
echo Converting jsonl -^> per-image .txt ...
"%PY%" "%ROOT%\tools\jsonl2txt.py" "%DATASET%\captions.jsonl"
echo.
echo DONE. Please REVIEW every .txt before training (edit freely).
pause
exit /b 0

:fail
echo.
echo Failed. Check the error above.
echo Tip: write the .txt files manually instead - one .txt per image, same name.
pause
exit /b 1
