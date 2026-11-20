#!/usr/bin/env python3
"""Render the front page of 19 November 2026 as one image.

Reads nothing from the network: every story below was verified against the
news of Thursday 19 November 2026 before this script was written, and the
text is baked into this file. Run:  python3 render.py  ->  entry.png
(1024 x 1024, PNG). Fonts are the DejaVu faces shipped with the system.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952

PAPER = (247, 243, 232)      # newsprint cream
INK = (20, 20, 20)           # near-black text
NAVY = (20, 33, 61)          # masthead / ticker band
RED = (180, 35, 24)          # kicker red
GOLD = (232, 184, 75)        # masthead accent
GREY = (90, 90, 90)          # footer grey
RULE = (180, 35, 24)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)     # headlines
SERIF = lambda s: font("DejaVuSerif.ttf", s)            # deck
SERIF_I = lambda s: font("DejaVuSerif.ttf", s)          # deck (no italic face; fake below)
SANS = lambda s: font("DejaVuSans.ttf", s)              # body
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)       # kickers


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; returns the y just below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tracked(draw, cx, y, text, fnt, fill, tracking=4):
    """Draw centred text with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def draw_globe(draw, cx, cy, r):
    """A simple wireframe globe: navy disc, gold meridians, red markers."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY,
                 outline=GOLD, width=4)
    # latitude lines
    for frac, w in ((-0.55, 3), (0, 3), (0.55, 3)):
        yy = cy + frac * r
        half = (r * r - (frac * r) ** 2) ** 0.5
        draw.line([cx - half, yy, cx + half, yy], fill=GOLD, width=w)
    # longitude ellipses
    for rx in (int(r * 0.45), int(r * 0.85)):
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r],
                     outline=GOLD, width=3)
    draw.line([cx, cy - r, cx, cy + r], fill=GOLD, width=3)
    # red markers: The Hague, Shenzhen, Dhaka, New York
    for ang, dist in ((210, 0.45), (20, 0.55), (60, 0.35), (300, 0.5)):
        import math
        a = math.radians(ang)
        px = cx + dist * r * math.cos(a)
        py = cy + dist * r * math.sin(a) * 0.85
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                     outline=(255, 255, 255), width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W / 2, 14), "THE WORLD IN ONE DAY", font=SERIF_B(62),
           fill=(255, 255, 255), anchor="ma")
    tracked(d, W / 2, 92, "THURSDAY  19  NOVEMBER  2026",
            SANS_B(26), GOLD, tracking=6)
    d.text((W / 2, 126), "THE DAY'S WORLD NEWS — IN ONE IMAGE",
           font=SANS(15), fill=(200, 205, 220), anchor="ma")
    d.rectangle([0, 148, W, 154], fill=RED)

    # ---------- lead story ----------
    y = 172
    d.text((MARGIN, y), "THE HAGUE  •  THE WORLD COURT",
           font=SANS_B(19), fill=RED)
    y += 30
    lead_w = 640
    y = para(d, MARGIN, y, "MYANMAR GUILTY OF GENOCIDE",
             SERIF_B(54), lead_w, 58)
    y += 6
    y = para(d, MARGIN, y,
             "The World Court rules Myanmar committed genocide against "
             "the Rohingya — the first state ever held responsible.",
             SERIF(24), lead_w, 29)
    y += 8
    y = para(d, MARGIN, y,
             "The International Court of Justice ruled 9–6 on Thursday "
             "that Myanmar's military acted with genocidal intent in the "
             "2017 clearance operations. About 10,000 Rohingya were "
             "killed; reparations were ordered.",
             SANS(19), lead_w, 25)
    # globe at the right of the lead block
    draw_globe(d, 852, 320, 108)
    d.text((852, 440), "FOUR CAPITALS, ONE DAY",
           font=SANS_B(14), fill=GREY, anchor="ma")

    # ---------- divider ----------
    d.line([MARGIN, 514, W - MARGIN, 514], fill=INK, width=2)
    d.line([MARGIN, 518, W - MARGIN, 518], fill=INK, width=1)

    # ---------- secondary grid: 2 x 2 ----------
    stories = [
        ("SHENZHEN  •  SUMMIT",
         "TRUMP, XI & PUTIN: NO NUCLEAR WAR",
         "First-ever trilateral summit ends with a four-point "
         "\u201cDeclaration toward Peace\u201d: UN reform, fuel supplies, "
         "limits on the ICC — and a dialogue on nuclear risk. Ukraine "
         "and Iran go unmentioned."),
        ("NEW YORK  •  MARKETS",
         "ANTHROPIC'S $1.5 TRILLION DEBUT AS STOCKS SLIDE",
         "The AI maker prices its IPO at $83 and starts Nasdaq trading "
         "on Thursday — while US stocks fall as fears of an AI bust "
         "spread through the market."),
        ("ANTALYA  •  CLIMATE",
         "COP31: MINISTERS RACE TO UNBLOCK TALKS",
         "Ministers meet into the night at the climate summit in "
         "Turkey, trying to bridge the gaps between nations and agree "
         "a final text."),
        ("DHAKA  •  UNREST",
         "BANGLADESH IN TURMOIL",
         "The ancestral home of leader Muhammad Yunus is set on fire "
         "and violence hits 28 districts after the death sentence on "
         "former prime minister Sheikh Hasina."),
    ]
    gx, gy = MARGIN, 530
    cell_w, cell_h = (CW - 24) // 2, 168
    for i, (kicker, head, body) in enumerate(stories):
        cx = gx + (i % 2) * (cell_w + 24)
        cy = gy + (i // 2) * (cell_h + 12)
        d.text((cx, cy), kicker, font=SANS_B(16), fill=RED)
        yy = para(d, cx, cy + 24, head, SERIF_B(25), cell_w, 30)
        para(d, cx, yy + 4, body, SANS(17), cell_w, 23)
    # vertical divider between the two columns
    d.line([W / 2, 530, W / 2, 530 + 2 * cell_h], fill=(200, 195, 180),
           width=1)

    # ---------- ticker band ----------
    d.rectangle([0, 884, W, 958], fill=NAVY)
    ticker = ("ALSO ON 19 NOVEMBER —  EU proposes a \u20ac45bn loan for "
            "Ukraine  •  Gaza peace plan scores 4/26  •  Van Gogh sells "
            "for $190.4m, a record  •  IEA: the Hormuz crisis threatens "
            "energy security")
    para(d, MARGIN, 894, ticker, SANS_B(16), CW, 24, fill=(255, 255, 255))

    # ---------- footer ----------
    d.text((W / 2, 972),
           "Every story above happened, or was first reported, on Thursday 19 November 2026.",
           font=SANS(15), fill=GREY, anchor="ma")
    d.text((W / 2, 994),
           "Sources: International Court of Justice  •  White House  •  Dow Jones  •  UN News  •  Reuters",
           font=SANS(14), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
