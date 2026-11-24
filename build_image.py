#!/usr/bin/env python3
"""Build entry.png — 'The World in One Page', Monday 23 November 2026.

Deterministic news-poster rendered with Pillow from the real headlines of
23 Nov 2026 (researched from BBC / Reuters / CNN / AP / AFP reporting that
day; see README.md for the source list). No network, no randomness, no
timestamps: re-running this script writes byte-identical output.

Layout (1024x1024, newspaper front page):
  masthead | lead story (COP31) with globe art | 6-card story grid |
  'Also today' strip | footer.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (247, 243, 233)
INK = (18, 24, 32)
NAVY = (12, 35, 64)
NAVY_LT = (27, 58, 96)
RED = (192, 39, 34)
RED_DK = (150, 28, 26)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (203, 196, 180)
MUTED = (84, 88, 96)
SKY = (146, 196, 228)
SEA = (64, 130, 180)
LAND = (96, 160, 110)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, max_w, fill, spacing=4, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def tag_chip(d, x, y, label, bg):
    f = font(F_SANS_B, 15)
    w = int(d.textlength(label, font=f)) + 20
    d.rounded_rectangle([x, y, x + w, y + 24], radius=4, fill=bg)
    d.text((x + 10, y + 4), label, font=f, fill=WHITE)
    return w


def globe(d, cx, cy, r):
    """Stylised globe: blue disc, meridians, abstract continents, red crack."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA, outline=NAVY, width=3)
    for k in (-0.55, -0.28, 0.0, 0.28, 0.55):
        d.ellipse([cx - r + int(abs(k) * r * 0.55), cy - r,
                   cx + r - int(abs(k) * r * 0.55), cy + r],
                  outline=(255, 255, 255, 160), width=2)
    for dy in (-int(r * 0.45), 0, int(r * 0.45)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(255, 255, 255, 160), width=2)
        d.line([cx - r, cy + dy, cx + r, cy + dy], fill=(255, 255, 255, 110), width=2)
    # abstract continents
    d.ellipse([cx - int(r * 0.72), cy - int(r * 0.62), cx - int(r * 0.05), cy - int(r * 0.08)],
              fill=LAND)
    d.ellipse([cx + int(r * 0.08), cy + int(r * 0.05), cx + int(r * 0.62), cy + int(r * 0.58)],
              fill=LAND)
    d.ellipse([cx - int(r * 0.25), cy + int(r * 0.42), cx + int(r * 0.28), cy + int(r * 0.78)],
              fill=LAND)
    # red crack across the disc
    d.line([(cx - int(r * 0.42), cy - r), (cx - int(r * 0.10), cy - int(r * 0.42)),
            (cx - int(r * 0.36), cy + int(r * 0.05)), (cx + int(r * 0.05), cy + int(r * 0.47)),
            (cx - int(r * 0.05), cy + r)],
           fill=RED, width=4, joint="curve")


def card(d, x, y, w, h, tag, tag_bg, headline, deck, head_size=24):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD, outline=LINE, width=1)
    d.rectangle([x + 2, y + 2, x + w - 2, y + 6], fill=tag_bg)
    tag_chip(d, x + 16, y + 14, tag, tag_bg)
    draw_wrapped(d, x + 16, y + 46, headline, font(F_SERIF, head_size), w - 32,
                 INK, spacing=2, max_lines=2)
    draw_wrapped(d, x + 16, y + 104, deck, font(F_SANS, 15), w - 32, MUTED,
                 spacing=3, max_lines=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- frame ----
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=2)

    # ---- masthead ----
    d.rectangle([6, 6, W - 7, 122], fill=NAVY)
    d.text((28, 22), "THE WORLD", font=font(F_SERIF, 64), fill=WHITE)
    d.text((28, 92), "IN ONE PAGE", font=font(F_SANS_B, 17), fill=GOLD)
    d.text((1018 - 28 - int(d.textlength("MONDAY 23 NOVEMBER 2026", font=font(F_SANS_B, 21))),
            30), "MONDAY 23 NOVEMBER 2026", font=font(F_SANS_B, 21), fill=WHITE)
    d.text((1018 - 28 - int(d.textlength("ONE DAY  •  ONE IMAGE", font=font(F_SANS, 15))),
            62), "ONE DAY  •  ONE IMAGE", font=font(F_SANS, 15), fill=(180, 200, 225))
    d.text((1018 - 28 - int(d.textlength("WORLD NEWS  •  23 NOV 2026", font=font(F_SANS, 15))),
            86), "WORLD NEWS  •  23 NOV 2026", font=font(F_SANS, 15), fill=(180, 200, 225))
    d.rectangle([6, 122, W - 7, 128], fill=RED)

    # ---- lead story ----
    d.text((28, 138), "CLIMATE  •  COP31, ANTALYA, TÜRKIYE", font=font(F_SANS_B, 17), fill=RED)
    d.text((28, 162), "COP31 COLLAPSES:", font=font(F_SERIF, 46), fill=INK)
    d.text((28, 214), "NO DEAL ON CLIMATE", font=font(F_SERIF, 46), fill=INK)
    draw_wrapped(d, 28, 274,
                 "After record overtime talks, nearly 200 nations fail to agree a "
                 "final pact. Fossil-fuel language is stripped from the draft; the EU "
                 "and island states refuse to sign a text that does not even name coal, "
                 "oil and gas.",
                 font(F_SANS, 18), 640, MUTED, spacing=4, max_lines=3)
    globe(d, 858, 252, 96)
    d.text((858 - int(d.textlength("NO DEAL", font=font(F_SANS_B, 20)) / 2), 360),
           "NO DEAL", font=font(F_SANS_B, 20), fill=RED_DK)

    d.line([28, 392, W - 28, 392], fill=LINE, width=2)

    # ---- story grid: 2 cols x 3 rows ----
    gx, gy = 28, 406
    cw, ch, gap = 472, 148, 24
    cards = [
        ("UKRAINE", NAVY_LT,
         "Trump: peace plan is \u201cnot my final offer\u201d",
         "The 28-point US plan gives Kyiv until 27 Nov to reply. Envoy Kushner "
         "floats NATO-style security guarantees."),
        ("WAR", RED,
         "15 killed near Kyiv; Ukraine sinks ship off Libya",
         "Russian strikes hit the Kyiv region. Zelenskyy says naval drones sank "
         "a Russian corvette at Benghazi."),
        ("TECH", (43, 92, 140),
         "Nvidia brings back Jensen Huang as CEO",
         "The board reinstates its chief with immediate effect after pressure "
         "from President Trump. Shares jump."),
        ("MIDDLE EAST", (120, 72, 20),
         "US hits Iran with sweeping new sanctions",
         "Washington targets the regime\u2019s \u201clast financial lifeline\u201d. "
         "Tehran vows to counter any Hormuz blockade."),
        ("ASIA", TEAL,
         "Factory fire in Indonesia kills at least 24",
         "A blaze at a sweets factory near Jakarta leaves about 30 people "
         "missing as rescuers search the wreckage."),
        ("INDIA \u2013 NEPAL", (90, 60, 120),
         "Modi offers Nepal NPR 24,000 crore in aid",
         "Eight deals signed and a new Ayodhya\u2013Janakpur train launched as "
         "Nepal PM Balendra Shah ends his Delhi visit."),
    ]
    for i, (tag, bg, head, deck) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + 14)
        card(d, x, y, cw, ch, tag, bg, head, deck)

    # ---- also today strip ----
    ay = 406 + 3 * ch + 2 * 12 + 14
    d.rectangle([28, ay, W - 28, ay + 82], fill=NAVY)
    d.text((48, ay + 10), "ALSO TODAY", font=font(F_SANS_B, 16), fill=GOLD)
    draw_wrapped(d, 48, ay + 34,
                 "Democrats win their largest US House majority since 1992 (258 seats)  •  "
                 "FIFA: 2031 Women\u2019s World Cup to the USA, Mexico, Costa Rica & Jamaica  •  "
                 "BepiColombo reaches Mercury  •  AI \u201cproves\u201d the "
                 "Riemann hypothesis \u2014 claim disputed",
                 font(F_SANS, 15), W - 96, (235, 240, 248), spacing=4, max_lines=2)

    # ---- footer ----
    fy = ay + 82 + 12
    d.text((28, fy), "Headlines as reported on Monday 23 November 2026",
           font=font(F_SANS_B, 14), fill=INK)
    d.text((28, fy + 20), "Sources: BBC, Reuters, CNN, AP, AFP",
           font=font(F_SANS, 13), fill=MUTED)
    right = "THE WORLD IN ONE PAGE"
    d.text((W - 28 - int(d.textlength(right, font=font(F_SANS_B, 14))), fy),
           right, font=font(F_SANS_B, 14), fill=INK)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
