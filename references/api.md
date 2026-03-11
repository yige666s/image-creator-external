# ShortArt Image API Reference

## Table of Contents
1. [API Overview](#api-overview)
2. [Create Project](#create-project-post-apiprojectcreate)
3. [Query Project](#query-project-get-apiprojectget)
4. [Upload Image](#upload-image-post-apiosupload)
5. [Model and Parameter Matrix](#model-and-parameter-matrix)
6. [Project Status Codes](#project-status-codes)
7. [Response Format](#response-format)

---

## API Overview

| API | Method | Path |
|------|------|------|
| Create image generation task | POST | `/api/project/create` |
| Query project status/result | GET | `/api/project/get` |
| Upload local image to OSS | POST | `/api/oss/upload` |

**Base URL:** `https://shortart-api.wenuts.top`  
**Auth:** `Authorization: Bearer <token>`

---

## Create Project `POST /api/project/create`

### Request Body

```json
{
  "model": "nano-banana-pro",
  "prompt": "...",
  "count": 1,
  "images": ["images/20260121/uid/filename.jpg"],
  "resolution": "2K",
  "aspectRatio": "16:9"
}
```

| Field | Type | Required | Description |
|------|------|------|------|
| `model` | string | ✅ | See model list |
| `prompt` | string | ✅ | Image description, supports Chinese and English |
| `count` | int | ✅ | Generation count 1-4 |
| `resolution` | string | ✅ | See resolution list, case insensitive |
| `aspectRatio` | string | ✅ | Aspect ratio |
| `images` | list | ❌ | OSS relative path, if provided, image-to-image mode |

### Response

```json
{
  "code": 0,
  "data": {
    "projectId": "67ce3b2a1234abcd5678ef90",
    "credit": 85,
    "subCredit": 0,
    "consumedCredit": 15
  }
}
```

---

## Query Project `GET /api/project/get`

**Parameter:** `?projectID=<projectId>`

### Response

```json
{
  "code": 0,
  "data": {
    "project": {
      "id": "67ce3b2a...",
      "status": 2,
      "domain": "https://cdn.wenuts.top/",
      "result": {
        "images": [
          {"id": "...", "path": "projects/...", "width": 3840, "height": 2160, "riskLevel": 0}
        ]
      },
      "error": ""
    }
  }
}
```

Complete image URL = `domain` + `path`

---

## Upload Image `POST /api/oss/upload`

**Content-Type:** `multipart/form-data`

| Field | Type | Description |
|------|------|------|
| `file` | file | Image file |
| `type` | string | Fixed value `"image"` |

### Response

```json
{
  "code": 0,
  "data": {
    "path": "user_media/<uid>/<name>.jpg",
    "domain": "https://cdn.wenuts.top/",
    "width": 1920,
    "height": 1080
  }
}
```

The returned `path` can be directly passed to the `images` field when creating a project.

---

## Model and Parameter Matrix

| Model | Supported Resolutions | Price (Credits/Image) | Features |
|------|-----------|----------------|------|
| `seedream4.5` | 1k, 2k, 4k | 15 | Lowest average price, supports image-to-image, high quality |
| `nano-banana-pro` | 1k, 2k, 4k | 50 / 50 / 100 | High quality, suitable for commercial scenarios |
| `nano-banana-2` | 0.5k, 1k, 2k, 4k | 20 / 30 / 40 / 50 | Fast speed, supports low resolution preview |

**Resolution Description:**

| Value | Actual Pixels (Reference) |
|----|----------------|
| `0.5k` | ~512×512 |
| `1k` | ~1024×1024 |
| `2k` | ~2048×2048 |
| `4k` | ~3840×2160 |

**Aspect Ratio Options:** `1:1` `16:9` `9:16` 

> ⚠️ Generating 4 images or using 4k resolution requires a subscription plan

---

## Project Status Codes

| Value | Status | Description |
|----|------|------|
| `0` | pending | Waiting for processing |
| `1` | processing | Generating |
| `2` | completed | Completed, images ready |
| `3` | failed | Failed, check `error` field |

---

## Response Format

All APIs use a unified format:

```json
{"code": 0, "message": "", "data": {...}}
```

| code | Meaning |
|------|------|
| `0` | Success |
| Non-0 | Failed, read `message` field for reason |
