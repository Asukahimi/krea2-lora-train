# -*- coding: utf-8 -*-
"""下载 musubi-tuner 训练 Krea 2 LoRA 所需的权重（bf16 原版，不用 fp8 推理格式）。

- 训练用 RAW DiT（bf16）：krea2_raw_bf16.safetensors        24.48 GB
- 文本编码器（bf16）：   qwen3vl_4b_bf16.safetensors         8.27 GB
  （VAE 复用已下好的 qwen_image_vae.safetensors）

下载到 ComfyUI 的 models 目录，两边共用，省一份空间。
"""
import os
import time

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ComfyUI 的 models 目录：优先环境变量 MODELS，否则用默认路径
MODELS = os.environ.get("MODELS", r"E:\DownMain\ComfyUI\models")
MIRRORS = [
    "https://hf-mirror.com/{repo}/resolve/main/{path}",
    "https://huggingface.co/{repo}/resolve/main/{path}",
]
REPO = "Comfy-Org/Krea-2"
FILES = [
    ("diffusion_models/krea2_raw_bf16.safetensors",
     os.path.join(MODELS, "diffusion_models", "krea2_raw_bf16.safetensors")),
    ("text_encoders/qwen3vl_4b_bf16.safetensors",
     os.path.join(MODELS, "text_encoders", "qwen3vl_4b_bf16.safetensors")),
]


def human(n):
    return f"{n/1024**3:.2f}GB" if n > 1024**2 else f"{n/1024**2:.0f}MB"


def fetch(path, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    for attempt in range(1, 12):
        url = MIRRORS[(attempt - 1) % len(MIRRORS)].format(repo=REPO, path=path)
        try:
            done = os.path.getsize(tmp) if os.path.exists(tmp) else 0
            headers = {"Range": f"bytes={done}-"} if done else {}
            with requests.get(url, headers=headers, stream=True, timeout=(20, 300)) as r:
                if done and r.status_code != 206:
                    done = 0
                    if os.path.exists(tmp):
                        os.remove(tmp)
                r.raise_for_status()
                total = int(r.headers.get("Content-Length", 0)) + done
                t0 = last = time.time()
                with open(tmp, "ab" if done else "wb") as f:
                    for chunk in r.iter_content(8 * 1024 * 1024):
                        f.write(chunk)
                        done += len(chunk)
                        if time.time() - last > 20:
                            last = time.time()
                            print(f"    ... {os.path.basename(dest)} {human(done)}/{human(total)} "
                                  f"{done/1024**2/max(time.time()-t0,1):.1f}MB/s", flush=True)
            os.replace(tmp, dest)
            return True, f"{human(os.path.getsize(dest))}  {os.path.basename(dest)}"
        except Exception as e:
            print(f"    !! {os.path.basename(dest)} 第{attempt}次失败: {type(e).__name__}", flush=True)
            time.sleep(4 * attempt)
    return False, f"失败 {path}"


def main():
    need = [f for f in FILES if not (os.path.exists(f[1]) and os.path.getsize(f[1]) > 1024**3)]
    print(f"待下载 {len(need)} 个（训练用 bf16 权重）", flush=True)
    for p, d in need:
        print(f"   {p}", flush=True)
    ok = 0
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(fetch, p, d): p for p, d in need}
        for f in as_completed(futs):
            good, msg = f.result()
            ok += good
            print(("[完成] " if good else "[失败] ") + msg, flush=True)
    print(f"\n汇总: {ok}/{len(need)} 成功", flush=True)


if __name__ == "__main__":
    main()
