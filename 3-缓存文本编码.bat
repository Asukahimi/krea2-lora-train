@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Step 3 / 4 : pre-cache Qwen3-VL text encoder outputs
echo ============================================================
"%PY%" "%ROOT%\musubi-tuner\krea2_cache_text_encoder_outputs.py" ^
  --dataset_config "%ROOT%\config\dataset_character.toml" ^
  --text_encoder "%QWEN_BF16%" ^
  --batch_size 1
echo.
pause
