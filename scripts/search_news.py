#!/usr/bin/env python3
"""
🔍 News Search Script - AI Islamic Content Generator
Searches for latest news about Palestine, Syria, Burma, Yemen and Islamic topics
"""

import os
import json
import sys
from datetime import datetime
from composio import ComposioToolSet, App, Action

def search_latest_news():
    """Search for latest news from multiple sources"""

    try:
        toolset = ComposioToolSet(api_key=os.environ.get("COMPOSIO_API_KEY"))

        print(f"🔍 [{datetime.utcnow().isoformat()}] Starting news search...")

        # Topics to search
        topics = [
            "Palestine Gaza latest news",
            "Syria humanitarian situation",
            "Rohingya Myanmar Burma crisis",
            "Yemen humanitarian crisis",
            "Islamic world current events",
            "Muslim oppression worldwide"
        ]

        all_news = []

        for topic in topics:
            try:
                print(f"📰 Searching: {topic}")

                # Use Composio Search for news
                result = toolset.execute_action(
                    action=Action.COMPOSIO_SEARCH_NEWS,
                    params={
                        "query": topic,
                        "when": "d",  # Last day
                        "hl": "ar",   # Arabic results
                        "gl": "world"
                    }
                )

                if result and isinstance(result, dict):
                    data = result.get("data", {})
                    if isinstance(data, dict) and "data" in data:
                        data = data["data"]

                    news_items = data.get("news_results", data.get("results", []))

                    for item in news_items[:2]:  # Top 2 per topic
                        all_news.append({
                            "topic": topic,
                            "title": item.get("title", ""),
                            "snippet": item.get("snippet", item.get("description", "")),
                            "link": item.get("link", ""),
                            "source": item.get("source", {}).get("name", "Unknown"),
                            "date": item.get("date", datetime.utcnow().isoformat())
                        })

            except Exception as e:
                print(f"⚠️ Error searching {topic}: {str(e)}")
                continue

        news_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_articles": len(all_news),
            "articles": all_news[:10]  # Top 10 overall
        }

        # Output for GitHub Actions
        with open(os.environ.get("GITHUB_OUTPUT", "/tmp/output.txt"), "a") as f:
            f.write(f"news_json={json.dumps(news_data)}\n")

        print(f"✅ [{datetime.utcnow().isoformat()}] Found {len(all_news)} news articles")
        print(json.dumps(news_data, ensure_ascii=False, indent=2))

        return news_data

    except Exception as e:
        print(f"❌ Error in news search: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    search_latest_news()
