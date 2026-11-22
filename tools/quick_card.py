"""
Quick Card CLI — Instant 1-second card generator and publisher.
Fast execution without scraping or overhead.
Usage:
  python tools/quick_card.py --template 1 --title "العنوان" --speaker "الصحفي فابريزيو رومانو" --photo "path.jpg" [--publish]
  python tools/quick_card.py --template 2 --title "نص التصريح الطويل" --speaker "اللاعب واين روني" --photo "path.jpg" [--publish]
"""

import argparse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from engines.template_card_engine import render_template_card, render_statement_card
from publish.fb import post_photo


def parse_speaker(speaker_str):
    """Splits 'الصحفي فابريزيو رومانو' into role ('الصحفي') and name ('فابريزيو رومانو')"""
    parts = speaker_str.strip().split(maxsplit=1)
    if len(parts) == 2 and parts[0] in ["الصحفي", "صحيفة", "اللاعب", "المدرب", "نادي", "شبكة", "منصة", "المصدر"]:
        return parts[0], parts[1]
    return "المصدر", speaker_str


def main():
    parser = argparse.ArgumentParser(description="Quick Volt Card Tool")
    parser.add_argument("--template", type=int, choices=[1, 2], default=1, help="1 for breaking, 2 for manchette")
    parser.add_argument("--title", required=True, help="Headline or statement text")
    parser.add_argument("--speaker", default="كورة ڤولت", help="Speaker or source with role")
    parser.add_argument("--photo", required=True, help="Path to photo")
    parser.add_argument("--page", default="kora_volt", choices=["kora_volt", "fantasy_volt"])
    parser.add_argument("--publish", action="store_true", help="Publish directly to Facebook")
    
    args = parser.parse_args()
    role, name = parse_speaker(args.speaker)
    
    out_file = f"quick_card_t{args.template}.png"
    if args.template == 1:
        card = render_template_card(
            photo_path=args.photo,
            headline=args.title,
            source_role=role,
            source_name=name,
            output_filename=out_file
        )
    else:
        card = render_statement_card(
            photo_path=args.photo,
            statement_text=args.title,
            source_role=role,
            source_name=name,
            output_filename=out_file
        )
        
    print(f"✅ Card generated in <1s: {card}")
    
    if args.publish:
        brand = "#كورة_ڤولت" if args.page == "kora_volt" else "#فانتازي_ڤولت"
        caption = f"⚡ {args.title}\n\n{brand}"
        res = post_photo(image_path=card, caption=caption, page_key=args.page)
        print(f"🚀 Published! Post ID: {res.get('id') or res.get('post_id')}")


if __name__ == "__main__":
    main()
