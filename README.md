# 肥嘟嘟 · 美团袋鼠 Codex 桌宠

参考“你的胆子真是肥嘟嘟的”表情图制作的非官方 Codex 桌宠。

![肥嘟嘟预览](preview.webp)

## 安装

下载本仓库，或运行：

```sh
git clone https://github.com/inoader/codex-feidudu-pet.git
cd codex-feidudu-pet
python3 install.py
```

安装完成后，重新打开 Codex，在桌宠选择器中选择 **肥嘟嘟 · 美团袋鼠**。
安装脚本仅复制桌宠资源，不修改应用全局配置；如果目录已经存在，使用 `--replace` 明确允许覆盖。

也可以手动将 `pet.json` 和 `spritesheet.png` 放入 `$CODEX_HOME/pets/meituan-feidudu/`。未设置 `CODEX_HOME` 时，默认使用 `~/.codex`。

## 文件与规格

- `spritesheet.png`：1536 × 1872 像素，RGBA 透明背景。
- `pet.json`：`spriteVersionNumber: 1`，每帧 192 × 208 像素，8 列 9 行。
- `preview.webp`：待机动画预览。
- `source/`：AI 生成原图与生成提示词。
- `build_pet.py`：清理背景、提取动画帧和组合图集的脚本。

这是当前使用的 v1 版本，尚未包含 v2 的 16 向视线动作。部分动作通过重采样补齐帧数；检查动作暂时复用等待动作，工作状态采用原地跑动。并非逐帧复刻原视频。

## 重新构建

安装桌宠本身不需要以下依赖；仅修改或重建图集时需要：

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 build_pet.py
```

图像由内置 imagegen 根据参考生成，再使用 Pillow 和 NumPy 整理。构建脚本针对仓库内的原始图集布局，不是通用图集转换工具。

## 参考

- [肥嘟嘟原头像与全身形象](https://www.sina.cn/news/detail/5334329758319460.html)
- [肥嘟嘟表情图汇总](https://www.digitaling.com/articles/1573067.html)

美团及其袋鼠形象相关权利归原权利人所有。本项目为非官方衍生作品，与美团或 OpenAI 无隶属关系。
