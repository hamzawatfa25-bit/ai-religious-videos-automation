#!/usr/bin/env python3
"""
🎬 Video Generation - AI Islamic Content Generator
Uses Google Veo 3 to generate high-quality 30-second videos
"""

import os
import json
import sys
import time
from datetime import datetime
from composio import ComposioToolSet, Action

def generate_video():
    """Generate video using Veo 3"""

    try:
        toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        print(f"🎬 [{datetime.utcnow().isoformat()}] Starting video generation with Veo 3...")

        # Get script data
        script_json = os.environ.get("SCRIPT_DATA", "{}")
        script_data = json.loads(script_json) if script_json else {}
        script_text = script_data.get("script", "")

        if not script_text:
            raise Exception("No script provided")

        # Create Veo 3 prompt
        veo_prompt = f"""Create a captivating 30-second Islamic content video:

Visual Style:
- Professional, modern Islamic aesthetics
- Warm, spiritual atmosphere with golden/blue tones
- Subtle Arabic calligraphy or geometric patterns
- Smooth transitions and cinematic feel

Content Focus:
{script_text[:200]}

Requirements:
- Duration: exactly 30 seconds
- Family-friendly content
- High quality, engaging visuals
- No faces or people (Islamic content style)
- Focus on nature, architecture, abstract visuals
- Spiritual and peaceful mood"""

        # Generate video with Veo 3
        print("🎥 Calling Veo 3...")
        result = toolset.execute_action(
            action=Action.GEMINI_GENERATE_VIDEOS,
            params={
                "prompt": veo_prompt,
                "model": "veo-3.0-fast-generate-preview",
                "person_generation": "dont_allow"
            }
        )

        # Extract operation name
        operation_name = None
        if result and isinstance(result, dict):
            data = result.get("data", {})
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            operation_name = data.get("name", data.get("operation_name", ""))

        if not operation_name:
            raise Exception("Failed to start video generation")

        print(f"⏳ Video generation started: {operation_name}")
        print("⏳ Waiting for video to complete (this may take 2-5 minutes)...")

        # Wait for video completion
        video_result = toolset.execute_action(
            action=Action.GEMINI_WAIT_FOR_VIDEO,
            params={"operation_name": operation_name}
        )

        # Extract video URL
        video_url = ""
        if video_result and isinstance(video_result, dict):
            data = video_result.get("data", {})
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            # Try multiple possible paths for the URL
            video_url = (
                data.get("public_url") or 
                data.get("s3_url") or 
                data.get("url") or
                data.get("download_url") or
                ""
            )

        if not video_url:
            raise Exception("Failed to get video URL")

        # Output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/tmp/output.txt"), "a") as f:
            f.write(f"video_url={video_url}\n")

        print(f"✅ [{datetime.utcnow().isoformat()}] Video generated successfully!")
        print(f"🎬 Video URL: {video_url}")

        return video_url

    except Exception as e:
        print(f"❌ Error generating video: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_video()
