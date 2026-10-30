# -*- coding: utf-8 -*-
import re, os

OUT = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_toc_log.txt"
base = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training"
md = os.path.join(base, "docs", "颂钵疗愈师培训7.0.md")

def p(*a):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(" ".join(str(x) for x in a) + "\n")
open(OUT, "w", encoding="utf-8").close()

def slug(content):
    s = content.strip().lower()
    s = re.sub(r'[^\w一-鿿㐀-䶿\s\-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

seen = {}
def get(content):
    b = slug(content)
    if b not in seen:
        seen[b] = 0
        return b
    seen[b] += 1
    return "%s-%d" % (b, seen[b])

t = open(md, encoding="utf-8").read()
lines = t.split("\n")

# if a TOC already exists, remove it first (idempotent safety)
if any(l.strip() == "## 目录" for l in lines):
    # find region from ## 目录 to next H1 (single # )
    ts = te = None
    for i, l in enumerate(lines):
        if ts is None and l.strip() == "## 目录":
            ts = i
        if ts is not None and re.match(r'^# ', l):
            te = i
            break
    if ts is not None and te is not None:
        del lines[ts:te]
        p("removed_existing_toc", ts, te)

toc = ["## 目录", ""]
for l in lines:
    m = re.match(r'^(#{1,6})\s+(.*)$', l)
    if not m:
        continue
    content = m.group(2).strip()
    if content == "目录":
        continue
    if content in ("本章学习目标", "章节小结", "思考题"):
        continue
    anchor = get(content)
    level = len(m.group(1))
    indent = "  " * (level - 1)
    toc.append("%s- [%s](#%s)" % (indent, content, anchor))

new_toc = "\n".join(toc) + "\n"
lines[0:0] = new_toc.rstrip("\n").split("\n") + [""]
open(md, "w", encoding="utf-8").write("\n".join(lines))

p("toc_entries", len([x for x in toc if x.strip().startswith("- ")]))
p("DONE")
