# -*- coding: utf-8 -*-
import re, os

OUT = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_l1_log.txt"
base = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training"
md = os.path.join(base, "docs", "颂钵疗愈师培训7.0.md")
media = os.path.join(base, "docs", "media")

def p(*a):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(" ".join(str(x) for x in a) + "\n")

open(OUT, "w", encoding="utf-8").close()

t = open(md, encoding="utf-8").read()
lines = t.split("\n")

# locate TOC block
toc_start = toc_end = None
for i, l in enumerate(lines):
    if toc_start is None and l.strip() == "## 目录":
        toc_start = i
    if toc_start is not None and l.startswith("# 第一章 初识颂钵"):
        toc_end = i
        break
p("toc_start", toc_start, "toc_end", toc_end)

# ---- heading explicit renames (chapter/section numbers + numbering fixes) ----
rename_map = {
    "# 理论课题": "# 第二章 理论课题",
    "# 自然疗法（初中高）": "# 第五章 自然疗法（初中高）",
    "## 振动基础（初中高）": "## 第二节 振动基础（初中高）",
    "## 世界观": "## 第二节 世界观",
    "## 价值观": "## 第三节 价值观",
    "## 水晶": "## 第六节 水晶",
    "## 第九节 香道": "## 第八节 香道",
    "## 冥想": "## 第九节 冥想",
    "## 气功": "## 第十节 气功",
    "## 其他": "## 第十一节 其他",
    "### 4.3.3 本自｜具足": "### 4.1.3 本自｜具足",
    "#### 另外根据疗愈场所的面积进行尺寸的选择，大场地，选择满月钵，颜色适合深色为主，小场合，适合小型满月钵，尺寸不宜太过大":
        "另外根据疗愈场所的面积进行尺寸的选择，大场地，选择满月钵，颜色适合深色为主，小场合，适合小型满月钵，尺寸不宜太过大",
    "#### **价格方面**": "**价格方面**",
}

def fix_heading(line):
    s = line
    if s in rename_map:
        s = rename_map[s]
        return s, True
    # regex-based: 5.7.x -> 4.5.x (chapter 4 section 5 leftover)
    m = re.match(r'^(#{3,4})\s+5\.7\.', s)
    if m:
        return re.sub(r'5\.7\.', '4.5.', s, count=1), True
    m = re.match(r'^(####)\s+2\.7\.2\.3\s', s)
    if m:
        return re.sub(r'2\.7\.2\.3', '4.5.2.3', s, count=1), True
    # fix 1.3.13单 missing space -> handled by cjk_space below
    return s, False

# ---- CJK-Latin spacing ----
def cjk_space(text):
    protected = []
    def mask(m):
        protected.append(m.group(0))
        return "\x00%d\x00" % (len(protected)-1)
    x = re.sub(r'<[^>]+>', mask, text)
    x = re.sub(r'\]\([^)]*\)', mask, x)
    x = re.sub(r'`[^`]*`', mask, x)
    x = re.sub(r'https?://\S+', mask, x)
    x = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', x)
    x = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', x)
    x = re.sub(r'\x00(\d+)\x00', lambda m: protected[int(m.group(1))], x)
    return x

n_rename = n_hfix = n_head_space = 0
new_lines = []
in_code = False
for i, l in enumerate(lines):
    if toc_start is not None and toc_start <= i < toc_end:
        new_lines.append(l)  # keep TOC untouched for now
        continue
    if l.lstrip().startswith("```"):
        in_code = not in_code
        new_lines.append(l); continue
    if in_code:
        new_lines.append(l); continue
    if re.match(r'^#{1,6}\s', l):
        changed = False
        s, ch = fix_heading(l)
        if ch: n_rename += 1; changed = True
        s2 = cjk_space(s)
        if s2 != s: n_head_space += 1; changed = True
        new_lines.append(s2)
        continue
    # body line
    b = cjk_space(l)
    if b != l: n_hfix += 1
    new_lines.append(b)

text = "\n".join(new_lines)

# global English fixes
text = text.replace("Stop ing", "Stopping")
text = text.replace("Stoping", "Stopping")

# ---- images: <img> -> markdown with alt ----
def img_repl(m):
    src = m.group(1)
    full = m.group(0)
    am = re.search(r'alt="([^"]*)"', full)
    alt = am.group(1) if am else "颂钵疗愈示意图"
    if not alt.strip():
        alt = "颂钵疗愈示意图"
    return "![%s](%s)" % (alt, src)
text2 = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', img_repl, text)
n_img = text.count("<img")
n_img2 = text2.count("<img")
p("img_before", n_img, "img_after", n_img2)

# ---- tables: <table> -> markdown ----
def clean_cell(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = s.replace("|", "\\|").strip()
    return s

def table_to_md(tbl):
    # find rows
    rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', tbl, re.I)
    out = []
    first = True
    header_done = False
    for r in rows:
        cells = re.findall(r'<t[hd][^>]*>([\s\S]*?)</t[hd]>', r, re.I)
        if not cells:
            # cells may use <td> without closing properly; fallback
            cells = re.split(r'</?t[hd][^>]*>', r)
            cells = [c for c in cells if c.strip() != ""]
        cells = [clean_cell(c) for c in cells]
        if first:
            out.append("| " + " | ".join(cells) + " |")
            out.append("| " + " | ".join(["---"] * len(cells)) + " |")
            first = False
        else:
            out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)

tables = re.findall(r'<table[\s\S]*?</table>', text2, re.I)
p("tables_found", len(tables))
for tb in tables:
    md_tbl = table_to_md(tb)
    text2 = text2.replace(tb, "\n" + md_tbl + "\n", 1)

# write
open(md, "w", encoding="utf-8").write(text2)

p("n_rename", n_rename, "n_head_space", n_head_space, "n_body_space", n_hfix)
p("DONE")
