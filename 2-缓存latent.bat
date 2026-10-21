@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Step 2 / 4 : pre-cache image latents (Qwen-Image VAE)
echo ============================================================
"%PY%" "%ROOT%\musubi-tuner\krea2_cache_latents.py" ^
  --dataset_config "%ROOT%\config\dataset_character.toml" ^
  --vae "%VAE%"
echo.
pause
