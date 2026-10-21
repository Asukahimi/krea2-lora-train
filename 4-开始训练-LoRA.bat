@echo off
setlocal

rem ---- 路径与模型：只在 config.bat 里改一次 ----
call "%~dp0config.bat" || exit /b 1
cd /d "%ROOT%"
set "DATASET=%DATASET_CHAR%"

echo ============================================================
echo  Step 4 / 4 : train the LoRA  (RAW bf16 + fp8 + grad ckpt)
echo  - loss should drift downward; Ctrl+C stops early
echo  - a LoRA is saved to output\ after EVERY epoch (mychar-000001.safetensors ...)
echo ============================================================
set NAME=mychar
set EPOCHS=16
set DIM=32
set LR=1e-4
"%ACC%" launch --num_cpu_threads_per_process 1 --mixed_precision bf16 ^
  "%ROOT%\musubi-tuner\src\musubi_tuner\krea2_train_network.py" ^
  --dit "%RAW_BF16%" ^
  --vae "%VAE%" ^
  --dataset_config "%ROOT%\config\dataset_character.toml" ^
  --sdpa --mixed_precision bf16 --fp8_base --fp8_scaled --gradient_checkpointing ^
  --timestep_sampling shift --weighting_scheme none --discrete_flow_shift 2.5 ^
  --optimizer_type adamw8bit --learning_rate %LR% ^
  --max_data_loader_n_workers 2 --persistent_data_loader_workers ^
  --network_module networks.lora_krea2 --network_dim %DIM% --network_alpha %DIM% ^
  --max_train_epochs %EPOCHS% --save_every_n_epochs 1 --seed 42 ^
  --output_dir "%ROOT%\output" --output_name %NAME%
echo.
pause
