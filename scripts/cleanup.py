# -*- coding: utf-8 -*-
"""Clean up converted markdown: fix TOC, heading spaces, remove artifacts."""
import re
import io
import sys

MD = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\docs\颂钵疗愈师培训7.0.md"
LOG = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_clean_log.txt"

try:
    with open(MD, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.split("\n")
    out = []
    stats = {"toc_fixed": 0, "space_fixed": 0, "blank_squeezed": 0}

    toc_re = re.compile(
        r"^\[(?P<title>.+?)\s*\[\d+\]\(#[^)]*\)\]\(#[^)]*\)\s*$"
    )
    prev_blank = False
    for ln in lines:
        s = ln.rstrip()

        # TOC entries: [title [page](#a)](#a)  ->  - [title](#a)
        m = toc_re.match(s)
        if m:
            title = m.group("title").strip()
            # extract inner anchor of the inner link
            inner = re.search(r"\[\d+\]\((#[^)]*)\)", s)
            anchor = inner.group(1) if inner else ""
            s = f"- [{title}](#{anchor.lstrip('#')})"
            stats["toc_fixed"] += 1

        # collapse multiple spaces after heading marks
        new = re.sub(r"^(#{1,6})\s{2,}", r"\1 ", s)
        if new != s:
            stats["space_fixed"] += 1
            s = new

        # squeeze 3+ consecutive blank lines to 1 blank
        if s.strip() == "":
            if prev_blank:
                stats["blank_squeezed"] += 1
                continue
            prev_blank = True
        else:
            prev_blank = False

        out.append(s)

    with open(MD, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    result = "OK " + str(stats) + f" lines={len(out)}"
except Exception:
    import traceback
    result = "ERROR: " + traceback.format_exc()

with open(LOG, "w", encoding="utf-8") as f:
    f.write(result)
