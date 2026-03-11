# Image Creator External

Generate images from text or reference images using ShortArt AI.

## Installation

```bash
npx skills add yige666s/image-creator-external
ln -s ~/.agents/skills/image-creator-external ~/.openclaw/skills/image-creator-external  # install to openclaw
ln -s ~/.agents/skills/image-creator-external ~/.claude/skills/image-creator-external # install to claude code
```

## Features

- Text-to-image generation
- Image-to-image generation with reference photos
- Multiple AI models (seedream4.5, nano-banana-pro, nano-banana-2)

## Quick Start

---
> 🎉 **FREE TO START!** Generate images at [https://shortart.ai](https://shortart.ai)
---

### Generate Image With Chat

If you first use this, it will guide to complete authentication with your Google Account.

If you do not have an account, visit [https://shortart.ai](https://shortart.ai) to register an account with Google.

You can chat with your assistant like `help me generate image : Cute little kitty smiling. In the style of a Pixar 3D animation`, then wait a moment you can visit [https://shortart.ai/projects](https://shortart.ai/projects) to check it.

Meanwhile, you can generate or edit an image, only paste it into the dialog box so that let it knows the image path.

## Requirements

- Python 3.7+
- Lib: keyring, requests
- ShortArt account

## License

MIT
