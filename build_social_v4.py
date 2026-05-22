"""
OPERATION OPTIMAL — Social v4 (Daily Stoic style)
Dark cinematic bookends (slides 1+5) + warm book-page middle (slides 2-4)
MASSIVE text. True vertical centering. No small text anywhere.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os, random, math

OUT = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/social-posts"
IMG = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/assets/images"
W, H = 1080, 1350

# Colors
DARK = (26, 46, 26)
GOLD = (200, 168, 75)
WHITE = (255, 255, 255)
CREAM = (240, 232, 216)
WARM_DARK = (58, 48, 38)
BOOK_BLACK = (35, 30, 25)

# Fonts
def impact(sz): return ImageFont.truetype("C:/Windows/Fonts/impact.ttf", sz)
def arial_b(sz): return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", sz)
def arial(sz): return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", sz)
def georgia_b(sz):
    p = "C:/Windows/Fonts/georgiab.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else arial_b(sz)
def georgia(sz):
    p = "C:/Windows/Fonts/georgia.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else arial(sz)
def times_b(sz):
    p = "C:/Windows/Fonts/timesbd.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else georgia_b(sz)
def times(sz):
    p = "C:/Windows/Fonts/times.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else georgia(sz)

def wrap_lines(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            t = cur + " " + w if cur else w
            if draw.textbbox((0,0), t, font=fnt)[2] > max_w:
                lines.append(cur)
                cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
    return lines

def measure_block(draw, lines, fnt, sp=10):
    total = 0
    for line in lines:
        if line == "":
            total += fnt.size // 2
        else:
            bb = draw.textbbox((0,0), line, font=fnt)
            total += (bb[3] - bb[1]) + sp
    return total

def draw_block(draw, lines, fnt, fill, y, sp=10):
    for line in lines:
        if line == "":
            y += fnt.size // 2
            continue
        bb = draw.textbbox((0,0), line, font=fnt)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        draw.text(((W - tw)//2, y), line, fill=fill, font=fnt)
        y += th + sp
    return y

def gold_line(d, y, w=100):
    pass  # removed — was overlapping text

def gold_corners(d, margin=40, length=60, thickness=3, fill=GOLD):
    """Draw L-shaped gold corner ornaments on all 4 corners"""
    # Top-left
    d.rectangle([(margin, margin), (margin+length, margin+thickness)], fill=fill)
    d.rectangle([(margin, margin), (margin+thickness, margin+length)], fill=fill)
    # Top-right
    d.rectangle([(W-margin-length, margin), (W-margin, margin+thickness)], fill=fill)
    d.rectangle([(W-margin-thickness, margin), (W-margin, margin+length)], fill=fill)
    # Bottom-left
    d.rectangle([(margin, H-margin-thickness), (margin+length, H-margin)], fill=fill)
    d.rectangle([(margin, H-margin-length), (margin+thickness, H-margin)], fill=fill)
    # Bottom-right
    d.rectangle([(W-margin-length, H-margin-thickness), (W-margin, H-margin)], fill=fill)
    d.rectangle([(W-margin-thickness, H-margin-length), (W-margin, H-margin)], fill=fill)

# ── Create clean book-page texture ──
def make_page_bg():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # Add subtle noise via Pillow
    import struct
    noise_img = Image.new("RGB", (W, H))
    pixels = []
    for _ in range(W * H):
        r = random.randint(-5, 5)
        pixels.append((CREAM[0]+r, CREAM[1]+r, CREAM[2]+r))
    noise_img.putdata(pixels)
    img = noise_img
    # Slight warm vignette
    vig = Image.new("RGBA", (W, H), (0,0,0,0))
    vd = ImageDraw.Draw(vig)
    cx, cy = W//2, H//2
    max_r = math.sqrt(cx**2 + cy**2)
    for r in range(int(max_r), 0, -2):
        alpha = int(40 * (r / max_r) ** 2)
        vd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=(80, 60, 40, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
    # Subtle warm tint
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.85)
    return img

def load_dark_bg(name, dark=0.3, blur=2):
    img = Image.open(os.path.join(OUT, name)).convert("RGB").resize((W, H), Image.LANCZOS)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    img = ImageEnhance.Brightness(img).enhance(dark)
    o = Image.new("RGBA", (W, H), (20, 35, 20, 155))
    return Image.alpha_composite(img.convert("RGBA"), o).convert("RGB")

def book_photo_bg(photo):
    img = Image.open(os.path.join(IMG, photo)).convert("RGBA")
    w, h = img.size
    tr = W/H
    cr = w/h
    if cr > tr:
        nw = int(h*tr)
        img = img.crop(((w-nw)//2, 0, (w+nw)//2, h))
    else:
        nh = int(w/tr)
        img = img.crop((0, (h-nh)//2, w, (h+nh)//2))
    return img.resize((W, H), Image.LANCZOS).convert("RGB")


# ============================================================
# SLIDE BUILDERS
# ============================================================

def slide_stopper(fname, bg_name, headline, subtitle):
    """Dark dramatic slide with MASSIVE centered headline"""
    img = load_dark_bg(bg_name, dark=0.28, blur=2)
    d = ImageDraw.Draw(img)

    # Measure headline to center vertically
    hfont = impact(140)
    h_lines = wrap_lines(d, headline, hfont, 960)
    sfont = arial(34)
    s_lines = wrap_lines(d, subtitle, sfont, 820)

    h_height = measure_block(d, h_lines, hfont, sp=5)
    s_height = measure_block(d, s_lines, sfont, sp=8)
    total = h_height + 40 + s_height  # 40 for gold line gap

    start_y = (H - total) // 2 - 30  # slight upward bias

    y = draw_block(d, h_lines, hfont, WHITE, start_y, sp=5)
    draw_block(d, s_lines, sfont, (210, 210, 205), y + 50, sp=8)
    gold_corners(d, margin=35, length=55, thickness=3)

    # Tiny bottom bar
    d.rectangle([(0, H-55), (W, H)], fill=(12, 20, 12))
    bf = arial_b(14)
    bt = "OPERATION OPTIMAL  |  OUT MAY 15"
    bb = d.textbbox((0,0), bt, font=bf)
    d.text(((W-bb[2]+bb[0])//2, H-38), bt, fill=GOLD, font=bf)

    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")


def slide_bookpage(fname, label, title, body):
    """Warm parchment book-page slide — Daily Stoic style"""
    img = make_page_bg()
    d = ImageDraw.Draw(img)

    # Thin dark green line at very top and bottom (book spine hint)
    d.rectangle([(0, 0), (W, 6)], fill=(80, 70, 55))
    d.rectangle([(0, H-6), (W, H)], fill=(80, 70, 55))

    # Label
    lf = arial_b(20)
    bb = d.textbbox((0,0), label, font=lf)
    d.text(((W-bb[2]+bb[0])//2, 80), label, fill=(140, 120, 90), font=lf)

    # Title — large bold serif
    tf = times_b(72)
    t_lines = wrap_lines(d, title, tf, 860)
    t_height = measure_block(d, t_lines, tf, sp=5)

    # Body — readable serif
    bf = times(30)
    b_lines = wrap_lines(d, body, bf, 820)
    b_height = measure_block(d, b_lines, bf, sp=14)

    # Center the title+body block vertically (below label)
    usable_top = 130
    usable_bottom = H - 100
    usable_h = usable_bottom - usable_top
    total = t_height + 35 + b_height  # 35 for divider gap
    start_y = usable_top + (usable_h - total) // 2

    y = draw_block(d, t_lines, tf, BOOK_BLACK, start_y, sp=5)

    draw_block(d, b_lines, bf, (55, 48, 40), y+45, sp=14)

    gold_corners(d, margin=40, length=50, thickness=2, fill=(170, 150, 115))

    # Bottom attribution
    af = arial(18)
    at = "OPERATION OPTIMAL  \u2014  TOMO MARJANOVIC"
    bb = d.textbbox((0,0), at, font=af)
    d.text(((W-bb[2]+bb[0])//2, H-60), at, fill=(160, 140, 110), font=af)

    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")


def slide_bookquote(fname, quote_text, attribution):
    """Parchment quote slide — big serif, centered"""
    img = make_page_bg()
    d = ImageDraw.Draw(img)

    d.rectangle([(0, 0), (W, 6)], fill=(80, 70, 55))
    d.rectangle([(0, H-6), (W, H)], fill=(80, 70, 55))

    # Big decorative quote mark
    qf = times_b(200)
    bb = d.textbbox((0,0), "\u201C", font=qf)
    tw = bb[2] - bb[0]
    d.text(((W-tw)//2, 100), "\u201C", fill=(180, 160, 130), font=qf)

    # Quote text — large serif, true vertical center
    qfont = times_b(44)
    q_lines = wrap_lines(d, quote_text, qfont, 820)
    q_height = measure_block(d, q_lines, qfont, sp=18)

    start_y = (H - q_height) // 2 + 20
    y = draw_block(d, q_lines, qfont, BOOK_BLACK, start_y, sp=18)

    # Attribution
    af = arial_b(20)
    bb = d.textbbox((0,0), attribution, font=af)
    d.text(((W-bb[2]+bb[0])//2, y+50), attribution, fill=(140, 120, 90), font=af)

    gold_corners(d, margin=40, length=50, thickness=2, fill=(170, 150, 115))

    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")


def slide_book_cta(fname, photo, part_label):
    """Book-in-hand photo with big bold CTA"""
    img = book_photo_bg(photo)
    d = ImageDraw.Draw(img)

    # Heavy gradient from bottom
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    for i in range(H*3//4):
        a = int(250 * (i / (H*3//4)))
        yy = H - H*3//4 + i
        od.rectangle([(0, yy), (W, yy+1)], fill=(20, 35, 20, a))
    for i in range(200):
        a = int(100*(1-i/200))
        od.rectangle([(0,i),(W,i+1)], fill=(20, 35, 20, a))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)

    # Gold chip at top
    cf = arial_b(14)
    bb = d.textbbox((0,0), part_label, font=cf)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    px, py = 18, 10
    x = (W-tw)//2 - px
    d.rounded_rectangle([(x, 35), (x+tw+px*2, 35+th+py*2)], radius=4, fill=GOLD)
    d.text((x+px, 35+py), part_label, fill=DARK, font=cf)

    # BIG CTA at bottom
    y = H - 430
    d.text(((W - d.textbbox((0,0), "AVAILABLE", font=impact(110))[2])//2, y),
           "AVAILABLE", fill=WHITE, font=impact(110))
    y += 125
    d.text(((W - d.textbbox((0,0), "MAY 15", font=impact(150))[2])//2, y),
           "MAY 15", fill=GOLD, font=impact(150))
    y += 165
    wf = arial_b(30)
    wt = "operationoptimal.com"
    bb = d.textbbox((0,0), wt, font=wf)
    d.text(((W-bb[2]+bb[0])//2, y), wt, fill=WHITE, font=wf)

    # Bottom bar
    d.rectangle([(0, H-55), (W, H)], fill=(12, 20, 12))
    bf = arial_b(16)
    bt = "LINK IN BIO"
    bb = d.textbbox((0,0), bt, font=bf)
    d.text(((W-bb[2]+bb[0])//2, H-40), bt, fill=GOLD, font=bf)

    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")


# ============================================================
# BUILD ALL 5 POSTS (17 slides)
# ============================================================

print("POST 1: Part I — Own Your Health")
slide_stopper("post1-slide1.jpg", "bg1.jpg",
    "NOBODY'S COMING\nTO SAVE YOU.",
    "Not your doctor. Not some miracle drug.\nIf you want to be healthy, it's on you.")

slide_bookpage("post1-slide2.jpg",
    "CHAPTER 1",
    "Own Your Own Health",
    "Our health is failing us because our healthcare has betrayed it.\n\nBig Pharma and Big Medicine celebrate our symptom suppression as success; normalizes our chronic fatigue as adulthood; and mistakes our over-medication for medicine.\n\nWe live in the greatest chronic illness crisis the world has ever seen, and modern medicine's answer is pills before progress.")

slide_bookquote("post1-slide3.jpg",
    "If your health is your responsibility, that means you have the power to change it right now.\n\nToday.",
    "TOMO MARJANOVIC")

slide_bookquote("post1-slide4.jpg",
    "Hardship is resistance training, and the muscle it builds is your brain.\n\nLean into the hurt to get to the healthy.",
    "CHAPTER 4: THE TOLL OF STRESS")

slide_book_cta("post1-slide5.jpg", "tomo-img_4601.jpg", "PART I: OWN YOUR HEALTH")


print("POST 2: Part II — The Science")
slide_stopper("post2-slide1.jpg", "bg6.jpg",
    "THE FUTURE OF\nMEDICINE IS NOT\nA PILL.",
    "It's prevention. It's optimization.\nIt's taking back control.")

slide_bookpage("post2-slide2.jpg",
    "CHAPTER 8",
    "The Future of Medicine",
    "The future of medicine is hormone therapy. Because standard medicine has gone awry.\n\nIt's become corrupt, dogmatic, and overfocused on symptom treatment rather than symptom prevention.\n\nThe future of medicine is prevention and holistic wellness; it's staving off disease and chronic illnesses before they happen.")

slide_bookquote("post2-slide3.jpg",
    "This is not health care, it's disease management for profit.\n\nThe revolving door where you walk in with one problem, leave with a prescription, and come back six months later with two more.",
    "CHAPTER 8: THE FUTURE OF MEDICINE")

slide_bookquote("post2-slide4.jpg",
    "You have the potential to live a longer, happier, and more fulfilled life.\n\nImagine that living to 100 is just within your reach.\n\nWhy not reach out and take it?",
    "CHAPTER 7: LONGEVITY")

slide_book_cta("post2-slide5.jpg", "tomo-img_4602.jpg", "PART II: THE SCIENCE")


print("POST 3: Part III — Wealth & Legacy")
slide_stopper("post3-slide1.jpg", "bg5.jpg",
    "THE GREATEST\nWEALTH YOU WILL\nEVER HAVE IS\nYOUR HEALTH.",
    "Multiply that wealth. Start today.")

slide_bookpage("post3-slide2.jpg",
    "CHAPTER 10",
    "Turning Health into Wealth",
    "It doesn't matter if you're a billionaire. If you're sick, all that matters is getting well again.\n\nWhen we are facing an illness, any illness, we very suddenly realize the value of our health.\n\nWouldn't you trade all your money and all your success, just to live longer with your loved ones?")

slide_bookquote("post3-slide3.jpg",
    "Never let a $5 task interfere with a $150,000 task.\n\nWe are habituated to underperforming. Our optimal selves should be our normal selves.",
    "CHAPTER 10: HEALTH INTO WEALTH")

slide_bookquote("post3-slide4.jpg",
    "You are the solution to your own problem.\n\nNo doctor, pill, or quick fix can replace the mindset that everything in your life begins with ownership.",
    "CONCLUSION: IT'S MY FAULT")

slide_book_cta("post3-slide5.jpg", "tomo-img_4603.jpg", "PART III: WEALTH & LEGACY")


print("POST 4: Static — Announcement")
img = load_dark_bg("bg4.jpg", dark=0.25, blur=3)
cover = Image.open(os.path.join(IMG, "book-cover.png")).convert("RGBA")
ch = 600
cw = int(cover.width * (ch / cover.height))
cover = cover.resize((cw, ch), Image.LANCZOS)
img.paste(cover, ((W-cw)//2, 100), cover)
d = ImageDraw.Draw(img)
y = 740
d.text(((W - d.textbbox((0,0), "OPERATION OPTIMAL", font=impact(70))[2])//2, y),
       "OPERATION OPTIMAL", fill=WHITE, font=impact(70))
y += 90
d.text(((W - d.textbbox((0,0), "OUT MAY 15", font=impact(95))[2])//2, y),
       "OUT MAY 15", fill=GOLD, font=impact(95))
y += 115
sf = georgia(28)
st = "Health, Wellness, and\nBecoming Your Best You"
for line in st.split("\n"):
    bb = d.textbbox((0,0), line, font=sf)
    d.text(((W-bb[2]+bb[0])//2, y+25), line, fill=(210,210,205), font=sf)
    y += 40
af = arial_b(22)
at = "TOMO MARJANOVIC"
bb = d.textbbox((0,0), at, font=af)
d.text(((W-bb[2]+bb[0])//2, y+45), at, fill=GOLD, font=af)
d.rectangle([(0, H-55), (W, H)], fill=(12, 20, 12))
bf = arial_b(14)
bt = "operationoptimal.com"
bb = d.textbbox((0,0), bt, font=bf)
d.text(((W-bb[2]+bb[0])//2, H-38), bt, fill=GOLD, font=bf)
gold_corners(d, margin=35, length=55, thickness=3)
img.save(os.path.join(OUT, "post4-static-announcement.jpg"), "JPEG", quality=95)
print("  post4-static-announcement.jpg")


print("POST 5: Static — Launch Day")
slide_book_cta("post5-static-launch.jpg", "tomo-img_4601.jpg", "OUT NOW  |  MAY 15, 2026")

print(f"\nAll 17 files rebuilt in {OUT}")
