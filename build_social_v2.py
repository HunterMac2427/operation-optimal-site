from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

OUT = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/social-posts"
IMG = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/assets/images"
W, H = 1080, 1350  # Instagram portrait (4:5) — max feed real estate

DARK_GREEN = (26, 46, 26)
GOLD = (200, 168, 75)
WHITE = (255, 255, 255)
SOFT_WHITE = (230, 230, 225)
DIM_WHITE = (160, 160, 155)

def font(bold=False, size=48):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()

def heading_font(size=64):
    p = "C:/Windows/Fonts/impact.ttf"
    return ImageFont.truetype(p, size) if os.path.exists(p) else font(bold=True, size=size)

def georgia_font(size=32):
    p = "C:/Windows/Fonts/georgiab.ttf"
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    p2 = "C:/Windows/Fonts/georgia.ttf"
    return ImageFont.truetype(p2, size) if os.path.exists(p2) else font(bold=True, size=size)

def draw_centered(draw, text, fnt, fill, y, max_w=900, spacing=10):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            test = cur + " " + w if cur else w
            bb = draw.textbbox((0,0), test, font=fnt)
            if bb[2] - bb[0] > max_w:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
    for line in lines:
        if line == "":
            y += fnt.size // 2
            continue
        bb = draw.textbbox((0,0), line, font=fnt)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        draw.text(((W - tw)//2, y), line, fill=fill, font=fnt)
        y += th + spacing
    return y

def load_bg(filename, darken=0.35, blur=0):
    bg = Image.open(os.path.join(OUT, filename)).convert("RGB")
    bg = bg.resize((W, H), Image.LANCZOS)
    if blur > 0:
        bg = bg.filter(ImageFilter.GaussianBlur(radius=blur))
    if darken < 1.0:
        enhancer = ImageEnhance.Brightness(bg)
        bg = enhancer.enhance(darken)
    return bg

def load_book_photo(filename):
    img = Image.open(os.path.join(IMG, filename)).convert("RGBA")
    w, h = img.size
    # Crop to 4:5 from center
    target_ratio = W / H
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize((W, H), Image.LANCZOS)

def gold_line(draw, y, width=80):
    draw.rectangle([(W//2 - width//2, y), (W//2 + width//2, y+3)], fill=GOLD)

def add_bottom_bar(draw, text="OPERATION OPTIMAL  |  MAY 15"):
    # Semi-transparent bar at bottom
    draw.rectangle([(0, H-70), (W, H)], fill=(15, 25, 15))
    f = font(bold=True, size=16)
    bb = draw.textbbox((0,0), text, font=f)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, H-48), text, fill=GOLD, font=f)

def add_top_chip(draw, text):
    f = font(bold=True, size=14)
    bb = draw.textbbox((0,0), text, font=f)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    px, py = 16, 8
    x = (W - tw) // 2 - px
    y = 40
    draw.rounded_rectangle([(x, y), (x + tw + px*2, y + th + py*2)], radius=4, fill=(200,168,75,180), outline=None)
    draw.text((x + px, y + py), text, fill=DARK_GREEN, font=f)

# ============================================================
# HELPERS FOR SLIDE TYPES
# ============================================================

def make_scroll_stopper(filename, bg_file, big_text, sub_text):
    img = load_bg(bg_file, darken=0.25, blur=2)
    # Heavy dark overlay for text readability
    overlay = Image.new("RGBA", (W, H), (20, 35, 20, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Center the big text vertically
    hf = heading_font(size=100)
    y = draw_centered(draw, big_text, hf, WHITE, 380, max_w=950, spacing=8)
    gold_line(draw, y + 20, 100)

    sf = font(False, size=30)
    draw_centered(draw, sub_text, sf, SOFT_WHITE, y + 55, max_w=800)

    add_bottom_bar(draw)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  {filename}")

def make_chapter_slide(filename, bg_file, chapter_label, chapter_title, excerpt):
    img = load_bg(bg_file, darken=0.2, blur=4)
    overlay = Image.new("RGBA", (W, H), (20, 35, 20, 185))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Chapter label
    lf = font(bold=True, size=18)
    bb = draw.textbbox((0,0), chapter_label, font=lf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, 120), chapter_label, fill=GOLD, font=lf)

    gold_line(draw, 155, 60)

    # Title
    tf = heading_font(size=56)
    y = draw_centered(draw, chapter_title, tf, WHITE, 185, max_w=880)

    gold_line(draw, y + 15, 80)

    # Excerpt in italic-style serif
    ef = georgia_font(size=26)
    draw_centered(draw, excerpt, ef, SOFT_WHITE, y + 50, max_w=820, spacing=12)

    add_bottom_bar(draw)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  {filename}")

def make_quote_slide(filename, bg_file, quote, attribution):
    img = load_bg(bg_file, darken=0.2, blur=3)
    overlay = Image.new("RGBA", (W, H), (20, 35, 20, 180))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Large gold quotation marks
    qf = heading_font(size=200)
    bb = draw.textbbox((0,0), "\u201C", font=qf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, 80), "\u201C", fill=(200, 168, 75, 120), font=qf)

    # Quote text
    qfont = georgia_font(size=32)
    y = draw_centered(draw, quote, qfont, WHITE, 340, max_w=840, spacing=16)

    gold_line(draw, y + 25, 60)

    # Attribution
    af = font(bold=True, size=20)
    bb = draw.textbbox((0,0), attribution, font=af)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, y + 50), attribution, fill=GOLD, font=af)

    add_bottom_bar(draw)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  {filename}")

def make_book_cta_slide(filename, book_photo_file, top_text, cta_text):
    img = load_book_photo(book_photo_file)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Gradient overlay from bottom (stronger)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    gradient_h = H // 2
    for i in range(gradient_h):
        alpha = int(230 * (i / gradient_h))
        yy = H - gradient_h + i
        odraw.rectangle([(0, yy), (W, yy+1)], fill=(20, 35, 20, alpha))
    # Also slight top gradient
    for i in range(200):
        alpha = int(120 * (1 - i/200))
        odraw.rectangle([(0, i), (W, i+1)], fill=(20, 35, 20, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Top chip
    add_top_chip(draw, top_text)

    # Bottom CTA
    y = H - 220
    hf = heading_font(size=48)
    for line in ["AVAILABLE MAY 15"]:
        bb = draw.textbbox((0,0), line, font=hf)
        tw = bb[2] - bb[0]
        draw.text(((W-tw)//2, y), line, fill=WHITE, font=hf)
        y += bb[3] - bb[1] + 8

    gold_line(draw, y + 8, 80)

    sf = font(bold=True, size=22)
    bb = draw.textbbox((0,0), cta_text, font=sf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, y + 28), cta_text, fill=GOLD, font=sf)

    add_bottom_bar(draw, "operationoptimal.com  |  LINK IN BIO")
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  {filename}")


# ============================================================
# POST 1: PART I — Own Your Health
# ============================================================
print("POST 1: Part I — Own Your Health")

make_scroll_stopper("post1-slide1.jpg", "bg1.jpg",
    "NOBODY'S COMING\nTO SAVE YOU.",
    "Not your doctor. Not some miracle drug.\nIf you want to be healthy, it's on you.")

make_chapter_slide("post1-slide2.jpg", "bg4.jpg",
    "CHAPTER 1",
    "Own Your Own Health",
    "Our health is failing us because our healthcare has betrayed it.\n\nBig Pharma and Big Medicine celebrate our symptom suppression as success; normalizes our chronic fatigue as adulthood; and mistakes our over-medication for medicine.\n\nWe live in the greatest chronic illness crisis the world has ever seen, and modern medicine's answer is pills before progress.")

make_quote_slide("post1-slide3.jpg", "bg1.jpg",
    "If your health is your responsibility, that means you have the power to change it right now.\n\nToday.",
    "TOMO MARJANOVIC  |  OPERATION OPTIMAL")

make_quote_slide("post1-slide4.jpg", "bg4.jpg",
    "A healthy grocery list can cost around 40% less per trip than junk-food choices.\n\nDon't let the lie keep you broke and sick.",
    "CHAPTER 3  |  HACKING YOUR WAY TO HEALTH")

make_book_cta_slide("post1-slide5.jpg", "tomo-img_4601.jpg",
    "PART I: OWN YOUR HEALTH",
    "operationoptimal.com  |  Link in bio")


# ============================================================
# POST 2: PART II — Future of Medicine
# ============================================================
print("POST 2: Part II — Future of Medicine")

make_scroll_stopper("post2-slide1.jpg", "bg2.jpg",
    "THE FUTURE OF\nMEDICINE IS NOT\nA PILL.",
    "It's prevention. It's optimization.\nIt's taking back control.")

make_chapter_slide("post2-slide2.jpg", "bg2.jpg",
    "CHAPTER 8",
    "The Future of Medicine",
    "The future of medicine is hormone therapy. Because standard medicine has gone awry. It's become corrupt, dogmatic, and overfocused on symptom treatment rather than symptom prevention.\n\nThe future of medicine is prevention and holistic wellness; it's staving off disease and chronic illnesses before they happen.")

make_quote_slide("post2-slide3.jpg", "bg4.jpg",
    "This is not health care, it's disease management for profit.\n\nIt's the revolving door where you walk in with one problem, leave with a prescription, and come back six months later with two more.",
    "CHAPTER 8  |  THE FUTURE OF MEDICINE")

make_quote_slide("post2-slide4.jpg", "bg2.jpg",
    "You have the potential to live a longer, happier, and more fulfilled life.\n\nImagine that living to 100 years old is just within your reach.\n\nWhy not reach out and take it?",
    "CHAPTER 7  |  LONGEVITY & THE NEXT GENERATION")

make_book_cta_slide("post2-slide5.jpg", "tomo-img_4602.jpg",
    "PART II: THE SCIENCE",
    "operationoptimal.com  |  Link in bio")


# ============================================================
# POST 3: PART III — Wealth, Happiness, Legacy
# ============================================================
print("POST 3: Part III — Wealth, Happiness, Legacy")

make_scroll_stopper("post3-slide1.jpg", "bg5.jpg",
    "THE GREATEST\nWEALTH YOU WILL\nEVER HAVE IS\nYOUR HEALTH.",
    "Multiply that wealth. Start today.")

make_chapter_slide("post3-slide2.jpg", "bg4.jpg",
    "CHAPTER 10",
    "Turning Health\ninto Wealth",
    "It doesn't matter if you're a billionaire. If you're sick, all that matters is getting well again.\n\nWhen we are facing an illness, any illness, we very suddenly realize the value of our health. Wouldn't you trade all your money and all your success, just to live longer with your loved ones?")

make_quote_slide("post3-slide3.jpg", "bg5.jpg",
    "Never let a $5 task interfere with a $150,000 task.\n\nWe are habituated to underperforming. Our optimal selves should be our normal selves.",
    "CHAPTER 10  |  TURNING HEALTH INTO WEALTH")

make_quote_slide("post3-slide4.jpg", "bg4.jpg",
    "Every chapter in this book has pointed towards a single truth: you are the solution to your own problem.\n\nNo doctor, pill, or quick fix can replace the mindset that everything in your life begins with ownership.",
    "CONCLUSION  |  IT'S MY FAULT")

make_book_cta_slide("post3-slide5.jpg", "tomo-img_4603.jpg",
    "PART III: WEALTH & LEGACY",
    "operationoptimal.com  |  Link in bio")


# ============================================================
# POST 4: STATIC — Book Cover Announcement
# ============================================================
print("POST 4: Static — Book Announcement")

img = load_bg("bg4.jpg", darken=0.25, blur=3)
overlay = Image.new("RGBA", (W, H), (20, 35, 20, 160))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

# Place book cover centered
cover = Image.open(os.path.join(IMG, "book-cover.png")).convert("RGBA")
cover_h = 650
ratio = cover_h / cover.height
cover_w = int(cover.width * ratio)
cover = cover.resize((cover_w, cover_h), Image.LANCZOS)

# Add subtle shadow behind book
shadow = Image.new("RGBA", (cover_w + 30, cover_h + 30), (0,0,0,0))
sdraw = ImageDraw.Draw(shadow)
sdraw.rectangle([(15, 15), (cover_w+15, cover_h+15)], fill=(0,0,0,80))
shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
sx = (W - cover_w) // 2 - 15
img.paste(Image.alpha_composite(img.crop((sx, 100, sx+cover_w+30, 100+cover_h+30)).convert("RGBA"), shadow).convert("RGB"), (sx, 100))

cx = (W - cover_w) // 2
img.paste(cover, (cx, 115), cover)

draw = ImageDraw.Draw(img)

y = 810
hf = heading_font(size=54)
for line in ["OPERATION OPTIMAL", "OUT MAY 15"]:
    bb = draw.textbbox((0,0), line, font=hf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, y), line, fill=WHITE, font=hf)
    y += bb[3] - bb[1] + 10

gold_line(draw, y + 10, 100)

sf = georgia_font(size=24)
sub = "Health, Wellness, and Becoming Your Best You"
bb = draw.textbbox((0,0), sub, font=sf)
tw = bb[2] - bb[0]
draw.text(((W-tw)//2, y+35), sub, fill=SOFT_WHITE, font=sf)

af = font(bold=True, size=20)
auth = "TOMO MARJANOVIC"
bb = draw.textbbox((0,0), auth, font=af)
tw = bb[2] - bb[0]
draw.text(((W-tw)//2, y+75), auth, fill=GOLD, font=af)

add_bottom_bar(draw, "operationoptimal.com")
img.save(os.path.join(OUT, "post4-static-announcement.jpg"), "JPEG", quality=95)
print("  post4-static-announcement.jpg")


# ============================================================
# POST 5: STATIC — Launch Day (Book in Hand)
# ============================================================
print("POST 5: Static — Launch Day")

img = load_book_photo("tomo-img_4601.jpg").convert("RGB")
draw = ImageDraw.Draw(img)

# Strong gradient from bottom
overlay = Image.new("RGBA", (W, H), (0,0,0,0))
odraw = ImageDraw.Draw(overlay)
for i in range(H//2):
    alpha = int(240 * (i / (H//2)))
    yy = H - H//2 + i
    odraw.rectangle([(0, yy), (W, yy+1)], fill=(20, 35, 20, alpha))
for i in range(250):
    alpha = int(150 * (1 - i/250))
    odraw.rectangle([(0, i), (W, i+1)], fill=(20, 35, 20, alpha))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img)

add_top_chip(draw, "OUT NOW  |  MAY 15, 2026")

y = H - 300
hf = heading_font(size=64)
for line in ["IT'S HERE."]:
    bb = draw.textbbox((0,0), line, font=hf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, y), line, fill=WHITE, font=hf)
    y += bb[3] - bb[1] + 5

sf = heading_font(size=40)
for line in ["OPERATION OPTIMAL", "IS NOW AVAILABLE."]:
    bb = draw.textbbox((0,0), line, font=sf)
    tw = bb[2] - bb[0]
    draw.text(((W-tw)//2, y), line, fill=SOFT_WHITE, font=sf)
    y += bb[3] - bb[1] + 5

gold_line(draw, y + 10, 80)

cf = font(bold=True, size=22)
cta = "Grab your copy today"
bb = draw.textbbox((0,0), cta, font=cf)
tw = bb[2] - bb[0]
draw.text(((W-tw)//2, y + 30), cta, fill=GOLD, font=cf)

add_bottom_bar(draw, "operationoptimal.com  |  LINK IN BIO")
img.save(os.path.join(OUT, "post5-static-launch.jpg"), "JPEG", quality=95)
print("  post5-static-launch.jpg")

print(f"\nDone! All files in {OUT}")
