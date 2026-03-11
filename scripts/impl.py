"""
Image Creator Skill - Entry Point
"""
import json
import logging
import sys
import os
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))
from client import ShortArtClient


def _get_token(config: dict) -> str:
    token = (
        config.get("shortart_api_token")
        or os.environ.get("SHORTART_API_TOKEN", "")
    )
    if token:
        return token

    try:
        from auth import shortart_auth
        return shortart_auth.get_token() 
    except ImportError:
        pass

    return ""


def execute(
    prompt: str = "",
    model: str = "",
    count: int = 1,
    images: list = None,
    resolution: str = "2k",
    aspect_ratio: str = "1:1",
    upload: str = None,
    config: Dict[str, Any] = None,
    **kwargs,
) -> str:
    if config is None:
        config = {}

    logger.info(f"[image-creator] prompt={prompt[:60]!r}, model={model}, count={count}")

    token = _get_token(config)

    if not token:
        return json.dumps({
            "status": "error",
            "error": (
                "ShortArt session token not found.\n"
                "Configure it via one of the following:\n"
                "  Option 1 (recommended): run python3 scripts/auth.py login to complete Google OAuth\n"
                "  Option 2: set skills.entries.image-creator.env.SHORTART_API_TOKEN in ~/.openclaw/openclaw.json"
            )
        }, ensure_ascii=False)

    client = ShortArtClient(
        token=token,
        base_url="https://shortart-api.wenuts.top",
    )

    oss_images = list(images or [])

    # Upload local image
    if upload:
        up = client.upload_image(upload)
        if up["status"] != "success":
            return json.dumps(up, ensure_ascii=False)
        oss_images.append(up["path"])
        logger.info(f"[image-creator] uploaded: {up['path']}")

    result = client.create_project(
        prompt=prompt,
        model=model,
        count=count,
        images=oss_images or None,
        resolution=resolution,
        aspect_ratio=aspect_ratio,
    )

    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images via ShortArt")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--model", default="nano-banana-pro",
                        choices=["seedream4.5", "nano-banana-pro", "nano-banana-2"])
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--resolution", default="2k",
                        choices=["0.5k", "1k", "2k", "4k"])
    parser.add_argument("--aspect-ratio", default="1:1", 
                        choices=["1:1", "16:9", "9:16"])
    parser.add_argument("--image", action="append", dest="images",
                        help="OSS relative path (repeat for multiple)")
    parser.add_argument("--upload", help="Local image file to upload first")
    args = parser.parse_args()

    output = execute(
        prompt=args.prompt,
        model=args.model,
        count=args.count,
        images=args.images,
        resolution=args.resolution,
        aspect_ratio=args.aspect_ratio,
        upload=args.upload,
    )
    print(output)
