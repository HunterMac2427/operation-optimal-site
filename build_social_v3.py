"""
OPERATION OPTIMAL — Social Media Campaign v3
5 posts (3 carousels + 2 static) for May 15 2026 launch

Brand: Dark green #1a2e1a, Gold #c8a84b, White
Tone: Bold, masculine, no-nonsense, premium health/wellness
Format: 1080x1350 (Instagram portrait 4:5)

Backgrounds:
  bg1 = Mountain summit at golden hour (Part I: personal power)
  bg2 = DNA helix science (Part II: medicine/science)
  bg4 = Dark green marble with gold veins (chapter slides, quotes)
  bg5 = Runner at dawn (Part III: wealth/performance)
  bg6 = Ocean waves crashing (raw power, quotes)
  bg7 = Forest path with light (journey, discovery)

Photos: tomo-img_4601/4602/4603 = hand holding book (no selfies)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

OUT = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/social-posts"
IMG = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/assets/images"
W, H = 1080, 1350

DARK_GREEN = (26, 46, 26)
GOLD = (200, 168, 75)
WHITE = (255, 255, 255)
SOFT = (220, 220, 215)
DIM = (140, 140, 135)

# Fonts
def f(bold=False, sz=48):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(p, sz)

def hf(sz=64):
    return ImageFont.truetype("C:/Windows/Fonts/impact.ttf", sz)

def gf(sz=32):
    for p in ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/georgia.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return f(bold=True, size=sz)

def wrap(draw, text, fnt, fill, y, mw=920, sp=10):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            t = cur + " " + w if cur else w
            if draw.textbbox((0,0), t, font=fnt)[2] > mw:
                lines.append(cur)
                cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
    for line in lines:
        if line == "":
            y += fnt.size // 2
            continue
        bb = draw.textbbox((0,0), line, font=fnt)
        draw.text(((W - bb[2] + bb[0])//2, y), line, fill=fill, font=fnt)
        y += bb[3] - bb[1] + sp
    return y

def bg(name, dark=0.3, blur=0):
    img = Image.open(os.path.join(OUT, name)).convert("RGB").resize((W, H), Image.LANCZOS)
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(img).enhance(dark)

def overlay(img, alpha=170):
    o = Image.new("RGBA", (W, H), (20, 35, 20, alpha))
    return Image.alpha_composite(img.convert("RGBA"), o).convert("RGB")

def gold_line(d, y, w=100):
    d.rectangle([(W//2 - w//2, y), (W//2 + w//2, y+4)], fill=GOLD)

def bottom_bar(d, text="OPERATION OPTIMAL  |  MAY 15"):
    d.rectangle([(0, H-65), (W, H)], fill=(12, 20, 12))
    bb = d.textbbox((0,0), text, font=f(True, 15))
    d.text(((W - bb[2] + bb[0])//2, H-43), text, fill=GOLD, font=f(True, 15))

def chip(d, text):
    fn = f(True, 14)
    bb = d.textbbox((0,0), text, font=fn)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    px, py = 18, 10
    x = (W - tw)//2 - px
    d.rounded_rectangle([(x, 35), (x+tw+px*2, 35+th+py*2)], radius=4, fill=GOLD)
    d.text((x+px, 35+py), text, fill=DARK_GREEN, font=fn)

def book_bg(photo):
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
# SCROLL STOPPER — big bold text, dramatic bg
# ============================================================
def stopper(fname, bgfile, big, sub):
    img = overlay(bg(bgfile, dark=0.3, blur=2), alpha=150)
    d = ImageDraw.Draw(img)
    y = wrap(d, big, hf(110), WHITE, 320, mw=980, sp=5)
    gold_line(d, y+15, 120)
    wrap(d, sub, f(False, 32), SOFT, y+50, mw=850)
    bottom_bar(d)
    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")

# ============================================================
# CHAPTER SLIDE — label, big title, excerpt
# ============================================================
def chapter(fname, bgfile, label, title, body):
    img = overlay(bg(bgfile, dark=0.22, blur=4), alpha=185)
    d = ImageDraw.Draw(img)
    # Label
    bb = d.textbbox((0,0), label, font=f(True, 20))
    d.text(((W-bb[2]+bb[0])//2, 100), label, fill=GOLD, font=f(True, 20))
    gold_line(d, 135, 60)
    # Title
    y = wrap(d, title, hf(60), WHITE, 170, mw=900, sp=5)
    gold_line(d, y+12, 80)
    # Body — centered, readable
    wrap(d, body, gf(27), SOFT, y+45, mw=840, sp=14)
    bottom_bar(d)
    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")

# ============================================================
# QUOTE SLIDE — big quotation mark, quote, attribution
# ============================================================
def quote(fname, bgfile, text, attr):
    img = overlay(bg(bgfile, dark=0.22, blur=3), alpha=175)
    d = ImageDraw.Draw(img)
    # Gold quote mark
    d.text(((W-180)//2, 70), "\u201C", fill=(160,135,60), font=hf(220))
    # Quote
    y = wrap(d, text, gf(34), WHITE, 340, mw=860, sp=16)
    gold_line(d, y+25, 70)
    # Attribution
    bb = d.textbbox((0,0), attr, font=f(True, 20))
    d.text(((W-bb[2]+bb[0])//2, y+50), attr, fill=GOLD, font=f(True, 20))
    bottom_bar(d)
    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")

# ============================================================
# BOOK CTA SLIDE — book photo bg, big bold CTA text
# ============================================================
def book_cta(fname, photo, part_label):
    img = book_bg(photo)
    d = ImageDraw.Draw(img)
    # Gradient from bottom (very strong)
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    od = ImageDraw.Draw(ov)
    for i in range(H*2//3):
        a = int(245 * (i / (H*2//3)))
        yy = H - H*2//3 + i
        od.rectangle([(0, yy), (W, yy+1)], fill=(20, 35, 20, a))
    for i in range(200):
        a = int(130 * (1-i/200))
        od.rectangle([(0,i), (W,i+1)], fill=(20, 35, 20, a))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)

    chip(d, part_label)

    # BIG CTA text at bottom
    y = H - 340
    wrap(d, "AVAILABLE", hf(80), WHITE, y, mw=980)
    y2 = y + 85
    wrap(d, "MAY 15", hf(100), GOLD, y2, mw=980)
    y3 = y2 + 110
    gold_line(d, y3, 100)
    wrap(d, "operationoptimal.com", f(True, 28), WHITE, y3+25, mw=800)

    bottom_bar(d, "LINK IN BIO")
    img.save(os.path.join(OUT, fname), "JPEG", quality=95)
    print(f"  {fname}")


# ============================================================
# BUILD ALL 5 POSTS
# ============================================================

# POST 1: PART I — Own Your Health
print("POST 1: Part I")
stopper("post1-slide1.jpg", "bg1.jpg",
    "NOBODY'S COMING\nTO SAVE YOU.",
    "Not your doctor. Not some miracle drug.\nIf you want to be healthy, it's on you.")

chapter("post1-slide2.jpg", "bg4.jpg",
    "CHAPTER 1",
    "Own Your Own Health",
    "Our health is failing us because our healthcare has betrayed it.\n\nBig Pharma and Big Medicine celebrate our symptom suppression as success; normalizes our chronic fatigue as adulthood; and mistakes our over-medication for medicine.\n\nWe live in the greatest chronic illness crisis the world has ever seen, and modern medicine's answer is pills before progress.")

quote("post1-slide3.jpg", "bg6.jpg",
    "If your health is your responsibility, that means you have the power to change it right now.\n\nToday.",
    "TOMO MARJANOVIC  |  OPERATION OPTIMAL")

quote("post1-slide4.jpg", "bg7.jpg",
    "Hardship is resistance training, and the muscle it builds is your brain.\n\nLean into the hurt to get to the healthy.",
    "CHAPTER 4  |  THE TOLL OF STRESS")

book_cta("post1-slide5.jpg", "tomo-img_4601.jpg", "PART I: OWN YOUR HEALTH")


# POST 2: PART II — The Science
print("POST 2: Part II")
stopper("post2-slide1.jpg", "bg2.jpg",
    "THE FUTURE OF\nMEDICINE IS NOT\nA PILL.",
    "It's prevention. It's optimization.\nIt's taking back control.")

chapter("post2-slide2.jpg", "bg4.jpg",
    "CHAPTER 8",
    "The Future of Medicine",
    "The future of medicine is hormone therapy. Because standard medicine has gone awry. It's become corrupt, dogmatic, and overfocused on symptom treatment rather than symptom prevention.\n\nThe future of medicine is prevention and holistic wellness; it's staving off disease and chronic illnesses before they happen.")

quote("post2-slide3.jpg", "bg2.jpg",
    "This is not health care, it's disease management for profit.\n\nIt's the revolving door where you walk in with one problem, leave with a prescription, and come back six months later with two more.",
    "CHAPTER 8  |  THE FUTURE OF MEDICINE")

quote("post2-slide4.jpg", "bg6.jpg",
    "You have the potential to live a longer, happier, and more fulfilled life.\n\nImagine that living to 100 years old is just within your reach.\n\nWhy not reach out and take it?",
    "CHAPTER 7  |  LONGEVITY")

book_cta("post2-slide5.jpg", "tomo-img_4602.jpg", "PART II: THE SCIENCE")


# POST 3: PART III — Wealth, Happiness, Legacy
print("POST 3: Part III")
stopper("post3-slide1.jpg", "bg5.jpg",
    "THE GREATEST\nWEALTH YOU WILL\nEVER HAVE IS\nYOUR HEALTH.",
    "Multiply that wealth. Start today.")

chapter("post3-slide2.jpg", "bg4.jpg",
    "CHAPTER 10",
    "Turning Health\ninto Wealth",
    "It doesn't matter if you're a billionaire. If you're sick, all that matters is getting well again.\n\nWhen we are facing an illness, any illness, we very suddenly realize the value of our health. Wouldn't you trade all your money and all your success, just to live longer with your loved ones?")

quote("post3-slide3.jpg", "bg1.jpg",
    "Never let a $5 task interfere with a $150,000 task.\n\nWe are habituated to underperforming.\nOur optimal selves should be our normal selves.",
    "CHAPTER 10  |  HEALTH INTO WEALTH")

quote("post3-slide4.jpg", "bg7.jpg",
    "You are the solution to your own problem.\n\nNo doctor, pill, or quick fix can replace the mindset that everything in your life begins with ownership.",
    "CONCLUSION  |  IT'S MY FAULT")

book_cta("post3-slide5.jpg", "tomo-img_4603.jpg", "PART III: WEALTH & LEGACY")


# POST 4: STATIC — Book Announcement
print("POST 4: Static Announcement")
img = overlay(bg("bg4.jpg", dark=0.25, blur=3), alpha=150)

# Book cover
cover = Image.open(os.path.join(IMG, "book-cover.png")).convert("RGBA")
ch = 620
cw = int(cover.width * (ch / cover.height))
cover = cover.resize((cw, ch), Image.LANCZOS)

# Shadow
shadow = Image.new("RGBA", (cw+40, ch+40), (0,0,0,0))
ImageDraw.Draw(shadow).rectangle([(20,20),(cw+20,ch+20)], fill=(0,0,0,60))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
sx = (W-cw)//2 - 20
img.paste(Image.alpha_composite(img.crop((sx,80,sx+cw+40,80+ch+40)).convert("RGBA"), shadow).convert("RGB"), (sx,80))
img.paste(cover, ((W-cw)//2, 95), cover)

d = ImageDraw.Draw(img)
y = 770
wrap(d, "OPERATION OPTIMAL", hf(60), WHITE, y, mw=950)
y2 = y + 75
wrap(d, "OUT MAY 15", hf(70), GOLD, y2, mw=950)
y3 = y2 + 90
gold_line(d, y3, 120)
wrap(d, "Health, Wellness, and\nBecoming Your Best You", gf(28), SOFT, y3+30, mw=800)
wrap(d, "TOMO MARJANOVIC", f(True, 22), GOLD, y3+110, mw=800)
bottom_bar(d, "operationoptimal.com")
img.save(os.path.join(OUT, "post4-static-announcement.jpg"), "JPEG", quality=95)
print("  post4-static-announcement.jpg")


# POST 5: STATIC — Launch Day
print("POST 5: Static Launch")
img = book_bg("tomo-img_4601.jpg")
ov = Image.new("RGBA", (W, H), (0,0,0,0))
od = ImageDraw.Draw(ov)
for i in range(H*3//4):
    a = int(250 * (i / (H*3//4)))
    yy = H - H*3//4 + i
    od.rectangle([(0,yy),(W,yy+1)], fill=(20,35,20,a))
for i in range(250):
    a = int(140*(1-i/250))
    od.rectangle([(0,i),(W,i+1)], fill=(20,35,20,a))
img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
d = ImageDraw.Draw(img)
chip(d, "OUT NOW  |  MAY 15, 2026")

y = H - 400
wrap(d, "IT'S HERE.", hf(90), WHITE, y, mw=980)
y2 = y + 100
wrap(d, "OPERATION OPTIMAL\nIS NOW AVAILABLE.", hf(55), SOFT, y2, mw=950, sp=5)
y3 = y2 + 130
gold_line(d, y3, 100)
wrap(d, "GRAB YOUR COPY TODAY", f(True, 30), GOLD, y3+25, mw=800)
bottom_bar(d, "operationoptimal.com  |  LINK IN BIO")
img.save(os.path.join(OUT, "post5-static-launch.jpg"), "JPEG", quality=95)
print("  post5-static-launch.jpg")

print(f"\nAll done! Files in {OUT}")
