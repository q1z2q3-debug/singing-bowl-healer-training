# -*- coding: utf-8 -*-
"""Convert the singing bowl training docx to GitHub-flavored markdown."""
import os
import sys
import io
import pypandoc

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SRC = r"H:\009 培训学院\疗愈师培训\教材版本\教材 202304\颂钵疗愈师培训7.0（大字版）.docx"
PROJ = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training"
DOCS = os.path.join(PROJ, "docs")
MEDIA = os.path.join(DOCS, "media")
OUT = os.path.join(DOCS, "颂钵疗愈师培训7.0.md")

LOG = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_conv_log.txt"

os.makedirs(MEDIA, exist_ok=True)

try:
    out = pypandoc.convert_file(
        SRC,
        "gfm",
        format="docx",
        extra_args=[
            "--extract-media=" + MEDIA,
            "--wrap=none",
            "--markdown-headings=atx",
        ],
    )

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)

    lines = out.count("\n")
    size = os.path.getsize(OUT)
    imgs = out.count("](media/") + out.count("](./media/")
    media_files = []
    for root, _dirs, files in os.walk(MEDIA):
        for fn in files:
            media_files.append(os.path.join(root, fn))
    result = f"OK lines={lines} bytes={size} images_ref={imgs} media_files={len(media_files)}"
except Exception as e:
    import traceback
    result = "ERROR: " + traceback.format_exc()

with open(LOG, "w", encoding="utf-8") as f:
    f.write(result)
