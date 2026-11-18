"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Reads news.json next to this file and renders a newspaper-style infographic:
masthead with the date, one lead story with a drawn illustration, four
regional stories with flat pictograms, a tech strip and an "also on the
day" ticker. Pure Pillow, no network, deterministic output.
"""

import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 46)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (193, 39, 45)
TEAL = (18, 92, 96)
GREEN = (46, 125, 50)
CARD_LINE = (216, 207, 184)
GREY = (90, 90, 100)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def burst(draw, cx, cy, r_out, r_in, points, color):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=color)


def icon_burst(draw, x, y, s):
    burst(draw, x + s / 2, y + s / 2, s * 0.48, s * 0.22, 10, (232, 126, 32))
    burst(draw, x + s / 2, y + s / 2, s * 0.26, s * 0.12, 8, (245, 197, 66))


def icon_virus(draw, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.30
    for i in range(8):
        a = math.pi * i / 4
        draw.line([cx + r * math.cos(a), cy + r * math.sin(a),
                   cx + (r + s * 0.14) * math.cos(a),
                   cy + (r + s * 0.14) * math.sin(a)],
                  fill=RED, width=4)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    for dx, dy in [(-0.12, -0.10), (0.12, 0.08), (0.0, 0.14)]:
        draw.ellipse([cx + dx * s - 3, cy + dy * s - 3,
                      cx + dx * s + 3, cy + dy * s + 3], fill=(255, 255, 255))


def icon_ballot(draw, x, y, s):
    draw.rectangle([x + s * 0.08, y + s * 0.30, x + s * 0.92, y + s * 0.88],
                   fill=NAVY)
    draw.rectangle([x + s * 0.30, y + s * 0.30, x + s * 0.70, y + s * 0.40],
                   fill=PAPER)
    draw.line([x + s * 0.28, y + s * 0.62, x + s * 0.45, y + s * 0.76,
               x + s * 0.74, y + s * 0.44], fill=(255, 255, 255), width=6,
              joint="curve")
    draw.polygon([(x + s * 0.30, y + s * 0.02), (x + s * 0.52, y + s * 0.02),
                  (x + s * 0.46, y + s * 0.24), (x + s * 0.24, y + s * 0.24)],
                 fill=(255, 255, 255), outline=NAVY)


def icon_court(draw, x, y, s):
    draw.polygon([(x + s * 0.04, y + s * 0.34), (x + s * 0.50, y + s * 0.04),
                  (x + s * 0.96, y + s * 0.34)], fill=NAVY)
    for i in range(3):
        cx = x + s * (0.22 + 0.28 * i)
        draw.rectangle([cx - 5, y + s * 0.42, cx + 5, y + s * 0.80],
                       fill=NAVY)
    draw.rectangle([x + s * 0.06, y + s * 0.84, x + s * 0.94, y + s * 0.94],
                   fill=NAVY)


def icon_chip(draw, x, y, s):
    draw.rectangle([x + s * 0.18, y + s * 0.18, x + s * 0.82, y + s * 0.82],
                   fill=GREEN)
    draw.rectangle([x + s * 0.36, y + s * 0.36, x + s * 0.64, y + s * 0.64],
                   fill=(255, 255, 255))
    for i in range(3):
        off = s * (0.30 + 0.20 * i)
        draw.line([x + off, y + s * 0.06, x + off, y + s * 0.18],
                  fill=GREEN, width=4)
        draw.line([x + off, y + s * 0.82, x + off, y + s * 0.94],
                  fill=GREEN, width=4)
        draw.line([x + s * 0.06, y + off, x + s * 0.18, y + off],
                  fill=GREEN, width=4)
        draw.line([x + s * 0.82, y + off, x + s * 0.94, y + off],
                  fill=GREEN, width=4)


ICONS = [icon_burst, icon_virus, icon_ballot, icon_court]
ACCENTS = [(232, 126, 32), RED, NAVY, (90, 60, 140)]


def draw_bridge(draw, x0, y0, x1, y1):
    """Lead illustration: a sea strait, a bridge with its middle span down."""
    draw.rectangle([x0, y0, x1, y1], fill=(191, 217, 232))
    sea_y = y0 + int((y1 - y0) * 0.58)
    draw.rectangle([x0, sea_y, x1, y1], fill=(46, 110, 142))
    for wy in (sea_y + 26, sea_y + 62, sea_y + 96):
        for wx in range(x0 + 12, x1 - 30, 64):
            draw.arc([wx, wy, wx + 44, wy + 16], 0, 180, fill=(255, 255, 255),
                     width=3)
    mid = (x0 + x1) // 2
    gap = 64
    # deck: left and right of the gap
    draw.rectangle([x0 + 8, sea_y - 58, mid - gap // 2, sea_y - 48],
                   fill=(60, 60, 70))
    draw.rectangle([mid + gap // 2, sea_y - 58, x1 - 8, sea_y - 48],
                   fill=(60, 60, 70))
    # collapsed span, tilted down into the water
    draw.polygon([(mid - gap // 2, sea_y - 48), (mid + gap // 2, sea_y - 48),
                  (mid + gap // 2 - 14, sea_y + 34),
                  (mid - gap // 2 - 14, sea_y + 34)], fill=(90, 90, 100))
    # towers
    for tx in (x0 + 52, x1 - 52):
        draw.rectangle([tx - 6, sea_y - 128, tx + 6, sea_y - 48],
                       fill=(60, 60, 70))
        draw.line([tx, sea_y - 128, mid - gap // 2, sea_y - 52],
                  fill=(120, 120, 130), width=2)
        draw.line([tx, sea_y - 128, mid + gap // 2, sea_y - 52],
                  fill=(120, 120, 130), width=2)
    # explosion over the gap
    burst(draw, mid, sea_y - 84, 46, 20, 10, (232, 126, 32))
    burst(draw, mid, sea_y - 84, 24, 10, 8, (245, 197, 66))
    for cx, cy, r in [(mid - 34, sea_y - 116, 16), (mid + 30, sea_y - 122, 13),
                      (mid + 52, sea_y - 100, 10)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 125))
    draw.rectangle([x0, y0, x1, y1], outline=NAVY, width=3)


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 168], fill=NAVY)
    d.rectangle([0, 168, W, 172], fill=GOLD)
    d.text((W // 2, 20), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 58), fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 96), "TUESDAY  •  17 NOVEMBER  •  2026",
           font=font(SANS_B, 34), fill=(245, 197, 66), anchor="ma")
    d.text((W // 2, 140), "ONE DAY  •  ONE IMAGE  •  THE WHOLE WORLD",
           font=font(SANS, 17), fill=(190, 200, 220), anchor="ma")

    # ---- lead story ----
    lead = news["lead"]
    d.text((36, 192), lead["kicker"], font=font(SANS_B, 22), fill=RED)
    y = 224
    for line in wrap(d, lead["headline"], font(SERIF_B, 45), 560):
        d.text((36, y), line, font=font(SERIF_B, 45), fill=INK)
        y += 54
    y += 6
    for line in wrap(d, lead["summary"], font(SANS, 23), 560):
        d.text((36, y), line, font=font(SANS, 23), fill=(50, 50, 66))
        y += 30
    draw_bridge(d, 624, 192, 988, 492)

    # ---- story grid ----
    d.line([36, 516, 988, 516], fill=NAVY, width=3)
    card_w, card_h, gap = 466, 132, 20
    for i, story in enumerate(news["stories"]):
        cx = 36 + (i % 2) * (card_w + gap)
        cy = 532 + (i // 2) * (card_h + gap)
        accent = ACCENTS[i]
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=(255, 255, 255),
                    outline=CARD_LINE, width=2)
        d.rectangle([cx, cy, cx + 8, cy + card_h], fill=accent)
        ICONS[i](d, cx + 22, cy + 16, 62)
        tx = cx + 100
        d.text((tx, cy + 12), story["kicker"], font=font(SANS_B, 16),
               fill=accent)
        hy = cy + 34
        for line in wrap(d, story["headline"], font(SANS_B, 23),
                         card_w - 116)[:2]:
            d.text((tx, hy), line, font=font(SANS_B, 23), fill=INK)
            hy += 27
        for line in wrap(d, story["summary"], font(SANS, 17),
                         card_w - 116)[:2]:
            d.text((tx, hy), line, font=font(SANS, 17), fill=(60, 60, 74))
            hy += 21

    # ---- tech strip ----
    ty = 816
    d.rectangle([36, ty, 988, ty + 72], fill=(255, 243, 214),
                outline=CARD_LINE, width=2)
    icon_chip(d, 52, ty + 8, 56)
    tech = news["tech"]
    d.text((124, ty + 6), tech["kicker"], font=font(SANS_B, 16), fill=GREEN)
    d.text((124, ty + 26), tech["headline"], font=font(SANS_B, 23), fill=INK)
    d.text((124, ty + 52), tech["summary"], font=font(SANS, 16),
           fill=(60, 60, 74))

    # ---- ticker ----
    d.line([36, 906, 988, 906], fill=NAVY, width=2)
    ticker = "ALSO ON 17 NOVEMBER:  " + "   •   ".join(news["ticker"])
    ty2 = 918
    for line in wrap(d, ticker, font(SANS, 16), 952)[:2]:
        d.text((36, ty2), line, font=font(SANS, 16), fill=(40, 40, 56))
        ty2 += 22

    # ---- footer ----
    d.line([36, 978, 988, 978], fill=CARD_LINE, width=2)
    d.text((W // 2, 988),
           "Events of Tuesday 17 November 2026, as reported that day.  "
           "Sources: " + news["sources"],
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
