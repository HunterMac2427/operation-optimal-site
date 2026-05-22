from PIL import Image, ImageDraw, ImageFont
import os

OUT = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/social-posts"
IMG = "C:/Users/Hmact/OneDrive/Desktop/Web Design/Operation Optimal/assets/images"
W, H = 1080, 1080

DARK_GREEN = (26, 46, 26)
GOLD = (200, 168, 75)
WHITE = (255, 255, 255)

def get_font(bold=False, size=48):
    p = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_heading_font(size=64):
    p = "C:/Windows/Fonts/impact.ttf"
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return get_font(bold=True, size=size)

def draw_wrapped(draw, text, font, fill, y_start, max_width=900, line_spacing=12):
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            test = current + " " + word if current else word
            bbox = draw.textbbox((0,0), test, font=font)
            if bbox[2] - bbox[0] > max_width:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)
    y = y_start
    for line in lines:
        if line == "":
            y += font.size // 2
            continue
        bbox = draw.textbbox((0,0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x, y), line, fill=fill, font=font)
        y += bbox[3] - bbox[1] + line_spacing
    return y

def make_text_slide(filename, top_label, heading, body, bottom_label="OPERATION OPTIMAL  |  TOMO MARJANOVIC"):
    img = Image.new("RGB", (W, H), DARK_GREEN)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(W//2 - 40, 60), (W//2 + 40, 64)], fill=GOLD)
    label_font = get_font(bold=True, size=20)
    if top_label:
        bbox = draw.textbbox((0,0), top_label, font=label_font)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, 85), top_label, fill=GOLD, font=label_font)
    heading_font = get_heading_font(size=52)
    heading_y = 140 if top_label else 100
    y = draw_wrapped(draw, heading, heading_font, WHITE, heading_y, max_width=880)
    draw.rectangle([(W//2 - 30, y+15), (W//2 + 30, y+19)], fill=GOLD)
    body_font = get_font(False, size=28)
    draw_wrapped(draw, body, body_font, (200, 200, 195), y + 50, max_width=860, line_spacing=10)
    bottom_font = get_font(bold=True, size=16)
    bbox = draw.textbbox((0,0), bottom_label, font=bottom_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-50), bottom_label, fill=(120,120,115), font=bottom_font)
    draw.rectangle([(W//2 - 40, H-70), (W//2 + 40, H-66)], fill=GOLD)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  Created {filename}")

def make_quote_slide(filename, quote, attribution="- TOMO MARJANOVIC"):
    img = Image.new("RGB", (W, H), DARK_GREEN)
    draw = ImageDraw.Draw(img)
    qm_font = get_heading_font(size=180)
    draw.text((80, 60), "\u201C", fill=(100, 84, 38), font=qm_font)
    quote_font = get_font(False, size=32)
    y = draw_wrapped(draw, quote, quote_font, WHITE, 260, max_width=840, line_spacing=14)
    attr_font = get_font(bold=True, size=22)
    bbox = draw.textbbox((0,0), attribution, font=attr_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, y+40), attribution, fill=GOLD, font=attr_font)
    draw.rectangle([(W//2 - 40, H-60), (W//2 + 40, H-56)], fill=GOLD)
    bottom_font = get_font(bold=True, size=16)
    label = "OPERATION OPTIMAL  |  MAY 15"
    bbox = draw.textbbox((0,0), label, font=bottom_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-40), label, fill=(120,120,115), font=bottom_font)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  Created {filename}")

def make_photo_slide(filename, photo_path, overlay_lines, sub_text=""):
    img = Image.open(photo_path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left+side, top+side))
    img = img.resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H), (0,0,0,0))
    odraw = ImageDraw.Draw(overlay)
    for i in range(H//3):
        alpha = int(220 * (i / (H//3)))
        yy = H - H//3 + i
        odraw.rectangle([(0, yy), (W, yy+1)], fill=(26, 46, 26, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    y = H - 200
    heading_font = get_heading_font(size=42)
    for line in overlay_lines:
        bbox = draw.textbbox((0,0), line, font=heading_font)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, y), line, fill=WHITE, font=heading_font)
        y += bbox[3] - bbox[1] + 8
    if sub_text:
        sub_font = get_font(False, size=24)
        bbox = draw.textbbox((0,0), sub_text, font=sub_font)
        tw = bbox[2] - bbox[0]
        draw.text(((W-tw)//2, y+10), sub_text, fill=GOLD, font=sub_font)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  Created {filename}")

def make_bold_slide(filename, big_text, sub_text, bottom_text="OPERATION OPTIMAL  |  MAY 15"):
    img = Image.new("RGB", (W, H), DARK_GREEN)
    draw = ImageDraw.Draw(img)
    big_font = get_heading_font(size=90)
    y = draw_wrapped(draw, big_text, big_font, WHITE, 250, max_width=900)
    draw.rectangle([(W//2 - 50, y+20), (W//2 + 50, y+26)], fill=GOLD)
    sub_font = get_font(False, size=28)
    draw_wrapped(draw, sub_text, sub_font, (200, 200, 195), y+60, max_width=800)
    bottom_font = get_font(bold=True, size=18)
    bbox = draw.textbbox((0,0), bottom_text, font=bottom_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H-50), bottom_text, fill=GOLD, font=bottom_font)
    img.save(os.path.join(OUT, filename), "JPEG", quality=95)
    print(f"  Created {filename}")

book_photo_1 = os.path.join(IMG, "tomo-img_4598.jpg")
book_photo_2 = os.path.join(IMG, "tomo-img_4599.jpg")
book_cover = os.path.join(IMG, "book-cover.png")

# === POST 1: CAROUSEL - PART I ===
print("POST 1: Part I Carousel")
make_bold_slide("post1-slide1.jpg",
    "NOBODY'S COMING\nTO SAVE YOU.",
    "Not your doctor. Not some miracle drug.\nIf you want to be healthy, it's on you.")

make_text_slide("post1-slide2.jpg",
    "CHAPTER 1",
    "Own Your Own Health",
    "Our health is failing us because our healthcare has betrayed it. Big Pharma and Big Medicine celebrate our symptom suppression as success; normalizes our chronic fatigue as adulthood; and mistakes our over-medication for medicine.\n\nWe live in the greatest chronic illness crisis the world has ever seen, and modern medicine's answer is pills before progress.")

make_quote_slide("post1-slide3.jpg",
    "If your health is your responsibility, that means you have the power to change it right now.\n\nToday.",
    "- TOMO MARJANOVIC, OPERATION OPTIMAL")

make_quote_slide("post1-slide4.jpg",
    "Stop eating fast food. Stop drinking soda. Go for walks. Those three things alone could change your entire life.\n\nThe recipe is easy. The difficulty is in doing the work.",
    "- CHAPTER 3: HACKING YOUR WAY TO HEALTH")

make_photo_slide("post1-slide5.jpg", book_photo_1,
    ["AVAILABLE MAY 15", "operationoptimal.com"],
    "Link in bio")

# === POST 2: CAROUSEL - PART II ===
print("POST 2: Part II Carousel")
make_bold_slide("post2-slide1.jpg",
    "THE FUTURE OF\nMEDICINE IS NOT\nA PILL.",
    "It's prevention. It's optimization.\nIt's taking back control.")

make_text_slide("post2-slide2.jpg",
    "CHAPTER 8",
    "The Future of Medicine",
    "The future of medicine is hormone therapy. Because standard medicine has gone awry. It's become corrupt, dogmatic, and overfocused on symptom treatment rather than symptom prevention.\n\nThe future of medicine is prevention and holistic wellness; it's staving off disease and chronic illnesses before they happen.")

make_quote_slide("post2-slide3.jpg",
    "This is not health care, it's disease management for profit.\n\nIt's the revolving door where you walk in with one problem, leave with a prescription, and come back six months later with two more.",
    "- CHAPTER 8: THE FUTURE OF MEDICINE")

make_quote_slide("post2-slide4.jpg",
    "You have the potential to live a longer, happier, and more fulfilled life.\n\nImagine that living to 100 years old is just within your reach.\n\nWhy not reach out and take it?",
    "- CHAPTER 7: LONGEVITY & THE NEXT GENERATION")

make_photo_slide("post2-slide5.jpg", book_photo_2,
    ["AVAILABLE MAY 15", "operationoptimal.com"],
    "Link in bio")

# === POST 3: CAROUSEL - PART III ===
print("POST 3: Part III Carousel")
make_bold_slide("post3-slide1.jpg",
    "THE GREATEST\nWEALTH YOU WILL\nEVER HAVE IS\nYOUR HEALTH.",
    "Multiply that wealth. Start today.")

make_text_slide("post3-slide2.jpg",
    "CHAPTER 10",
    "Turning Health into Wealth",
    "It doesn't matter if you're a billionaire. If you're sick, all that matters is getting well again.\n\nWhen we are facing an illness, any illness, we very suddenly realize the value of our health. Wouldn't you trade all your money and all your success, just to live longer with your loved ones?")

make_quote_slide("post3-slide3.jpg",
    "Never let a $5 task interfere with a $150,000 task.\n\nWe are habituated to underperforming. Our optimal selves should be our normal selves.",
    "- CHAPTER 10: TURNING HEALTH INTO WEALTH")

make_quote_slide("post3-slide4.jpg",
    "Every chapter in this book has pointed towards a single truth: you are the solution to your own problem.\n\nNo doctor, pill, or quick fix can replace the mindset that everything in your life begins with ownership.",
    "- CONCLUSION: IT'S MY FAULT")

make_photo_slide("post3-slide5.jpg", book_photo_1,
    ["AVAILABLE MAY 15", "operationoptimal.com"],
    "Link in bio")

# === POST 4: STATIC - Announcement ===
print("POST 4: Static Announcement")
img = Image.new("RGB", (W, H), DARK_GREEN)
draw = ImageDraw.Draw(img)
cover = Image.open(book_cover).convert("RGBA")
cover_h = 550
ratio = cover_h / cover.height
cover_w = int(cover.width * ratio)
cover = cover.resize((cover_w, cover_h), Image.LANCZOS)
cx = (W - cover_w) // 2
img.paste(cover, (cx, 120), cover)
draw = ImageDraw.Draw(img)
heading_font = get_heading_font(size=48)
y = 700
for line in ["OPERATION OPTIMAL", "OUT MAY 15"]:
    bbox = draw.textbbox((0,0), line, font=heading_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, y), line, fill=WHITE, font=heading_font)
    y += bbox[3] - bbox[1] + 12
draw.rectangle([(W//2 - 40, y+10), (W//2 + 40, y+14)], fill=GOLD)
sub_font = get_font(False, size=24)
sub = "Health, Wellness, and Becoming Your Best You"
bbox = draw.textbbox((0,0), sub, font=sub_font)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, y+35), sub, fill=(200,200,195), font=sub_font)
auth_font = get_font(bold=True, size=20)
auth = "TOMO MARJANOVIC"
bbox = draw.textbbox((0,0), auth, font=auth_font)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, y+75), auth, fill=GOLD, font=auth_font)
bottom_font = get_font(bold=True, size=16)
bl = "operationoptimal.com"
bbox = draw.textbbox((0,0), bl, font=bottom_font)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, H-40), bl, fill=(120,120,115), font=bottom_font)
img.save(os.path.join(OUT, "post4-static-announcement.jpg"), "JPEG", quality=95)
print("  Created post4-static-announcement.jpg")

# === POST 5: STATIC - Launch Day ===
print("POST 5: Static Launch Day")
make_photo_slide("post5-static-launch.jpg", book_photo_2,
    ["IT'S HERE.", "OPERATION OPTIMAL", "IS NOW AVAILABLE."],
    "operationoptimal.com  |  Link in bio")

print("\nDone! All 19 files created.")
