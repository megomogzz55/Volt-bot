"""
Volt Hybrid Daemon — Local Fast-Reactor & Cloud Sync
Runs silently in background while your PC is on:
1. Reacts to breaking news in seconds (instead of waiting for GitHub 90-minute cron).
2. Auto-syncs state with GitHub so Cloud and Local never conflict.
3. Sends live alerts with rendered cards to Telegram.
4. Pauses smoothly with zero CPU overhead.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from engines.mega_news_engine import MegaNewsEngine
from engines.telegram_notifier import send_telegram_alert
from publish.fb import post_photo


def sync_with_github():
    """Pulls latest state from GitHub Actions so we never duplicate posts."""
    try:
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=BASE_DIR, capture_output=True, timeout=20)
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Git sync warning: {e}")


def push_state_to_github():
    """Pushes local posted state to GitHub Actions so cloud doesn't repeat it."""
    try:
        subprocess.run(["git", "add", "data/mega_news_state.json"], cwd=BASE_DIR, capture_output=True, timeout=10)
        res = subprocess.run(["git", "commit", "-m", "chore: sync state from local daemon [skip ci]"], cwd=BASE_DIR, capture_output=True, timeout=10)
        if res.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, capture_output=True, timeout=20)
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Git push warning: {e}")


def check_and_publish_news(target_page="kora_volt", max_posts=1):
    """Checks for breaking news, renders cards with official templates, and publishes."""
    engine = MegaNewsEngine()
    
    if target_page == "fantasy_volt":
        articles = engine.fetch_fantasy_volt_news(limit=3)
    else:
        articles = engine.fetch_kora_volt_news(limit=3)
        
    if not articles:
        return 0
        
    posted = 0
    for art in articles:
        if posted >= max_posts:
            break
            
        caption = engine.format_post(art, page=target_page)
        card_path = engine.generate_branded_card(art, page=target_page)
        
        page_label = "كورة ڤولت ⚡" if target_page == "kora_volt" else "فانتازي ڤولت ⚡"
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚀 Publishing breaking news to {page_label}...")
        print(f"Title: {art.get('rewritten_title', art['title'])}")
        print(f"Card: {card_path}")
        
        try:
            res = post_photo(image_path=card_path, caption=caption, page_key=target_page)
            post_id = res.get("id") or res.get("post_id")
            print(f"✅ Live on Facebook! ID: {post_id}")
            engine.mark_posted(art["title"])
            posted += 1
            
            # Send Telegram alert with rendered card
            alert_msg = (
                f"<b>⚡ تم نشر بوست جديد على {page_label}</b>\n\n"
                f"<b>العنوان:</b> {art.get('rewritten_title', art['title'])}\n"
                f"<b>المعرف:</b> <code>{post_id}</code>\n"
                f"<b>المصدر:</b> {art.get('source_name', 'كورة ڤولت')}"
            )
            send_telegram_alert(alert_msg, image_path=card_path)
            
        except Exception as e:
            print(f"❌ Failed to publish: {e}")
            
    if posted > 0:
        push_state_to_github()
        
    return posted


def run_daemon(poll_interval_seconds=180):
    """
    Main background daemon loop:
    - Syncs with GitHub
    - Alternates checks between Kora Volt and Fantasy Volt
    - Sleeps between cycles
    """
    print("=" * 65)
    print("⚡ VOLT HYBRID DAEMON — FAST REACTOR & CLOUD SYNC ACTIVE")
    print(f"⏱️  Polling interval: every {poll_interval_seconds}s (~{poll_interval_seconds//60} min)")
    print("=" * 65)
    
    cycle = 0
    while True:
        try:
            cycle += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Cycle #{cycle}: Syncing with GitHub...")
            sync_with_github()
            
            # Alternate checks: Kora Volt first, then Fantasy Volt
            check_and_publish_news(target_page="kora_volt", max_posts=1)
            
            if cycle % 2 == 0:
                check_and_publish_news(target_page="fantasy_volt", max_posts=1)
                
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Cycle #{cycle} complete. Sleeping {poll_interval_seconds}s...")
            time.sleep(poll_interval_seconds)
            
        except KeyboardInterrupt:
            print("\n🛑 Daemon stopped by user.")
            break
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Unexpected error in daemon loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    interval = 180
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        interval = int(sys.argv[1])
    run_daemon(poll_interval_seconds=interval)
