"""
Fantasy Volt & Kora Volt Automation Bot
Main CLI Entry Point
"""
import sys
import os
import argparse
from datetime import datetime

from publish.fb import post_photo, post_text, verify_token
from render.card_engine import (
    render_yellow_card,
    render_goal_assist,
    render_bonus,
    render_fulltime,
    render_price_changes,
    render_today_fixtures
)
from engines.fpl_engine import FPLEngine
from engines.live_score_engine import LiveScoreEngine
from engines.news_engine import NewsEngine
from engines.photo_news_engine import PhotoNewsEngine, download_image, fetch_entity_photo
from engines.fantasy_content_engine import FantasyContentEngine
from engines.vector_goal_card import render_vector_goal_card

def cmd_status():
    print("=" * 60)
    print("⚡ VOLT AUTOMATION SYSTEM STATUS")
    print("=" * 60)
    
    print("\n[1] FACEBOOK PAGES:")
    try:
        fv = verify_token("fantasy_volt")
        print(f"  ✅ Fantasy Volt: Connected ({fv.get('name')})")
    except Exception as e:
        print(f"  ❌ Fantasy Volt: Error -> {e}")
        
    try:
        kv = verify_token("kora_volt")
        print(f"  ✅ Kora Volt: Connected ({kv.get('name')})")
    except Exception as e:
        print(f"  ❌ Kora Volt: Error -> {e}")
        
    print("\n[2] ENGINES & APIS:")
    try:
        fpl = FPLEngine()
        gw = fpl.get_current_gameweek()
        dl = fpl.get_deadline_status()
        print(f"  ✅ FPL API: Active | {gw.get('name')} | Next Deadline in {dl.get('hours_left', 0):.1f} hrs")
    except Exception as e:
        print(f"  ❌ FPL API: Error -> {e}")
        
    try:
        ls = LiveScoreEngine()
        live = ls.get_live_matches()
        print(f"  ✅ LiveScore API: Active | {len(live)} live soccer matches worldwide")
    except Exception as e:
        print(f"  ❌ LiveScore API: Error -> {e}")
        
    try:
        ne = NewsEngine()
        news = ne.fetch_arabic_sports_news(limit=3)
        print(f"  ✅ News Engine: Active | {len(news)} fresh Arabic articles fetched")
    except Exception as e:
        print(f"  ❌ News Engine: Error -> {e}")
    print("=" * 60)

def cmd_render_demo():
    print("Generating all 5 card templates...")
    p1 = render_yellow_card("كيركيز", "بورنموث", 42)
    p2 = render_goal_assist("رايندرز", "أوسكار بوب", 34)
    p3 = render_bonus([("سيمينيو", 3), ("إيكيتيكي", 2), ("كول بالمر", 1)])
    p4 = render_fulltime("بورنموث", "ليفربول", 2, 4)
    p5 = render_price_changes(
        [("كول بالمر", "تشيلسي", "£11.1m", "+£0.1m", "48.2%"), ("مبيومو", "برينتفورد", "£7.8m", "+£0.1m", "39.4%")],
        [("بوكايو ساكا", "أرسنال", "£10.0m", "-£0.1m", "31.5%"), ("إيزي", "كريستال بالاس", "£6.6m", "-£0.1m", "14.2%")],
        date_str="اليوم"
    )
    print("SUCCESS: Generated 5 sample cards in C:/Users/Mogz/fantasy-volt/output/")
    print(f"1. {p1}")
    print(f"2. {p2}")
    print(f"3. {p3}")
    print(f"4. {p4}")
    print(f"5. {p5}")

def cmd_post_prices(publish=False):
    fpl = FPLEngine()
    print("Fetching today's price changes from FPL API...")
    rising, falling = fpl.get_price_changes()
    print(f"Found: {len(rising)} rises, {len(falling)} falls")
    
    if not rising and not falling:
        print("No price changes recorded today yet.")
        return

    today_str = datetime.now().strftime("%Y-%m-%d")
    card_path = render_price_changes(rising, falling, date_str=today_str)
    print(f"Rendered price changes card: {card_path}")
    
    caption = (
        f"⚡ نشرة تغيرات أسعار الفانتازي الرسمية ({today_str}) |\n\n"
        f"📈 أبرز الارتفاعات:\n" + "\n".join([f"• {n} ({t}): {c} ⬅️ {p}" for n, t, p, c, o in rising[:3]]) + "\n\n"
        f"📉 أبرز الانخفاضات:\n" + "\n".join([f"• {n} ({t}): {c} ⬅️ {p}" for n, t, p, c, o in falling[:3]]) + "\n\n"
        f"مين من دول في تشكيلتك؟ شاركنا في الكومنتات! 👇\n"
        f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt"
    )
    
    if publish:
        print("Publishing to Fantasy Volt page...")
        res = post_photo(card_path, caption=caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("\nGenerated Caption (preview):\n", caption)
        print("\nRun with --publish to publish live to Facebook.")

def cmd_morning_fixtures(publish=False):
    today_str = datetime.now().strftime("%Y-%m-%d")
    matches = [
        {"home": "مانشستر سيتي", "away": "ليفربول", "time": "6:30 م", "comp": "الدوري الإنجليزي"},
        {"home": "ريال مدريد", "away": "برشلونة", "time": "9:00 م", "comp": "الدوري الإسباني"},
        {"home": "الأهلي", "away": "الزمالك", "time": "7:00 م", "comp": "الدوري المصري الممتاز"},
        {"home": "بايرن ميونخ", "away": "دورتموند", "time": "7:30 م", "comp": "الدوري الألماني"}
    ]
    card_path = render_today_fixtures(matches, date_str=today_str)
    print(f"Rendered morning fixtures card: {card_path}")
    
    caption = (
        f"⚡ جدول أهم مباريات اليوم ({today_str}) • بتوقيت القاهرة |\n\n"
        f"🏴󠁧󠁢󠁥󠁮󠁧󠁿 مانشستر سيتي 🆚 ليفربول (6:30 م)\n"
        f"🇪🇸 ريال مدريد 🆚 برشلونة (9:00 م)\n"
        f"🇪🇬 الأهلي 🆚 الزمالك (7:00 م)\n"
        f"🇩🇪 بايرن ميونخ 🆚 دورتموند (7:30 م)\n\n"
        f"💬 قمة الليلة في رأيك هتنتهي كام كام؟ شاركنا توقعاتك في التعليقات! 👇\n"
        f"#كورة_ڤولت #مباريات_اليوم #الدوري_الانجليزي #الكلاسيكو"
    )
    
    if publish:
        print("Publishing morning fixtures to Kora Volt page...")
        res = post_photo(card_path, caption=caption, page_key="kora_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("\nGenerated Caption (preview):\n", caption)
        print("\nRun with --publish to publish live to Facebook.")

def cmd_photo_news(publish=False, count=1):
    engine = PhotoNewsEngine()
    stories = engine.fetch_top_stories_with_photos(limit=count)
    if not stories:
        print("No fresh photo stories found.")
        return
        
    for i, story in enumerate(stories, 1):
        caption = engine.format_filgoal_style_caption(story)
        fname = f"story_{i}_{hash(story['title']) % 10000}.jpg"
        img_path = download_image(story["img_url"], fname)
        
        print(f"\n--- [PHOTO NEWS #{i}] ---")
        print("Entity:", story["entity_ar"], f"({story['entity_en']})")
        print("Image:", img_path)
        print("Caption:\n", caption)
        
        if publish and img_path:
            print("Publishing photo post to Kora Volt page...")
            try:
                res = post_photo(img_path, caption=caption, page_key="kora_volt")
                print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
                engine.mark_posted(story["title"])
            except Exception as e:
                print("Publish Error:", e)
        else:
            print("(Dry-run: not published. Add --publish to post live)")

def cmd_post_news(publish=False, count=1):
    engine = NewsEngine()
    news = engine.fetch_news_stream(limit=count * 3)
    if not news:
        print("No new unposted articles found.")
        return
        
    posted_count = 0
    for item in news:
        if posted_count >= count:
            break
        caption = engine.format_engaging_post(item)
        print(f"\n--- [NEWS POST #{posted_count + 1}] ---")
        print(caption)
        
        if publish:
            print(f"Publishing to Kora Volt page...")
            try:
                res = post_text(caption, page_key="kora_volt")
                print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
                engine.mark_posted(item["title"], item.get("category"))
                posted_count += 1
            except Exception as e:
                print("Publish Error:", e)
        else:
            posted_count += 1
            print("(Dry-run: not published. Add --publish to post live)")

def cmd_fpl_debate(publish=False, mode="debate"):
    boot = FPLEngine().fetch_bootstrap()
    curr_gw = next((e for e in boot.get("events", []) if e.get("is_current")), None)
    gw_name = curr_gw.get("name", "الجولة") if curr_gw else "الجولة القادمة"
    
    if mode == "closed":
        post_txt = (
            f"🚨 قفلت خلاص.. الديدلاين أغلق رسميًا لـ {gw_name}! 🔒\n\n"
            f"أهم قرار أخدته في التشكيلة إيه؟ 🤔\n"
            f"👑 الكابتن مع مين؟\n"
            f"🔄 عملت كام تبديل وسالب كام؟\n"
            f"🃏 فعلت أي خاصية في الجولة دي؟\n\n"
            f"شاركنا تشكيلتك وكابتنك في الكومنتات.. وبالتوفيق لكل المدربين! ⚡\n\n"
            f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt"
        )
    elif mode == "warning":
        post_txt = (
            f"⏳ تنبيه الفرصة الأخيرة | {gw_name} ⚡\n\n"
            f"باقي ساعة واحدة فقط على إغلاق الديدلاين!\n\n"
            f"تأكد من:\n"
            f"✅ تفعيل الكابتن وتحديد نائب الكابتن (Vice Captain)\n"
            f"✅ ترتيب دكة البدلاء بعناية\n"
            f"✅ مراجعة آخر تقارير الإصابات\n\n"
            f"مين اللاعب اللي لسه محتار تبيعه ولا تخليه؟ 👇\n\n"
            f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt"
        )
    else:
        debates = [
            (
                f"⚡ حيرة الكابتنة في {gw_name} | فانتازي ڤولت\n\n"
                f"لو التشكيلة بتاعتك فيها:\n"
                f"👑 محمد صلاح (ماتش قوي على ملعبه)\n"
                f"🤖 إيرلينج هالاند (مواجهة صعبة خارج الأرض)\n"
                f"🪄 كول بالمر (فورمة استثنائية)\n\n"
                f"الكابتن المضمون في رأيك مين؟ والريسك مع مين؟ 🤔👇\n\n"
                f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt #صلاح #هالاند"
            ),
            (
                f"🔥 سؤال الموسم للمدربين | فانتازي ڤولت\n\n"
                f"معاك كاش 10.5 مليون.. ومحتاج لاعب وسط سوبر يفرق في الترتيب:\n"
                f"1️⃣ كول بالمر (تشيلسي)\n"
                f"2️⃣ بوكايو ساكا (أرسنال)\n\n"
                f"هتختار مين فيهم بدون تردد وليه؟ شاركنا اختيارك! 👇\n\n"
                f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt"
            ),
            (
                f"📊 الخيارات التفاضلية (Differentials) | فانتازي ڤولت\n\n"
                f"أفضل 3 لاعبين بنسبة ملكية أقل من 10% قادرين يفجروا الترتيب في الجولات القادمة:\n\n"
                f"🎯 إيزي (كريستال بالاس) - جدول مباريات مميز\n"
                f"🎯 كولوسيفسكي (توتنهام) - صانع الفرص الأول للفريق\n"
                f"🎯 مورجان روجرز (أستون فيلا) - سعر اقتصادي وأساسي دائم\n\n"
                f"مين فيهم عينك عليه في تشكيلتك؟ شاركنا في الكومنتات! 👇\n\n"
                f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt"
            )
        ]
        import random
        post_txt = random.choice(debates)

    print("\n--- [BEIN FANTASY STYLE POST] ---")
    print(post_txt)
    
    if publish:
        print("Publishing to Fantasy Volt page...")
        res = post_text(post_txt, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("\n(Dry-run: not published. Add --publish to post live)")


def cmd_fpl_quiz(publish=False):
    fce = FantasyContentEngine()
    q = fce.get_quiz_post()
    caption = q["question"]
    entity = q["entity"]
    
    img_url = fetch_entity_photo(entity)
    img_path = download_image(img_url, f"quiz_{entity.replace(' ', '_')}.jpg") if img_url else None
    
    print("\n--- [FPL QUIZ POST] ---")
    print("Entity:", entity, "| Image:", img_path)
    print(caption)
    
    if publish:
        print("Publishing Quiz to Fantasy Volt...")
        if img_path:
            res = post_photo(img_path, caption=caption, page_key="fantasy_volt")
        else:
            res = post_text(caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("(Dry-run: not published. Add --publish to post live)")

def cmd_fpl_facts(publish=False):
    fce = FantasyContentEngine()
    f = fce.get_facts_post()
    caption = f["text"]
    entity = f["entity"]
    
    img_url = fetch_entity_photo(entity)
    img_path = download_image(img_url, f"fact_{entity.replace(' ', '_')}.jpg") if img_url else None
    
    print("\n--- [FPL FACTS POST] ---")
    print("Entity:", entity, "| Image:", img_path)
    print(caption)
    
    if publish:
        print("Publishing Fact to Fantasy Volt...")
        if img_path:
            res = post_photo(img_path, caption=caption, page_key="fantasy_volt")
        else:
            res = post_text(caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("(Dry-run: not published. Add --publish to post live)")

def cmd_fpl_picks(publish=False):
    fce = FantasyContentEngine()
    p = fce.get_captaincy_picks_post()
    caption = p["text"]
    entity = p["entity"]
    
    img_url = fetch_entity_photo(entity)
    img_path = download_image(img_url, f"picks_{entity.replace(' ', '_')}.jpg") if img_url else None
    
    print("\n--- [FPL PICKS POST] ---")
    print("Entity:", entity, "| Image:", img_path)
    print(caption)
    
    if publish:
        print("Publishing Picks to Fantasy Volt...")
        if img_path:
            res = post_photo(img_path, caption=caption, page_key="fantasy_volt")
        else:
            res = post_text(caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("(Dry-run: not published. Add --publish to post live)")

def cmd_fpl_differentials(publish=False):
    fce = FantasyContentEngine()
    d = fce.get_differentials_post()
    caption = d["text"]
    entity = d["entity"]
    
    img_url = fetch_entity_photo(entity)
    img_path = download_image(img_url, f"diff_{entity.replace(' ', '_')}.jpg") if img_url else None
    
    print("\n--- [FPL DIFFERENTIALS POST] ---")
    print("Entity:", entity, "| Image:", img_path)
    print(caption)
    
    if publish:
        print("Publishing Differentials to Fantasy Volt...")
        if img_path:
            res = post_photo(img_path, caption=caption, page_key="fantasy_volt")
        else:
            res = post_text(caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("(Dry-run: not published. Add --publish to post live)")

def cmd_fpl_price_alert(publish=False):
    fce = FantasyContentEngine()
    pr = fce.get_evening_price_prediction_post()
    caption = pr["text"]
    entity = pr["entity"]
    
    img_url = fetch_entity_photo(entity)
    img_path = download_image(img_url, f"pr_alert_{entity.replace(' ', '_')}.jpg") if img_url else None
    
    print("\n--- [FPL PRICE ALERT POST] ---")
    print("Entity:", entity, "| Image:", img_path)
    print(caption)
    
    if publish:
        print("Publishing Price Alert to Fantasy Volt...")
        if img_path:
            res = post_photo(img_path, caption=caption, page_key="fantasy_volt")
        else:
            res = post_text(caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("(Dry-run: not published. Add --publish to post live)")


def cmd_vector_goal(scorer="محمد صلاح", assister="لويس دياز", team="ليفربول", minute=34, stats="هدف رائع", publish=False):
    card_path = render_vector_goal_card(scorer, assister, team, minute, stats)
    print(f"\nRendered Vector Goal Card: {card_path}")
    
    caption = (
        f"⚽ جوووووووووول! {scorer} يسجل لـ {team}! 🔥👑\n"
        f"🅰️ أسيست: {assister}\n"
        f"⏱️ الدقيقة: {minute}'\n\n"
        f"مين مأكبتنه ومعاه في التشكيلة؟ احسب نقطك! ⚡\n"
        f"#فانتازي_الدوري_الانجليزي #FPL #FantasyVolt #{team.replace(' ', '_')}"
    )
    print("Caption:\n", caption)
    
    if publish:
        print("Publishing Vector Goal Card to Fantasy Volt page...")
        res = post_photo(card_path, caption=caption, page_key="fantasy_volt")
        print("PUBLISHED SUCCESSFULLY! Post ID:", res.get("id"))
    else:
        print("\n(Dry-run: not published. Add --publish to post live)")

def main():
    parser = argparse.ArgumentParser(description="Fantasy Volt & Kora Volt Automation")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    subparsers.add_parser("status", help="Check system, tokens, and APIs status")
    subparsers.add_parser("render-demo", help="Render all 5 design templates")
    
    p_prices = subparsers.add_parser("prices", help="Fetch FPL price changes & render card")
    p_prices.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    
    p_news = subparsers.add_parser("news", help="Fetch latest sports news")
    p_news.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    p_news.add_argument("--count", type=int, default=1, help="Number of distinct news articles to post")
    
    p_pnews = subparsers.add_parser("photo-news", help="Fetch sports news WITH high-res photos (beIN style)")
    p_pnews.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    p_pnews.add_argument("--count", type=int, default=1, help="Number of photo news posts")
    
    p_fpl = subparsers.add_parser("fpl-debate", help="Post an engaging FPL debate/discussion")
    p_fpl.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    p_fpl.add_argument("--mode", choices=["debate", "warning", "closed"], default="debate", help="Type of FPL post")
    
    p_morn = subparsers.add_parser("morning", help="Generate today's fixtures card & publish")
    p_morn.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    
    p_quiz = subparsers.add_parser("fpl-quiz", help="Post interactive FPL quiz")
    p_quiz.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    p_facts = subparsers.add_parser("fpl-facts", help="Post FPL historical facts")
    p_facts.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    p_picks = subparsers.add_parser("fpl-picks", help="Post FPL captaincy picks")
    p_picks.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    p_diffs = subparsers.add_parser("fpl-differentials", help="Post FPL differentials")
    p_diffs.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    p_pr_alert = subparsers.add_parser("fpl-price-alert", help="Post evening price prediction alert")
    p_pr_alert.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    p_vg = subparsers.add_parser("vector-goal", help="Render Pop-Art Vector Goal & Assist Card")
    p_vg.add_argument("--scorer", default="محمد صلاح", help="Goal scorer Arabic name")
    p_vg.add_argument("--assister", default="لويس دياز", help="Assist provider Arabic name")
    p_vg.add_argument("--team", default="ليفربول", help="Team Arabic name")
    p_vg.add_argument("--minute", type=int, default=34, help="Match minute")
    p_vg.add_argument("--stats", default="هدف رائع", help="Short stat line")
    p_vg.add_argument("--publish", action="store_true", help="Publish directly to Facebook")

    args = parser.parse_args()
    
    if args.command == "status":
        cmd_status()
    elif args.command == "render-demo":
        cmd_render_demo()
    elif args.command == "prices":
        cmd_post_prices(publish=args.publish)
    elif args.command == "morning":
        cmd_morning_fixtures(publish=args.publish)
    elif args.command == "news":
        cmd_post_news(publish=args.publish, count=args.count)
    elif args.command == "photo-news":
        cmd_photo_news(publish=args.publish, count=args.count)
    elif args.command == "vector-goal":
        cmd_vector_goal(
            scorer=args.scorer,
            assister=args.assister,
            team=args.team,
            minute=args.minute,
            stats=args.stats,
            publish=args.publish
        )
    elif args.command == "fpl-quiz":
        cmd_fpl_quiz(publish=args.publish)
    elif args.command == "fpl-facts":
        cmd_fpl_facts(publish=args.publish)
    elif args.command == "fpl-picks":
        cmd_fpl_picks(publish=args.publish)
    elif args.command == "fpl-differentials":
        cmd_fpl_differentials(publish=args.publish)
    elif args.command == "fpl-price-alert":
        cmd_fpl_price_alert(publish=args.publish)
    elif args.command == "fpl-debate":
        cmd_fpl_debate(publish=args.publish, mode=getattr(args, "mode", "debate"))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
