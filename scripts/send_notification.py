#!/usr/bin/env python3
"""
📧 Notification Script - AI Islamic Content Generator
Sends email with video and thumbnail links
"""

import os
import json
import sys
from datetime import datetime
from composio import ComposioToolSet, Action

def send_notification():
    """Send email notification with generated content"""

    try:
        toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        print(f"📧 [{datetime.utcnow().isoformat()}] Sending notification...")

        # Get data
        video_url = os.environ.get("VIDEO_URL", "")
        thumbnail_url = os.environ.get("THUMBNAIL_URL", "")
        script_json = os.environ.get("SCRIPT_DATA", "{}")
        test_mode = os.environ.get("TEST_MODE", "false").lower() == "true"

        script_data = json.loads(script_json) if script_json else {}
        script_text = script_data.get("script", "No script")

        # Create email
        subject = f"🎬 فيديو جديد - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"

        if test_mode:
            subject = f"[TEST] {subject}"

        body = f"""<html dir="rtl">
<body style="font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px;">
    <div style="max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

        <h1 style="color: #2c5f2d; text-align: center;">🎬 فيديو جديد جاهز!</h1>

        <div style="background: #f0f8ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2 style="color: #1a4d2e;">📝 النص:</h2>
            <p style="line-height: 1.8; white-space: pre-wrap;">{script_text}</p>
        </div>

        <div style="margin: 30px 0;">
            <h2 style="color: #1a4d2e;">🎥 الفيديو:</h2>
            <a href="{video_url}" style="display: inline-block; background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                📥 تحميل الفيديو
            </a>
            <p style="margin-top: 10px; font-size: 12px; color: #666;">
                <a href="{video_url}" target="_blank">{video_url}</a>
            </p>
        </div>

        <div style="margin: 30px 0;">
            <h2 style="color: #1a4d2e;">🖼️ الصورة المصغرة:</h2>
            <img src="{thumbnail_url}" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" alt="Thumbnail">
            <br>
            <a href="{thumbnail_url}" style="display: inline-block; background: #2196F3; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px;">
                📥 تحميل الصورة
            </a>
            <p style="margin-top: 10px; font-size: 12px; color: #666;">
                <a href="{thumbnail_url}" target="_blank">{thumbnail_url}</a>
            </p>
        </div>

        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #856404;">⏰ التوقيت:</h3>
            <p style="margin: 5px 0;">تم الإنشاء: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p style="margin: 5px 0;">الوضع: {"🧪 اختبار" if test_mode else "✅ إنتاج"}</p>
        </div>

        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee;">
            <p style="color: #666; font-size: 14px;">
                💚 اللهم انصر المظلومين في فلسطين وغزة وسوريا واليمن والروهينغا وكل مكان 💚
            </p>
            <p style="color: #999; font-size: 12px; margin-top: 10px;">
                تم الإنشاء بواسطة نظام AI الآلي
            </p>
        </div>

    </div>
</body>
</html>"""

        # Send email
        result = toolset.execute_action(
            action=Action.GMAIL_SEND_EMAIL,
            params={
                "recipient_email": "hamzawatfa25@gmail.com",
                "subject": subject,
                "body": body,
                "is_html": True
            }
        )

        print(f"✅ [{datetime.utcnow().isoformat()}] Notification sent successfully!")

        return True

    except Exception as e:
        print(f"❌ Error sending notification: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    send_notification()
