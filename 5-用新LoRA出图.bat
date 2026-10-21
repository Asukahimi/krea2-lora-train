@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Test the trained LoRA with musubi-tuner's own sampler
echo  Uses the RAW bf16 DiT (28 steps, CFG 5.5) - no extra download needed.
echo  EDIT the LORA= line if your file name is different.
echo  NOTE: fp8 checkpoints do NOT work here (training format is bf16 only).
echo ============================================================
set LORA=%ROOT%\output\mychar.safetensors
set OUT=%ROOT%\output\samples
set PROMPT=a girl standing on a rooftop at sunset, anime illustration, highly detailed
set NEG=blurry, low quality, watermark, text
"%PY%" "%ROOT%\musubi-tuner\krea2_generate_image.py" "%PROMPT%" ^
  --dit "%RAW_BF16%" ^
  --vae "%VAE%" ^
  --text_encoder "%QWEN_BF16%" ^
  --steps 28 --guidance_scale 5.5 ^
  --width 1024 --height 1024 --negative_prompt "%NEG%" ^
  --attn_mode torch --seed 0 --num-images 2 ^
  --save_path "%OUT%" ^
  --lora_weight "%LORA%" --lora_multiplier 1.0
echo.
echo Images saved to %OUT%
pause
