import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\assets\A_serene_minimalist_scene_of_s_2026-10-29T17-20-12.png"
OUT = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\assets\social-preview.png"
TW, TH = 1280, 640  # GitHub / OG social card ratio 1.91:1

img = Image.open(SRC).convert("RGB")
w, h = img.size
# center-crop to 2.0 ratio then resize
target_ratio = TW / TH  # 2.0
if w / h > target_ratio:
    new_w = int(h * target_ratio)
    left = (w - new_w) // 2
    img = img.crop((left, 0, left + new_w, h))
else:
    new_h = int(w / target_ratio)
    top = (h - new_h) // 2
    img = img.crop((0, top, w, top + new_h))
img = img.resize((TW, TH), Image.LANCZOS)

# darken slightly for text contrast
base = Image.new("RGB", (TW, TH), (0, 0, 0))
img = Image.blend(img, base, 0.18)

# bottom gradient overlay (darker at bottom)
grad = Image.new("L", (TW, TH), 0)
pix = grad.load()
for y in range(TH):
    v = int(120 * (y / TH) ** 1.6)  # stronger toward bottom
    for x in range(TW):
        pix[x, y] = v
overlay = Image.new("RGB", (TW, TH), (10, 8, 6))
img = Image.composite(overlay, img, grad)

d = ImageDraw.Draw(img)

def font(path, size, idx=0):
    return ImageFont.truetype(path, size, index=idx)

title_f = font(r"C:\Windows\Fonts\msyhbd.ttc", 60, 0)
sub_f = font(r"C:\Windows\Fonts\msyh.ttc", 30, 0)
small_f = font(r"C:\Windows\Fonts\msyh.ttc", 22, 0)

x = 70
y = 250
# title
d.text((x, y), "颂钵疗愈师培训 7.0（大字版）", font=title_f, fill=(255, 244, 222))
# subtitle
y2 = y + 78
d.text((x, y2), "免费开源 · 声音疗愈 / 音疗师培训教材", font=sub_f, fill=(230, 214, 180))
# small line
y3 = y2 + 46
d.text((x, y3), "Singing Bowl Healer Training 7.0  ·  CC BY-NC-SA 4.0", font=small_f, fill=(200, 188, 160))
# accent rule line
d.rectangle([x, y - 26, x + 120, y - 18], fill=(201, 162, 92))

img.save(OUT, "PNG")
print("saved", OUT, os.path.getsize(OUT))

# remove the long-named source to keep repo clean
try:
    os.remove(SRC)
    print("removed source")
except Exception as e:
    print("remove err", e)
