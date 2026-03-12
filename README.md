<div align="center">

# 🎨 Image Creator External

**Generate stunning images from text or reference images using ShortArt AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

> 🎉 **FREE TO START! Generate images you want with just one sentence in a chat.**

[Get Started](#-installation) • [Features](#-features) • [Quick Start](#-quick-start)

</div>

---

## 📦 Installation

### Step 1: Install the skill

```bash
npx skills add yige666s/image-creator-external
```

This will install the skill to `~/.agents/skills/image-creator-external`.

### Step 2: Create symlink (Optional)

If you need to link the skill to a specific agent directory:

```bash
curl -fsSL https://raw.githubusercontent.com/yige666s/image-creator-external/main/install.sh | bash
```

Or manually:

```bash
# For Claude Code
ln -s ~/.agents/skills/image-creator-external ~/.claude/skills/image-creator-external

# For OpenClaw
ln -s ~/.agents/skills/image-creator-external ~/.openclaw/skills/image-creator-external
```

## ✨ Features

- 🖼️ **Text-to-Image** - Generate images from text descriptions
- 🎭 **Image-to-Image** - Transform images using reference photos
- 🤖 **Multiple AI Models** - Choose from various AI models
- 📊 **Flexible Options** - Batch generation, multiple resolutions, and aspect ratios

## 🚀 Quick Start

### 1. Get Your API Key

1. Visit [ShortArt.ai](https://shortart.ai) to register an account with Google
2. Get your API Key from [shortart.ai/key](https://shortart.ai/key)
3. Configure it in `~/.openclaw/openclaw.json` or export to `~/.zshrc`

### 2. Generate Images

Simply chat with your AI assistant:

```
Help me generate an image: Costume design drawing, a girl, on a white background,
wearing a white T-shirt, brown wide-leg pants, white shoes, in the picture
disassembled model's costume. Generate two images, 4k, 16:9
```

Then visit [shortart.ai/projects](https://shortart.ai/projects) to view your generated images.

### 3. Available Options

| Option | Values | Note |
|--------|--------|------|
| **Model** | `seedream4.5`, `nano-banana-pro`, `nano-banana-2` | Different quality/speed tradeoffs |
| **Count** | `1`, `2`, `3`, `4` | 4 images requires subscription |
| **Resolution** | `0.5k`, `1k`, `2k`, `4k` | 4k requires subscription, 0.5k only for nano-banana-2 |
| **Aspect Ratio** | `1:1`, `16:9`, `9:16` | Standard aspect ratios |

### 4. Image-to-Image Generation

Paste an image into the dialog box to use it as a reference for generation or editing.

---

## 📋 Requirements

- Python 3.7+
- `requests` library
- ShortArt account

## 📄 License

MIT License - see [LICENSE](LICENSE) for details
