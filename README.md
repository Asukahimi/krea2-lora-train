# Krea 2 LoRA 训练工具链

把 musubi-tuner 这套命令行训练器包装成几个双击就能跑的步骤：

**准备数据 → 自动打标 → 缓存 → 训练 → 出图 → 装进 ComfyUI**

面向的是"不想碰命令行、但想自己训一个 LoRA"的场景。

---

## 环境要求

| 项 | 要求 |
|---|---|
| 系统 | Windows（脚本是 .bat） |
| 显卡 | 建议 24 GB 显存以上，32 GB 实测流畅（RAW bf16 + fp8 base + grad checkpoint） |
| Python | 3.10+，用来建独立 venv，不影响系统环境 |
| ComfyUI | 需要一个装好的 ComfyUI，模型与它共用，不额外占空间 |
| 磁盘 | 约 35 GB（RAW bf16 24.5 GB + 文本编码器 8.3 GB） |

## 目录结构

```
krea2-lora-train/
├── config.bat              ← 路径配置，只改这一个文件
├── 1-自动打标.bat            Qwen3-VL 给图片写描述
├── 2-缓存latent.bat
├── 3-缓存文本编码.bat
├── 4-开始训练-LoRA.bat      ★ 训练
├── 4b-训练画风.bat          画风 LoRA（数据集换成 dataset/style）
├── 5-用新LoRA出图.bat
├── 6-把LoRA装进ComfyUI.bat
├── config/                 数据集配置（toml）
├── docs/训练教程.md         完整教程：参数详解、显存、常见报错
├── setup/
│   ├── setup_env.py        建独立 venv（复用已有 torch，省 3 GB 下载）
│   └── download_models.py  下 bf16 权重（双镜像 + 并发）
└── tools/jsonl2txt.py
```

`dataset/`、`output/` 由脚本自动创建，不在仓库里。

## 怎么用

### 0. 准备（只做一次）

```powershell
# 1) 训练器源码放到本目录
git clone https://github.com/kohya-ss/musubi-tuner

# 2) 下训练用的 bf16 权重（下到 ComfyUI 的 models 目录）
python setup\download_models.py

# 3) 建独立训练环境
python setup\setup_env.py
```

`setup_env.py` 会用 `BASE_PYTHON`（默认当前 Python）建一个 `.venv`，并
`--system-site-packages` 复用现成的 torch，避免重复下载 3 GB。

### 1. 改路径

打开 `config.bat`，确认 `MODELS` 指向你的 ComfyUI `models` 目录。其余路径由 `%~dp0` 自动推算，整个工程可以搬到任意位置。

### 2. 训练

图片放进 `dataset\character\`，然后依次双击：

1. `1-自动打标.bat`（自动生成描述，**建议人工过一遍**）
2. `2-缓存latent.bat`
3. `3-缓存文本编码.bat`
4. `4-开始训练-LoRA.bat`

产物在 `output\`，每个 epoch 存一份（`mychar-000001.safetensors` …）。

### 3. 出图与部署

- `5-用新LoRA出图.bat`：直接用新 LoRA 生成一张看效果
- `6-把LoRA装进ComfyUI.bat`：复制到 ComfyUI 的 `models\loras\krea2\trained\`

## 训练参数

在 `4-开始训练-LoRA.bat` 顶部改这几行：

| 变量 | 默认 | 说明 |
|---|---|---|
| `NAME` | `mychar` | 输出文件名 |
| `EPOCHS` | 16 | 轮数，角色 LoRA 一般 10~20 |
| `DIM` | 32 | LoRA 维度 |
| `LR` | 1e-4 | 学习率；画风 LoRA 用 5e-5 |

## 两个容易踩的点

**1. 训练只能用 bf16 权重**

ComfyUI 推理用的 `*_fp8_scaled.safetensors` 带 `weight_scale` / `comfy_quant` 量化元数据，直接拿来训练会报：

```
RuntimeError: Error(s) in loading state_dict ...
Unexpected key(s): "blocks.0.attn.wq.weight_scale"
```

DiT 和文本编码器都一样。脚本里已全部指向 bf16 版本。

**2. 模型和 ComfyUI 共用一份**

bf16 和 fp8 放在同一个 `models` 目录，ComfyUI 那边照旧用 fp8（省显存），训练这边用 bf16，互不影响。

## 详细文档

参数含义、显存不够怎么办、训练预览图、常见报错：[docs/训练教程.md](docs/训练教程.md)

## 版权与声明

- 本仓库只含脚本与文档，**不含模型权重、训练数据、训练产物**
- 依赖 [musubi-tuner](https://github.com/kohya-ss/musubi-tuner)（kohya-ss），遵守其原始许可证
- Krea 2 模型权重遵守其发布方许可
