@echo off
rem ============================================================
rem  Krea 2 LoRA 训练 - 路径配置
rem
rem  只需要改这个文件。
rem  ROOT 自动取本文件所在目录，所以整个工程可以直接搬到
rem  别的盘、别的路径，下面的脚本都不用改。
rem
rem  MODELS 指向 ComfyUI 的 models 目录：模型和 ComfyUI 共用，
rem  不额外占一份空间。ComfyUI 装在别处就改这一行，
rem  或者先设好同名环境变量再运行脚本。
rem ============================================================

rem ---- 1. 工程根目录（自动，一般不用改）----
for %%I in ("%~dp0.") do set "ROOT=%%~fI"

rem ---- 2. ComfyUI 的 models 目录（模型共用）----
if not defined MODELS set "MODELS=E:\DownMain\ComfyUI\models"

rem ---- 3. 独立训练环境（由 setup\setup_env.py 创建）----
set "PY=%ROOT%\.venv\Scripts\python.exe"
set "ACC=%ROOT%\.venv\Scripts\accelerate.exe"

rem ---- 4. 训练器源码（musubi-tuner，需自行 clone 到 ROOT 下）----
set "MUSUBI=%ROOT%\musubi-tuner"

rem ---- 5. 模型文件 ----
set "VAE=%MODELS%\vae\qwen_image_vae.safetensors"
set "QWEN_BF16=%MODELS%\text_encoders\qwen3vl_4b_bf16.safetensors"
set "QWEN_FP8=%MODELS%\text_encoders\qwen3vl_4b_fp8_scaled.safetensors"
set "RAW_BF16=%MODELS%\diffusion_models\krea2_raw_bf16.safetensors"
set "RAW_FP8=%MODELS%\diffusion_models\krea2_raw_fp8_scaled.safetensors"
set "TURBO=%MODELS%\diffusion_models\krea2_turbo_fp8_scaled.safetensors"

rem ---- 6. 数据与输出目录 ----
set "DATASET_CHAR=%ROOT%\dataset\character"
set "DATASET_STYLE=%ROOT%\dataset\style"
set "OUTDIR=%ROOT%\output"

if not exist "%DATASET_CHAR%" mkdir "%DATASET_CHAR%"
if not exist "%DATASET_STYLE%" mkdir "%DATASET_STYLE%"
if not exist "%OUTDIR%" mkdir "%OUTDIR%"
