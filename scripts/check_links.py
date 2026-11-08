# -*- coding: utf-8 -*-
"""Link / anchor / numbering checks for both textbooks. Exits 1 on any issue.

Covers, for docs/颂钵疗愈师培训7.0.md and en/book.md:
  1. every relative image reference exists on disk;
  2. every in-book markdown anchor link (#...) resolves to a real heading,
     using GitHub's slugger (no collapsing of consecutive hyphens);
  3. the zh table of contents anchors match the actual headings;
  4. numbered headings (e.g. 2.3.5.5) form a consistent outline
     (restarts at each H1 chapter).
"""
import io, os, re, sys, unicodedata

ZH = "docs/颂钵疗愈师培训7.0.md"
EN = "en/book.md"
TOC_BEGIN = "## 目录"
TOC_END = "## 序言（编者按）"

issues = []


def slug(text):
    s = text.strip().lower()
    out = []
    for ch in s:
        if ch == " ":
            out.append(" ")
        elif ch in "-_":
            out.append(ch)
        elif unicodedata.category(ch)[0] in ("L", "N"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def parse_headings(path):
    """Return list of (lineno, level, text, github_anchor) with de-dup."""
    res, seen = [], {}
    for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        text = m.group(2).strip()
        a = slug(text)
        if a in seen:
            seen[a] += 1
            a = "%s-%d" % (a, seen[a])
        else:
            seen[a] = 0
        res.append((i, len(m.group(1)), text, a))
    return res


def check_images(path):
    base = os.path.dirname(path)
    for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
        for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)", line):
            url = m.group(1)
            if url.startswith(("http://", "https://", "data:")):
                continue
            if not os.path.isfile(os.path.join(base, url)):
                issues.append("%s:%d missing image %s" % (path, i, url))


def check_anchor_links(path, anchors):
    for i, line in enumerate(io.open(path, encoding="utf-8"), 1):
        for m in re.finditer(r"\[[^\]]*\]\(#([^)]+)\)", line):
            if m.group(1) not in anchors:
                issues.append("%s:%d broken anchor #%s" % (path, i, m.group(1)))


def check_zh_toc(anchors):
    in_toc = False
    for i, line in enumerate(io.open(ZH, encoding="utf-8"), 1):
        s = line.strip()
        if s == TOC_BEGIN:
            in_toc = True
            continue
        if in_toc and s == TOC_END:
            break
        if not in_toc:
            continue
        m = re.search(r"\]\(#([^)]+)\)", line)
        if m and m.group(1) not in anchors:
            issues.append("%s:%d TOC anchor not found: #%s" % (ZH, i, m.group(1)))


def check_numbering(path, headings):
    """Outline consistency for numbered headings ('2.3.5.5 ...').

    Tolerates the book's style: unnumbered subsections occupy implicit
    slots (e.g. '3.1.1.5' may follow four unnumbered H4s), and a section
    transition like 1.1.4 -> 1.2.1 is valid. Flags depth jumps, wrong
    parent prefixes (the 1.3.1.x-under-1.2.1 class of bug) and
    non-monotonic siblings.
    """
    def valid_transition(prev, new):
        # same-length tuples: siblings must increase; a changed parent
        # is fine only when the new tuple restarts at 1 and the parent
        # itself is a valid transition.
        if new[:-1] == prev[:-1]:
            return new[-1] > prev[-1]
        return new[-1] == 1 and len(prev) > 1 and \
            valid_transition(prev[:-1], new[:-1])

    stack = []
    for (lineno, level, text, _a) in headings:
        if level == 1:  # chapter boundary: numbering restarts
            stack = []
            continue
        m = re.match(r"^(\d+(?:\.\d+)*)[\s、.]", text)
        if not m:
            continue
        nums = [int(x) for x in m.group(1).split(".")]
        label = ".".join(map(str, nums))
        if not stack:
            stack = nums
            continue
        if len(nums) > len(stack) + 1:
            issues.append("%s:%d numbering depth jump %s -> %s"
                          % (path, lineno, ".".join(map(str, stack)), label))
        elif len(nums) == len(stack) + 1:
            if nums[:-1] != stack:
                issues.append("%s:%d child %s not under %s"
                              % (path, lineno, label,
                                 ".".join(map(str, stack))))
        else:
            stack = stack[:len(nums)]
            if not valid_transition(stack, nums):
                issues.append("%s:%d numbering break %s -> %s"
                              % (path, lineno, ".".join(map(str, stack)),
                                 label))
        stack = nums


for path in (ZH, EN):
    headings = parse_headings(path)
    anchors = set(a for (_l, _lv, _t, a) in headings)
    check_images(path)
    check_anchor_links(path, anchors)
    check_numbering(path, headings)
check_zh_toc(set(a for (_l, _lv, _t, a) in parse_headings(ZH)))

if issues:
    print("FAIL: %d issue(s)" % len(issues))
    for it in issues[:50]:
        print(" -", it)
    sys.exit(1)
print("OK: images, anchors, TOC and numbering consistent for both books")
