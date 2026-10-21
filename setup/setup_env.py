# -*- coding: utf-8 -*-
"""搭建 Krea 2 LoRA 训练环境：
用秋叶包的 python 建独立 venv（--system-site-packages 复用 torch 2.7+cu128，省 3GB 下载），
再把 musubi-tuner 需要的依赖装进这个 venv（不会污染秋叶包/ComfyUI）。
"""
import os
import subprocess
import sys

# 用哪个 Python 来建独立 venv：优先环境变量 BASE_PYTHON，
# 否则用默认的秋叶包路径（按自己机器的情况改，或者先设 BASE_PYTHON）
PY = os.environ.get("BASE_PYTHON", sys.executable)
# 工程根目录 = 本文件所在目录的上一级
TRAIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV = os.path.join(TRAIN, ".venv")
VPY = os.path.join(VENV, "Scripts", "python.exe")
SRC = os.path.join(TRAIN, "musubi-tuner")
MIRROR = "https://mirrors.aliyun.com/pypi/simple/"
MIRROR_FALLBACK = ["https://mirrors.cloud.tencent.com/pypi/simple/",
                   "https://mirrors.ustc.edu.cn/pypi/simple/",
                   "https://pypi.org/simple/"]


def sh(args, **kw):
    print(">>", " ".join(str(a) for a in args), flush=True)
    return subprocess.run(args, text=True, **kw)


def pip(args, cwd=None, env=None):
    """pip 装包，主源失败自动换源。"""
    env = env or dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK="1")
    for i, src in enumerate([MIRROR] + MIRROR_FALLBACK):
        r = sh([VPY, "-m", "pip", "install"] + args + ["-i", src, "--timeout", "60"], cwd=cwd, env=env)
        if r.returncode == 0:
            return True
        print(f"!! 源 {src} 失败，换下一个", flush=True)
    return False


def main():
    os.makedirs(TRAIN, exist_ok=True)
    # 1) 建 venv（复用系统 torch）
    if not os.path.exists(VPY):
        sh([PY, "-m", "venv", "--system-site-packages", VENV], check=True)
        print("venv 已建：", VENV, flush=True)
    else:
        print("venv 已存在", flush=True)

    # 2) 升级 pip / wheel
    pip(["-q", "--upgrade", "pip", "wheel"])

    # 3) 装 musubi-tuner 本体 + 依赖（pyproject 里没有 torch，所以不会重下 torch）
    if not pip(["-e", "."], cwd=SRC):
        print("!! pip install -e . 失败，改为逐个装依赖", flush=True)
        pkgs = ["accelerate==1.6.0", "av", "bitsandbytes", "diffusers==0.32.1", "einops==0.7.0",
                "huggingface-hub==0.34.3", "opencv-python", "pillow>=11.3.0", "safetensors==0.4.5",
                "toml==0.10.2", "tqdm==4.67.1", "transformers==4.57.6", "voluptuous==0.15.2",
                "ftfy", "easydict", "sentencepiece"]
        pip(pkgs)

    # 4) 自检
    sh([VPY, "-c", (
        "import sys, torch, transformers, diffusers, accelerate, safetensors, einops, voluptuous, toml, cv2, PIL, numpy\n"
        "print('python     ', sys.version.split()[0])\n"
        "print('torch      ', torch.__version__, 'cuda', torch.version.cuda, 'avail', torch.cuda.is_available())\n"
        "print('transformers', transformers.__version__)\n"
        "print('diffusers  ', diffusers.__version__)\n"
        "print('accelerate ', accelerate.__version__)\n"
        "print('safetensors', safetensors.__version__)\n"
        "print('PIL        ', PIL.__version__)\n"
        "print('numpy      ', numpy.__version__)\n"
        "try:\n"
        "    import bitsandbytes as bnb; print('bitsandbytes', bnb.__version__)\n"
        "except Exception as e:\n"
        "    print('bitsandbytes 缺失 ->', type(e).__name__)\n"
        "try:\n"
        "    import musubi_tuner; print('musubi_tuner OK')\n"
        "except Exception as e:\n"
        "    print('musubi_tuner 导入失败 ->', type(e).__name__, e)\n"
        "try:\n"
        "    import triton; print('triton', triton.__version__)\n"
        "except Exception:\n"
        "    print('triton 未装（仅 ConvRot int8 需要，可忽略）')\n"
    )])


if __name__ == "__main__":
    main()
