# -*- coding: utf-8 -*-
"""Fix absolute local image paths in the converted markdown."""
import re

MD = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training\docs\颂钵疗愈师培训7.0.md"
LOG = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_imgfix_log.txt"

try:
    with open(MD, "r", encoding="utf-8") as f:
        text = f.read()

    # absolute local prefix (backslashes and forward slashes variants) -> relative
    patterns = [
        (r'C:\\Users\\RunzeAI\\WorkBuddy\\疗愈天地\\singing-bowl-healer-training\\docs\\media/media/',
         'media/'),
        (r'C:/Users/RunzeAI/WorkBuddy/疗愈天地/singing-bowl-healer-training/docs/media/media/',
         'media/'),
    ]
    total = 0
    for pat, rep in patterns:
        text, n = re.subn(pat, rep, text)
        total += n

    # any remaining nested media/media/ references (from pre-flatten conversion)
    text, n2 = re.subn(r'(?<!/)media/media/', 'media/', text)
    total += n2

    with open(MD, "w", encoding="utf-8") as f:
        f.write(text)
    result = f"OK fixed={total} (nested={n2})"
except Exception:
    import traceback
    result = "ERROR: " + traceback.format_exc()

with open(LOG, "w", encoding="utf-8") as f:
    f.write(result)
