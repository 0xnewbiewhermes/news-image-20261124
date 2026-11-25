"""Renders the data-driven front page for news-image-20261124.

Reads tools/stories.json (leads with illustrations, plus a list of one-line
items), draws the page with the scene and map helpers in make_image.py, and
writes entry.png at the repository root. It also rewrites the sources table
in README.md between the markers <!-- sources:start --> and <!-- sources:end -->.

Run from anywhere:  python tools/render_front_page.py
"""
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_image as base  # noqa: E402  (scene drawing and map helpers)

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")
README = os.path.join(ROOT, "README.md")
DATA = os.path.join(HERE, "stories.json")

SCENES = {
    "ukraine": base.scene_ukraine, "bangladesh": base.scene_bangladesh, "gaza": base.scene_gaza,
    "turkey": base.scene_turkey, "afcon": base.scene_afcon, "colombia": base.scene_colombia,
    "japan": base.scene_japan, "korea": base.scene_korea,
}
base.SCENES = SCENES

W, H, SS = base.W, base.H, base.SS
INK, PANEL, PAPER, RED, MUTED = base.INK, base.PANEL, base.PAPER, base.RED, base.MUTED
WHITE = base.WHITE

# Map band: full width, 180 px tall, below the numbers strip.
base.MAP_Y, base.MAP_H = 236, 180

# Short one-line texts for the list (full titles stay in stories.json for the README).
SHORT = {
    12: "Australia tech law: fines up to 5% of revenue",
    14: "Houthis advance toward Aden; forces dig in",
    19: "Bitcoin below $60,000; ETF outflows hit a record",
    20: "Solomons scraps China pact for Australia treaty",
    21: "Cameroon separatist pleads not guilty in Oslo",
    22: "Amnesty urges probe of Alamata shelling",
    23: "Garment workers clash with police over pay",
    25: "Latvia: Ukraine war may reach tipping point",
    26: "Norway in dialogue with Ukraine on stability",
    27: "Microsoft declares 'Code Red' after outage",
    29: "Appeals court renews Trump hush-money bid",
    30: "Puerto Rico's Jennifer Barreto is Miss Universe",
}


def tag_of(item):
    return "C" if len(item["sources"]) >= 2 else "R"


def sources_table(leads, items):
    rows = ["| # | Item | Tag | Sources (outlet, date, link) |", "|---|---|---|---|"]
    for it in leads + items:
        srcs = "; ".join(f"{s['outlet']}, {s['when']}: {s['url']}" for s in it["sources"])
        title = it.get("title", it.get("text", "")).replace("|", "/")
        rows.append(f"| {it['n']} | {title} | {tag_of(it)} | {srcs} |")
    return "\n".join(rows)


def write_readme(leads, items):
    if not os.path.exists(README):
        return
    text = open(README, encoding="utf-8").read()
    start, end = "<!-- sources:start -->", "<!-- sources:end -->"
    if start not in text or end not in text:
        return
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    block = start + "\n\n" + sources_table(leads, items) + "\n\n" + end
    open(README, "w", encoding="utf-8").write(head + block + tail)


def paste_fit(img, scene, x, y, w, h):
    base.paste_scene(img, scene, x, y, w=w, h=h)


def draw_lead(d, img, lead, x, y, pw=238, ph=124):
    base.rect(d, x, y, x + pw, y + ph, fill=PANEL, outline=INK, width=2)
    paste_fit(img, base.SCENES[lead["scene"]], x + 6, y + 6, 226, 56)
    base.text(d, x + 8, y + 66, lead["keyword"], base.font("sans_b", 18))
    base.text(d, x + 8, y + 92, lead["detail"], base.fit_font("sans", lead["detail"], 222, 15, 12))
    base.ell(d, x + pw - 30, y + 66, x + pw - 10, y + 86, fill=RED, outline=WHITE, width=1)
    base.text(d, x + pw - 20, y + 76, str(lead["n"]), base.font("sans_b", 13), fill=WHITE, anchor="mm")
    t = tag_of(lead)
    base.rect(d, x + pw - 58, y + 66, x + pw - 36, y + 86, fill=INK if t == "C" else PANEL, outline=INK, width=1)
    base.text(d, x + pw - 47, y + 76, t, base.font("sans_b", 13), fill=WHITE if t == "C" else INK, anchor="mm")


ABBR = {
    "AP": "AP", "Reuters": "RTR", "BBC": "BBC", "BBC Sport": "BBC", "Al Jazeera": "AJ",
    "AFP (copy via NAMPA)": "AFP", "CNN": "CNN", "New York Times": "NYT", "Washington Post": "WaPo",
    "USA Today": "USAT", "Pasquines": "PQ", "Africanews": "AFRI", "ABC (Australia)": "ABC",
    "Sanofi (press release)": "SANOFI", "Bloomberg": "BBG", "CNBC": "CNBC", "The Motley Fool": "FOOL",
    "CoinDesk": "CD",
}


def source_label(item):
    names = [ABBR.get(s["outlet"], s["outlet"][:6].upper()) for s in item["sources"][:2]]
    return "+".join(names)


def draw_item(d, item, x, y, width=488):
    base.text(d, x, y, str(item["n"]), base.font("sans_b", 15))
    base.text(d, x + 30, y + 2, item["region"], base.font("sans_b", 11), fill=MUTED)
    label = source_label(item)
    badge_w = base.font("sans_b", 11).getlength(label) / SS + 12
    text = SHORT.get(item["n"], item.get("text", ""))
    max_w = width - 104 - badge_w - 10
    base.text(d, x + 104, y, text, base.fit_font("sans", text, max_w, 15, 12))
    t = tag_of(item)
    bx, by = x + width - badge_w, y - 1
    base.rect(d, bx, by, x + width, by + 18, fill=INK if t == "C" else PANEL, outline=INK, width=1)
    base.text(d, bx + badge_w / 2, by + 9, label, base.font("sans_b", 11),
              fill=WHITE if t == "C" else INK, anchor="mm")


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    leads, items = data["leads"], data["list"]
    count = len(leads) + len(items)
    c_count = sum(1 for it in leads + items if tag_of(it) == "C")
    r_count = count - c_count
    regions = {it["region"] for it in leads + items}

    img = Image.new("RGB", (W * SS, H * SS), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    base.rect(d, 24, 22, 1000, 25, fill=INK)
    base.text(d, 24, 34, "THE WORLD IN ONE DAY", base.font("sans_b", 22), fill=RED)
    base.text(d, 1000, 34, "24.11.2026", base.font("sans_b", 22), fill=INK, anchor="ra")
    base.text(d, 24, 50, data["date"], base.fit_font("serif_b", data["date"], 976, 76, 40))
    sub = f"{count} stories, each dated 24 November 2026 and sourced to named outlets"
    base.text(d, 24, 136, sub, base.fit_font("sans", sub, 976, 20, 14))
    base.rect(d, 24, 164, 1000, 167, fill=INK)

    # numbers strip
    tiles = [(str(count), "stories"), (str(len(regions)), "regions"),
             (str(c_count), "with 2+ outlets"), (str(r_count), "with one outlet")]
    tw = (976 - 3 * 8) / 4
    for i, (num, label) in enumerate(tiles):
        x = 24 + i * (tw + 8)
        base.rect(d, x, 176, x + tw, 224, fill=PANEL, outline=INK, width=1)
        base.text(d, x + 12, 200, num, base.font("serif_b", 30), anchor="lm")
        nw = base.font("serif_b", 30).getlength(num) / SS
        base.text(d, x + 12 + nw + 8, 200, label, base.font("sans_b", 16), anchor="lm")

    # map band with pins for the leads
    base.draw_map(img)
    base.rect(d, base.MAP_X + 6, base.MAP_Y + 6, base.MAP_X + 226, base.MAP_Y + 30, fill=PANEL)
    base.text(d, base.MAP_X + 14, base.MAP_Y + 9, "WHERE IT HAPPENED", base.font("sans_b", 18))
    for lead in leads:
        base.pin(d, lead["n"], lead["lon"], lead["lat"])

    # lead cards: 4 per row, two rows
    cols = [24, 270, 516, 762]
    rows = [426, 558]
    for i, lead in enumerate(leads):
        draw_lead(d, img, lead, cols[i % 4], rows[i // 4])

    # the list: two columns
    base.text(d, 24, 694, f"ALSO ON THE DAY: {len(items)} MORE, BY REGION", base.font("sans_b", 18))
    base.rect(d, 24, 718, 1000, 719, fill=INK)
    half = (len(items) + 1) // 2
    for k, item in enumerate(items):
        col, row = (0, k) if k < half else (1, k - half)
        x = 24 if col == 0 else 524
        draw_item(d, item, x, 728 + row * 22.5, width=476)

    # date check box: what was left out as earlier news, and how to read the tags
    base.rect(d, 24, 978, 1000, 1018, fill=PANEL, outline=INK, width=1)
    base.text(d, 32, 983, "DATE CHECK  Left out as earlier news: Hormuz tanker claim (Mon 23 Nov), Libya ship attack (22 Nov),",
              base.fit_font("sans", "DATE CHECK  Left out as earlier news: Hormuz tanker claim (Mon 23 Nov), Libya ship attack (22 Nov),", 960, 14, 11))
    base.text(d, 32, 1000, "Trump executions order (23 Nov), Huang back at Nvidia (23 Nov), Estonia threat (23 Nov).  C = 2+ outlets, R = 1 outlet.",
              base.fit_font("sans", "Trump executions order (23 Nov), Huang back at Nvidia (23 Nov), Estonia threat (23 Nov).  C = 2+ outlets, R = 1 outlet.", 960, 14, 11))

    img = img.resize((W, H), Image.Resampling.LANCZOS)
    img.save(OUT, format="PNG", optimize=True)
    write_readme(leads, items)
    print("wrote", OUT, os.path.getsize(OUT), "bytes;", count, "stories;", c_count, "C;", r_count, "R")


if __name__ == "__main__":
    main()
