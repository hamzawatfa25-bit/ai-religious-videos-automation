#!/usr/bin/env python3
"""
🖼️ Thumbnail Generation - AI Islamic Content Generator
Creates eye-catching clickbait-style thumbnails
"""

import os
import json
import sys
from datetime import datetime
from composio import ComposioToolSet, Action

def generate_thumbnail():
    """Generate thumbnail using Gemini"""

    try:
        toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        print(f"🖼️ [{datetime.utcnow().isoformat()}] Generating thumbnail...")

        # Get script data
        script_json = os.environ.get("SCRIPT_DATA", "{}")
        script_data = json.loads(script_json) if script_json else {}
        script_text = script_data.get("script", "")[:300]

        # Create thumbnail prompt
        thumbnail_prompt = f"""Create a professional, eye-catching YouTube thumbnail for Islamic content:

Style Requirements:
- 1280x720 pixels, 16:9 aspect ratio
- Bold, vibrant colors (gold, teal, deep blue, white)
- High contrast for visibility
- Professional Islamic aesthetic

Visual Elements:
- Large, readable Arabic text overlay (key phrase from script)
- Islamic geometric patterns or architecture
- Crescent moon, mosque silhouette, or Quran imagery
- Warm, spiritual glow effect
- No human faces

Layout:
- Text in top or center (large, bold Arabic font)
- Background: spiritual scene (mosque, nature, abstract Islamic art)
- Color scheme: gradient from teal to gold

Content focus:
{script_text}

Make it clickable and professional!"""

        # Generate thumbnail
        result = toolset.execute_action(
            action=Action.GEMINI_GENERATE_IMAGE,
            params={
                "prompt": thumbnail_prompt,
                "model": "gemini-2.5-flash-image-preview",
                "temperature": 0.8
            }
        )

        # Extract URL
        thumbnail_url = ""
        if result and isinstance(result, dict):
            data = result.get("data", {})
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            thumbnail_url = (
                data.get("public_url") or
                data.get("s3_url") or
                data.get("url") or
                data.get("image_url") or
                ""
            )

        if not thumbnail_url:
            raise Exception("Failed to generate thumbnail")

        # Output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/tmp/output.txt"), "a") as f:
            f.write(f"thumbnail_url={thumbnail_url}\n")

        print(f"✅ [{datetime.utcnow().isoformat()}] Thumbnail generated successfully!")
        print(f"🖼️ Thumbnail URL: {thumbnail_url}")

        return thumbnail_url

    except Exception as e:
        print(f"❌ Error generating thumbnail: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_thumbnail()
