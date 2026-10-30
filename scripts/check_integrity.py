# -*- coding: utf-8 -*-
"""Verify the textbook markdown: no leftover HTML img/table, table rows consistent."""
import re, sys

path = "docs/颂钵疗愈师培训7.0.md"
text = open(path, encoding="utf-8").read()
lines = text.split("\n")

img_left = len(re.findall(r"<img", text))
table_left = len(re.findall(r"<table", text))

# Check markdown table column consistency (consecutive lines starting with | )
issues = []
i = 0
in_table = False
expected = 0
while i < len(lines):
    line = lines[i]
    if line.lstrip().startswith("|"):
        cells = [c for c in line.split("|")]
        # strip leading/trailing empty from split
        cells = cells[1:-1] if cells and cells[-1].strip() == "" else cells[1:]
        n = len(cells)
        if not in_table:
            in_table = True
            expected = n
        elif n != expected:
            issues.append((i + 1, expected, n, line[:50]))
    else:
        in_table = False
    i += 1

print("img_left", img_left)
print("table_left", table_left)
print("len", len(lines))
print("table_issues", len(issues))
for it in issues:
    print("  row", it[0], "expected", it[1], "got", it[2], "::", it[3])
