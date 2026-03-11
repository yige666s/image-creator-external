---
name: image-creator-external
description: "Generate images from text or reference images using ShortArt AI. Use when users want to: create an image, draw something, generate a picture, visualize an idea, produce visual content from a text prompt, or generate an image based on a reference photo. Triggers on: 生成图片, 画一张, 帮我画, 制作图片, generate image, create image, draw, visualize, 图片生成, 文生图, 创作图像, image generation, make a picture, 以图生图, 修改图片, 编辑图片, Edit Image, image-to-image."
allowed-tools: Bash(python3 *)
metadata: {"openclaw": {"emoji": "🎨"}}
---

# Image Creator

Generate images using ShortArt backend API, supporting text-to-image and image-to-image.

## Authentication Setup (Required for First Use)

image-creator requires your ShortArt login credentials. Two methods are supported:

**Method 1 (Recommended): Google OAuth Auto-Authorization**
```bash
python3 scripts/auth.py login
```
Browser will open Google login page. After authorization, ShortArt login completes automatically. Token is securely stored in system Keychain, valid for ~58 days. Re-authorization will be prompted when expired.

> Uses PKCE flow, no client_secret needed, secure.

**Method 2: Manual Token Configuration**
After logging into ShortArt website, copy the token after `Authorization: Bearer` from browser developer tools, and add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "image-creator": {
        "env": { "SHORTART_API_TOKEN": "paste_your_token_here" }
      }
    }
  }
}
```

**Check Authentication Status:**
```bash
python3 scripts/auth.py status
```

## Parameter Quick Reference

| Parameter | Options | Default |
|------|------|------|
| `--model` | `seedream4.5` \| `nano-banana-pro` \| `nano-banana-2` | `nano-banana-pro` |
| `--count` | 1-4 | 1 |
| `--resolution` | `1k` \| `2k` \| `4k` (nano-banana-2 also supports `0.5k`) | `2k` |
| `--aspect-ratio` | `1:1` \| `16:9` \| `9:16` \| `1:1` |

## Important: Execution Method

To generate images, call `scripts/impl.py`, replace the placeholder parameters with user input or default value

```bash
python3 scripts/impl.py "<prompt>" \
  --model {ModelName}\
  --count {Count} \
  --resolution {Resolution} \
  --aspect-ratio {AspectRatio}
```

Image-to-image (with reference image):

```bash
# Use existing OSS path
python3 scripts/impl.py "<prompt>" --image "images/20260121/.../filename.jpg"

# Upload local image
python3 scripts/impl.py "<prompt>" --upload /path/to/local/image.jpg
```

## Return Result

```json
{
  "status": "success",
  "project_id": "{projectId}",
  "credit": "{credit}",
  "sub_credit": "{subCredit}",
  "consumed_credit": "{consumedCredit}",
}
```

## Workflow

1. **Check Authentication** — Run `python3 {baseDir}/scripts/auth.py status`; if unauthorized, run `python3 {baseDir}/scripts/auth.py login` first
2. **Understand Requirements** — Confirm subject, style, dimensions, quantity
3. **Optimize Prompt** — Refer to [references/prompt-guide.md](references/prompt-guide.md) to expand description
4. **Select Parameters** — Choose model / resolution / aspectRatio based on use case
5. **Execute Script** — Run `scripts/impl.py` to get `project_id`, if failed with returned error, retry a maximum of two times
6. **Display Results** — Inform user that task is submitted

Task is asynchronous. After submission, `project_id` is returned immediately, and images are generated in the background.

## Reference Files

- **API Parameters & Response Format** → [references/api.md](references/api.md)
- **Prompt Writing Templates** → [references/prompt-guide.md](references/prompt-guide.md)
