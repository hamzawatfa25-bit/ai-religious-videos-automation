#!/usr/bin/env python3
"""
📊 Execution Logger - AI Islamic Content Generator
Logs execution details for tracking and debugging
"""

import os
import json
import sys
from datetime import datetime

def log_execution():
    """Log execution details"""

    try:
        status = os.environ.get("STATUS", "unknown")
        news_json = os.environ.get("NEWS_DATA", "{}")
        script_json = os.environ.get("SCRIPT_DATA", "{}")

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": status,
            "success": status == "success",
            "news_count": json.loads(news_json).get("total_articles", 0) if news_json != "{}" else 0,
            "script_generated": bool(json.loads(script_json).get("script")) if script_json != "{}" else False
        }

        print(f"📊 [{datetime.utcnow().isoformat()}] Execution Log:")
        print(json.dumps(log_entry, indent=2))

        # Could write to a log file or database here

        return log_entry

    except Exception as e:
        print(f"⚠️ Error logging execution: {str(e)}", file=sys.stderr)
        # Don't exit with error for logging failures

if __name__ == "__main__":
    log_execution()
