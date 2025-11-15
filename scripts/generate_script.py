#!/usr/bin/env python3
"""
✍️ Script Generation - AI Islamic Content Generator
Uses AI to create engaging, viral Islamic content scripts
"""

import os
import json
import sys
from datetime import datetime
from composio import ComposioToolSet, Action

def generate_video_script():
    """Generate engaging video script based on news"""

    try:
        toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        print(f"🧠 [{datetime.utcnow().isoformat()}] Generating script...")

        # Get news data
        news_json = os.environ.get("NEWS_DATA", "{}")
        news_data = json.loads(news_json) if news_json else {}

        articles = news_data.get("articles", [])

        # Create prompt for script generation
        prompt = f"""أنت كاتب محتوى إسلامي إبداعي متخصص في إنتاج محتوى فيديو قصير (30 ثانية) يجذب الملايين.

آخر الأخبار:
{json.dumps(articles[:3], ensure_ascii=False, indent=2)}

مهمتك: اكتب نص فيديو إدماني (30 ثانية) بالأسلوب التالي:

**Hook قوي (3 ثواني):**
- سؤال صادم أو حقيقة مثيرة تتعلق بالأخبار
- يوقف المشاهد فوراً

**محتوى قيم (22 ثانية):**
- معلومة دينية أو قصة قصيرة مرتبطة بالأحداث
- حقائق مذهلة من القرآن والسنة
- ربط الدين بالواقع المعاصر

**نهاية قوية (5 ثواني):**
- دعاء للمظلومين في فلسطين وغزة وسوريا واليمن والروهينغا
- دعوة للاشتراك
- سؤال يجعل المشاهد يفكر

متطلبات:
1. النص بالعربية الفصحى البسيطة
2. مدة 30 ثانية بالضبط عند القراءة
3. أسلوب إدماني وسريع
4. محتوى 100% صحيح من القرآن والسنة
5. ذكر المظلومين في كل فيديو
6. بدون أي علامات أو رموز خاصة، فقط النص

اكتب النص الآن:"""

        # Call Gemini via Composio
        result = toolset.execute_action(
            action=Action.GEMINI_GENERATE_CONTENT,
            params={
                "prompt": prompt,
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.9,
                "max_output_tokens": 500
            }
        )

        # Extract script
        script_text = ""
        if result and isinstance(result, dict):
            data = result.get("data", {})
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            script_text = data.get("text", data.get("content", ""))

        if not script_text:
            raise Exception("Failed to generate script")

        # Create structured output
        script_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "script": script_text,
            "duration_seconds": 30,
            "news_context": articles[:2] if articles else []
        }

        # Output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/tmp/output.txt"), "a") as f:
            f.write(f"script_json={json.dumps(script_data, ensure_ascii=False)}\n")

        print(f"✅ [{datetime.utcnow().isoformat()}] Script generated successfully")
        print("\n📝 SCRIPT:\n")
        print(script_text)

        return script_data

    except Exception as e:
        print(f"❌ Error generating script: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_video_script()
