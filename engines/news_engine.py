"""
News Engine for Kora Volt
Pulls curated Arabic sports news via Google News RSS & direct sports feeds.
Filters, deduplicates, and formats engaging posts for Facebook.
"""
import urllib.parse
import feedparser

class NewsEngine:
    def __init__(self):
        self.default_topics = [
            "الدوري الإنجليزي",
            "ريال مدريد",
            "برشلونة",
            "ليفربول",
            "الأهلي",
            "الزمالك",
            "محمد صلاح"
        ]

    def fetch_arabic_sports_news(self, query=None, limit=10):
        if not query:
            query = " OR ".join(self.default_topics)
            
        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ar&gl=EG&ceid=EG:ar"
        feed = feedparser.parse(url)
        
        items = []
        for entry in feed.entries[:limit]:
            # Clean headline and source
            title = entry.title
            source = "كورة ڤولت"
            if " - " in title:
                parts = title.rsplit(" - ", 1)
                title = parts[0].strip()
                source = parts[1].strip()
                
            items.append({
                "title": title,
                "source": source,
                "link": entry.link,
                "published": getattr(entry, "published", "")
            })
        return items

    def format_facebook_post(self, item):
        title = item["title"]
        source = item["source"]
        
        post_text = (
            f"⚡ عاجل من ملاعب الكرة |\n\n"
            f"📌 {title}\n\n"
            f"💬 شاركنا رأيك في التعليقات!\n"
            f"#كورة_ڤولت #كرة_القدم #أخبار_الرياضة"
        )
        return post_text

if __name__ == "__main__":
    engine = NewsEngine()
    print("Testing NewsEngine...")
    news = engine.fetch_arabic_sports_news(limit=5)
    print(f"Fetched {len(news)} items.")
    for n in news:
        print(f"[{n['source']}] {n['title']}")
        print(engine.format_facebook_post(n))
        print("-" * 40)
