#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_translate_driver.py
------------------------
Continues the English translation of the singing-bowl healer textbook, one section
per run. Designed to be invoked by a scheduler (e.g. Windows Task Scheduler every
30 minutes). It is SAFE: if no LLM API key is configured it logs and exits without
changing anything.

What it does each run:
  1. Read en/book.md. If there is NO `<!-- TODO` marker -> done, exit 0.
  2. Find the FIRST TODO marker and parse the Chinese section heading(s) to translate.
  3. Extract that section's text from the Chinese source (docs/颂钵疗愈师培训7.0.md).
  4. If an OpenAI-compatible API key is present in pypi.txt (labels:
     OPENAI_API_KEY / DEEPSEEK_API_KEY / ANTHROPIC_API_KEY / LLM_API_KEY), call the
     model to translate the section into fluent English, preserving markdown + images
     (re-pointed to ../docs/media/...). Otherwise log "no key" and exit 0.
  5. Replace the TODO with the translation, save, secret-scan, git add/commit/push
     using the GitHub token from pypi.txt (in-memory, never written to disk).

Paths are resolved relative to this script's location.
"""
import os, re, sys, json, subprocess, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "docs", "颂钵疗愈师培训7.0.md")
EN   = os.path.join(ROOT, "en", "book.md")
PYPY = r"C:\Users\RunzeAI\Desktop\pypi.txt"
REMOTE = "https://github.com/q1z2q3-debug/singing-bowl-healer-training.git"
LOG_DIR = os.path.join(os.environ.get("TEMP", "/tmp"), "wb_auto_translate")
os.makedirs(LOG_DIR, exist_ok=True)
LOG = open(os.path.join(LOG_DIR, "run_%s.log" % datetime.date.today().isoformat()), "a", encoding="utf-8")

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.write(s + "\n"); LOG.flush()

# ---- config helpers -------------------------------------------------------
def read_kv(path):
    kv = {}
    if not os.path.exists(path): return kv
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or "=" not in line: continue
        k, v = line.split("=", 1)
        kv[k.strip()] = v.strip().strip('"')
    return kv

def get_gh_token(kv):
    for k, v in kv.items():
        if "GITHUB_TOKEN" in k.upper():
            return v
    return None

def get_llm(kv):
    # returns (api_key, base_url, model) or None
    # priority: explicit LLM_* labels, else deepseek/openai
    pref = [("DEEPSEEK_API_KEY", "https://api.deepseek.com/v1/chat/completions", "deepseek-chat"),
            ("OPENAI_API_KEY", "https://api.openai.com/v1/chat/completions", "gpt-4o-mini"),
            ("ANTHROPIC_API_KEY", None, None),
            ("LLM_API_KEY", None, None)]
    for label, base, model in pref:
        if label in kv and kv[label]:
            # allow override of base/model via LLM_BASE / LLM_MODEL
            base = kv.get("LLM_BASE", base)
            model = kv.get("LLM_MODEL", model)
            return kv[label], base, model
    return None

# ---- section extraction ---------------------------------------------------
CJK = re.compile(r"[一-鿿]")
def find_todo(text):
    m = re.search(r"<!--\s*TODO(.*?)-->", text, re.S)
    return m

def parse_query(todo_body):
    """Return a list of grep patterns to locate source headings."""
    body = todo_body.strip()
    # If it contains CJK, it likely names the heading directly.
    if CJK.search(body):
        # extract quoted-ish heading fragments like 1.2.1 各类颂钵
        frags = re.findall(r"([0-9]+(?:\.[0-9]+)*\s*[一-鿿][一-鿿　-〿\w\s（）()、，。：:·\-]*?)(?:[，,/]|$)", body)
        if frags:
            return [f.strip() for f in frags if f.strip()]
        # fallback: take any run containing a digit and CJK
        run = re.search(r"[0-9][0-9\s.]*[一-鿿][^]]*", body)
        if run:
            return [run.group(0).strip()]
    # else numeric like "translate 2.1"
    nums = re.findall(r"\b(\d\.\d(?:\.\d)?)\b", body)
    if nums:
        return [r"^#+\s*" + re.escape(n) for n in nums]
    return []

def extract_section(src_text, pattern):
    lines = src_text.splitlines()
    # find first heading matching pattern
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^#+\s", ln) and re.search(pattern, ln):
            start = i; break
    if start is None:
        return None, None
    # determine heading level
    m = re.match(r"^(#+)\s", lines[start])
    level = len(m.group(1))
    end = len(lines)
    for j in range(start + 1, len(lines)):
        mm = re.match(r"^(#+)\s", lines[j])
        if mm and len(mm.group(1)) <= level:
            end = j; break
    heading = lines[start]
    body = "\n".join(lines[start+1:end]).strip()
    return heading, body

# ---- translation via LLM --------------------------------------------------
def translate(api_key, base_url, model, heading, body):
    sys_prompt = (
        "You are translating a Chinese singing-bowl (sound-healing) training manual into fluent, "
        "warm, informative English for an open-source edition. Preserve the markdown structure "
        "(headings, **bold**, bullet lists, GFM tables). Translate brand names: 简念=Jiannian, "
        "木子导师=Mentor Muzi, 润泽博士=Dr. Runze, 罄/磬=qìng. Output ONLY the translated markdown "
        "for the given section body, no commentary."
    )
    user = "HEADING (keep as English heading):\n%s\n\nBODY TO TRANSLATE:\n%s" % (heading, body)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
    }
    req = urllib.request.Request(base_url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Authorization": "Bearer %s" % api_key,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    return data["choices"][0]["message"]["content"].strip()

# ---- git helpers ----------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)

def main():
    log("=== auto_translate_driver run", datetime.datetime.now().isoformat(), "===")
    kv = read_kv(PYPY)
    llm = get_llm(kv)
    if not llm:
        log("NO_LLM_KEY: no OpenAI/DeepSeek/Anthropic key found in pypi.txt. Nothing to do (safe no-op).")
        log("EXIT_DONE")
        return 0

    if not os.path.exists(EN) or not os.path.exists(SRC):
        log("MISSING_FILES"); return 1

    en_text = open(EN, encoding="utf-8").read()
    m = find_todo(en_text)
    if not m:
        log("EN_BOOK_COMPLETE: no TODO markers remain.")
        return 0
    todo_body = m.group(1)
    queries = parse_query(todo_body)
    if not queries:
        log("CANNOT_PARSE_TODO:", todo_body[:120]); return 1

    src_text = open(SRC, encoding="utf-8").read()
    heading = body = None
    for q in queries:
        heading, body = extract_section(src_text, q)
        if heading: break
    if not heading:
        log("SECTION_NOT_FOUND for queries:", queries); return 1

    log("TRANSLATING:", heading)
    try:
        translated = translate(*llm, heading, body)
    except Exception as e:
        log("TRANSLATE_ERROR:", repr(e)); return 1

    # re-point images to ../docs/media/
    translated = re.sub(r"!\[([^\]]*)\]\((media/[^)]+)\)", r"![\1](../docs/\2)", translated)
    # replace the first TODO with translation
    new_en = en_text.replace(m.group(0), translated, 1)
    open(EN, "w", encoding="utf-8").write(new_en)

    # secret scan
    scan = subprocess.run(["git", "-C", ROOT, "grep", "-niE",
                           "ghp_|github_pat|api_key|secret", "--", "en/book.md"],
                          capture_output=True, text=True)
    if scan.returncode == 0:
        log("SECRET_SCAN_HIT (aborting commit):", scan.stdout[:300]); return 1

    gh = get_gh_token(kv)
    msg = "en: auto-translate %s" % heading.strip()
    git("add", "en/book.md")
    git("commit", "-m", msg)
    if gh:
        url = "https://%s@%s" % (gh, REMOTE.replace("https://", ""))
        res = git("push", url, "main")
        log("PUSH:", res.stdout[-300:] + res.stderr[-300:])
    else:
        log("NO_GH_TOKEN: committed locally only.")
    log("TODOs_remaining:", en_text.count("TODO") - 1)
    log("EXIT_DONE")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        LOG.close()
