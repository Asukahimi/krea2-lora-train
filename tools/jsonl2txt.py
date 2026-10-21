# -*- coding: utf-8 -*-
"""把 Qwen3-VL 打标输出的 jsonl 转成"每张图一个同名 .txt"，供 musubi-tuner 使用。

用法：
    python jsonl2txt.py <captions.jsonl>

jsonl 每行大致长这样（字段名兼容几种常见写法）：
    {"image_path": "01.png", "caption": "a girl with ..."}
    {"image": "...", "text": "..."}
"""
import io
import json
import os
import sys


def pick(d, *keys):
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return ""


def main():
    if len(sys.argv) < 2:
        print("用法: python jsonl2txt.py <captions.jsonl>")
        return 1
    src = sys.argv[1]
    if not os.path.exists(src):
        print("找不到文件:", src)
        return 1

    base = os.path.dirname(os.path.abspath(src))
    n = 0
    with io.open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            img = pick(d, "image_path", "image", "path", "file_name", "filename")
            cap = pick(d, "caption", "text", "prompt", "description")
            if not img or not cap:
                continue
            stem = os.path.splitext(os.path.basename(img))[0]
            out = os.path.join(base, stem + ".txt")
            with io.open(out, "w", encoding="utf-8") as g:
                g.write(cap.strip() + "\n")
            n += 1
    print(f"已写出 {n} 个 .txt 到 {base}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
