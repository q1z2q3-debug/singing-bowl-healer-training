# -*- coding: utf-8 -*-
"""Convert EMF media files to PNG for GitHub rendering."""
import os
import io
import sys
from PIL import Image

MEDIA = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\docs\media"
RAW = os.path.join(MEDIA, "emf_raw")
LOG = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_emf_log.txt"

os.makedirs(RAW, exist_ok=True)

results = []
try:
    emfs = [f for f in os.listdir(MEDIA) if f.lower().endswith(".emf")]
    for fn in emfs:
        src = os.path.join(MEDIA, fn)
        dst = os.path.join(MEDIA, fn[:-4] + ".png")
        try:
            im = Image.open(src)
            im.load()
            # cap width at 2000px to control size
            if im.width > 2000:
                h = int(im.height * 2000 / im.width)
                im = im.resize((2000, h), Image.LANCZOS)
            if im.mode in ("RGBA", "P", "CMYK"):
                im = im.convert("RGB")
            im.save(dst, "PNG", optimize=True)
            results.append(f"{fn}: OK png={os.path.getsize(dst)//1024}KB")
        except Exception as e:
            results.append(f"{fn}: FAIL {type(e).__name__} {e}")

    # move processed emf files into raw subfolder (keep originals out of git)
    moved = 0
    for fn in emfs:
        src = os.path.join(MEDIA, fn)
        if os.path.exists(src):
            os.replace(src, os.path.join(RAW, fn))
            moved += 1
    result = "OK\n" + "\n".join(results) + f"\nmoved_to_raw={moved}"
except Exception:
    import traceback
    result = "ERROR: " + traceback.format_exc()

with open(LOG, "w", encoding="utf-8") as f:
    f.write(result)
