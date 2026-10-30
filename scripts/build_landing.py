# -*- coding: utf-8 -*-
"""Generate an upgraded docs landing page (sidebar nav + search + dark mode + mobile)
from the textbook markdown's heading hierarchy."""
import io, re, json

MD = "docs/颂钵疗愈师培训7.0.md"
BASE = ("https://github.com/q1z2q3-debug/singing-bowl-healer-training/blob/main/"
        "docs/%E9%A2%82%E9%92%B5%E7%96%97%E6%84%88%E5%B8%88%E5%9F%B9%E8%AE%AD7.0.md")

def slug(text):
    s = text.lower()
    # keep a-z 0-9 - CJK; drop everything else (incl. full-width punctuation)
    s = re.sub(r"[^a-z0-9\-一-鿿㐀-䶿 ]", "", s)
    s = s.replace(" ", "-")
    s = re.sub(r"-+", "-", s).strip("-")
    return s

# Parse headings
headings = []  # (level, text, anchor)
seen = {}
with io.open(MD, encoding="utf-8") as f:
    for line in f:
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        if text == "目录":
            continue
        a = slug(text)
        # GitHub de-dup: append -1, -2 ... on collision
        if a in seen:
            seen[a] += 1
            a = "%s-%d" % (a, seen[a])
        else:
            seen[a] = 0
        headings.append((level, text, a))

# Build tree: H1 = chapter; H2 = section; H3 = subsection.
# H2 before first H1 -> synthetic 前言 group.
class Node:
    def __init__(self, level, text, anchor):
        self.level = level; self.text = text; self.anchor = anchor
        self.children = []

roots = []
front = Node(1, "前言 · Front Matter", "")
has_front = False
chapter = None
section = None
search_index = []

for (lvl, txt, anc) in headings:
    link = "%s#%s" % (BASE, anc)
    search_index.append({"t": txt, "a": anc, "l": lvl})
    if lvl == 1:
        chapter = Node(1, txt, anc); roots.append(chapter); section = None
    elif lvl == 2:
        node = Node(2, txt, anc)
        if chapter is None:
            if not has_front:
                roots.append(front); has_front = True
            front.children.append(node)
        else:
            chapter.children.append(node)
        section = node
    elif lvl >= 3:
        node = Node(lvl, txt, anc)
        parent = section if section is not None else (chapter if chapter is not None else front)
        if parent is None:
            parent = front
        parent.children.append(node)

def render(node, depth=0):
    pad = "  " * depth
    if node.level == 1:
        if not node.children:
            return '%s<li class="nav-leaf"><a href="%s#%s" data-text="%s">%s</a></li>' % (
                pad, BASE, node.anchor, node.text, node.text)
        inner = "\n".join(render(c, depth + 2) for c in node.children)
        return ('%s<details class="chap" open>\n'
                '%s  <summary><a href="%s#%s" data-text="%s">%s</a></summary>\n'
                '%s  <ul class="sub">\n%s\n%s  </ul>\n'
                '%s</details>') % (pad, pad, BASE, node.anchor, node.text, node.text,
                                    pad, inner, pad, pad)
    else:
        if not node.children:
            return '%s<li class="nav-leaf"><a href="%s#%s" data-text="%s">%s</a></li>' % (
                pad, BASE, node.anchor, node.text, node.text)
        inner = "\n".join(render(c, depth + 2) for c in node.children)
        return ('%s<li class="nav-branch">\n'
                '%s  <a href="%s#%s" data-text="%s">%s</a>\n'
                '%s  <ul class="sub">\n%s\n%s  </ul>\n'
                '%s</li>') % (pad, pad, BASE, node.anchor, node.text, node.text,
                              pad, inner, pad, pad)

nav_html = "\n".join(render(r, 3) for r in roots)
search_json = json.dumps(search_index, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>颂钵疗愈师培训 7.0（大字版）· 免费开源声音疗愈 / 音疗师培训教材</title>
  <meta name="description" content="免费开源的《颂钵疗愈师培训 7.0（大字版）》教材：系统讲解颂钵疗愈、声音疗愈、音疗师培训，涵盖颂钵技法、声音与振动理论、脉轮经络、个案实操与自然疗法。CC BY-NC-SA 4.0 协议。" />
  <meta name="keywords" content="颂钵疗愈师培训,声音疗愈,音疗师培训,颂钵教程,脉轮音疗,Tibetan Singing Bowl,Sound Healing,Sound Therapy Training,Chakra Healing" />
  <meta name="author" content="润泽（五感六觉）" />
  <meta name="robots" content="index, follow" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="颂钵疗愈师培训 7.0（大字版）· 免费开源教材" />
  <meta property="og:description" content="系统、免费、可传播的声音疗愈与音疗师培训教程。涵盖颂钵技法、理论、脉轮经络与实操。" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:url" content="https://q1z2q3-debug.github.io/singing-bowl-healer-training/" />
  <meta property="og:image" content="https://q1z2q3-debug.github.io/singing-bowl-healer-training/assets/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="https://q1z2q3-debug.github.io/singing-bowl-healer-training/assets/social-preview.png" />
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "颂钵疗愈师培训 7.0（大字版）",
    "description": "系统讲解颂钵疗愈与声音疗愈的免费开源培训教材，涵盖颂钵技法、声音与振动理论、脉轮经络、个案实操与自然疗法。",
    "inLanguage": "zh-CN",
    "provider": { "@type": "Organization", "name": "五感六觉 · 简念颂钵音疗中心",
                  "sameAs": "https://github.com/q1z2q3-debug/singing-bowl-healer-training" },
    "educationalLevel": "初学者到高级",
    "teaches": ["颂钵技法", "声音疗愈", "脉轮与经络", "个案实操", "疗愈师职业素养"],
    "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/"
  }
  </script>
  <style>
    :root{
      --bg:#f7f4ee; --ink:#2b2622; --muted:#7a7066; --accent:#8a6d3b; --line:#e5dccb;
      --card:#ffffff; --side:#fbf8f2; --hover:#efe7d6;
    }
    [data-theme="dark"]{
      --bg:#17150f; --ink:#e9e2d4; --muted:#a99e8c; --accent:#d8b46a; --line:#3a342a;
      --card:#211e17; --side:#1c1a13; --hover:#2c2820;
    }
    *{box-sizing:border-box}
    html,body{margin:0;padding:0}
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
      background:var(--bg);color:var(--ink);line-height:1.7;transition:background .25s,color .25s}
    a{color:var(--accent);text-decoration:none}
    a:hover{text-decoration:underline}
    /* top bar */
    .topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;
      padding:12px 18px;background:var(--card);border-bottom:1px solid var(--line)}
    .topbar .brand{font-weight:700;font-size:16px}
    .topbar .spacer{flex:1}
    .topbar .lang a{font-size:13px;padding:4px 8px;border:1px solid var(--line);border-radius:6px}
    .iconbtn{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--ink);
      border-radius:8px;padding:6px 10px;font-size:14px}
    .menu-btn{display:none}
    /* layout */
    .layout{display:flex;align-items:flex-start;max-width:1200px;margin:0 auto}
    .sidebar{position:sticky;top:54px;width:300px;max-height:calc(100vh - 54px);overflow:auto;
      background:var(--side);border-right:1px solid var(--line);padding:16px 14px}
    .sidebar h3{font-size:13px;color:var(--muted);margin:0 0 8px;letter-spacing:.04em}
    #search{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:8px;
      background:var(--card);color:var(--ink);font-size:14px;margin-bottom:12px}
    .nav-tree,.nav-tree ul{list-style:none;margin:0;padding:0}
    .nav-tree ul.sub{padding-left:14px;border-left:1px solid var(--line);margin-left:6px}
    .nav-tree details.chap>summary{list-style:none;cursor:pointer}
    .nav-tree details.chap>summary::-webkit-details-marker{display:none}
    .nav-tree summary a, .nav-tree .nav-branch>a, .nav-tree .nav-leaf>a{
      display:block;padding:6px 8px;border-radius:6px;font-size:14px}
    .nav-tree summary a{font-weight:600}
    .nav-tree .nav-leaf>a{font-size:13px;color:var(--muted)}
    .nav-tree a:hover{background:var(--hover);text-decoration:none}
    .nav-tree details.chap>summary::before{content:"\\25B8";display:inline-block;width:1em;
      color:var(--muted);transition:transform .15s}
    .nav-tree details.chap[open]>summary::before{transform:rotate(90deg)}
    .nav-count{color:var(--muted);font-size:12px;margin:4px 0 14px}
    /* main */
    .main{flex:1;min-width:0;padding:30px 28px 80px}
    .hero img{width:100%;border-radius:12px;border:1px solid var(--line);margin-bottom:18px}
    h1{font-size:28px;margin:0 0 6px;line-height:1.3}
    .sub{color:var(--accent);font-size:15px;margin:0 0 20px}
    .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:16px 0}
    .btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none!important;
      padding:11px 20px;border-radius:8px;font-weight:600;margin:6px 8px 6px 0}
    .btn.ghost{background:var(--card);color:var(--accent);border:1px solid var(--accent)}
    .kw{display:inline-block;background:var(--hover);color:var(--accent);border-radius:20px;
      padding:5px 12px;margin:4px 4px 0 0;font-size:13px}
    .qr{text-align:center;margin:24px 0}
    .qr img{width:220px;max-width:70%;border:1px solid var(--line);border-radius:10px}
    footer{color:var(--muted);font-size:13px;margin-top:36px;text-align:center}
    @media (max-width:860px){
      .menu-btn{display:inline-block}
      .sidebar{position:fixed;top:54px;left:0;height:calc(100vh - 54px);width:82%;max-width:320px;
        transform:translateX(-100%);transition:transform .25s;z-index:15;box-shadow:2px 0 12px rgba(0,0,0,.15)}
      .sidebar.open{transform:translateX(0)}
      .main{padding:22px 16px 70px}
    }
  </style>
</head>
<body>
  <div class="topbar">
    <button class="iconbtn menu-btn" id="menuBtn" aria-label="菜单">☰</button>
    <span class="brand">🌀 颂钵疗愈师培训 7.0</span>
    <span class="spacer"></span>
    <span class="lang"><a href="en/index.html">EN</a></span>
    <button class="iconbtn" id="themeBtn" aria-label="切换主题">🌙</button>
  </div>

  <div class="layout">
    <aside class="sidebar" id="sidebar">
      <h3>目录导航</h3>
      <input id="search" type="search" placeholder="搜索章节 / 关键词…" autocomplete="off" />
      <p class="nav-count" id="navCount"></p>
      <ul class="nav-tree" id="navTree">
__NAV__
      </ul>
    </aside>

    <main class="main">
      <div class="hero">
        <img src="assets/social-preview.png" alt="颂钵疗愈师培训 7.0 封面" />
      </div>
      <h1>颂钵疗愈师培训 7.0（大字版）</h1>
      <p class="sub">免费开源 · 声音疗愈 / 音疗师培训教材 · CC BY-NC-SA 4.0</p>

      <div class="card">
        <p>本站点对应 GitHub 开源仓库
          <a href="https://github.com/q1z2q3-debug/singing-bowl-healer-training">singing-bowl-healer-training</a>，
          收录《颂钵疗愈师培训 7.0（大字版）》完整 Markdown 教材，系统讲解<strong>颂钵疗愈、声音疗愈与音疗师培训</strong>。</p>
        <a class="btn" href="__BASE__">📖 在线阅读教材</a>
        <a class="btn ghost" href="https://github.com/q1z2q3-debug/singing-bowl-healer-training/archive/refs/heads/main.zip">⬇️ 下载仓库</a>
      </div>

      <h2>教材亮点</h2>
      <div class="card">
        <ul>
          <li><strong>由器入道</strong>：从“初识颂钵 → 理论课题 → 实践操作 → 生命智慧 → 自然疗法”五阶推进。</li>
          <li><strong>每章自检</strong>：章首“学习目标”、章末“章节小结”与“思考题”，方便自学校验。</li>
          <li><strong>实操工具箱</strong>：冥想引导词、放松词，以及阿森斯失眠、焦虑、抑郁、阿育吠陀等标准化量表。</li>
          <li><strong>配图丰富</strong>：全书 250+ 张图示，集中于 <code>docs/media/</code> 对照查阅。</li>
          <li><strong>开放共建</strong>：CC BY-NC-SA 4.0 协议，欢迎在仓库提交修订（见 <code>CONTRIBUTING.md</code>）。</li>
        </ul>
      </div>

      <h2>关键词</h2>
      <div>
        <span class="kw">颂钵疗愈师培训</span><span class="kw">声音疗愈</span><span class="kw">音疗师培训</span>
        <span class="kw">颂钵教程</span><span class="kw">脉轮音疗</span><span class="kw">身心放松</span>
        <span class="kw">助眠减压</span><span class="kw">Tibetan Singing Bowl</span>
        <span class="kw">Sound Healing</span><span class="kw">Sound Therapy Training</span><span class="kw">Chakra Healing</span>
      </div>

      <h2>联系我们</h2>
      <div class="qr">
        <img src="assets/wechat-qrcode.jpg" alt="简念颂钵音疗中心 微信二维码" />
        <p style="font-size:14px;color:var(--muted)">简念颂钵音疗中心 · 扫码交流</p>
      </div>

      <h2>许可协议</h2>
      <div class="card">
        <p>本作品采用 <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh">CC BY-NC-SA 4.0</a>
        （署名—非商业性使用—相同方式共享）协议开源。✅ 可自由阅读、下载、转发、教学；✅ 可改编（需相同协议共享）；❌ 不得用于商业用途。</p>
        <p style="color:#a05;font-size:14px">⚠️ 免责声明：教材内容仅用于学习与培训，不构成医疗建议，不能替代专业诊疗。</p>
      </div>

      <footer>© 2026 润泽（五感六觉）· 简念颂钵音疗中心 · 由 GitHub Pages 托管</footer>
    </main>
  </div>

  <script>
    var BASE = "__BASE__";
    // theme toggle
    var themeBtn = document.getElementById('themeBtn');
    var saved = localStorage.getItem('sbt-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
    function syncIcon(){ themeBtn.textContent = document.documentElement.getAttribute('data-theme')==='dark' ? '☀️' : '🌙'; }
    syncIcon();
    themeBtn.onclick = function(){
      var cur = document.documentElement.getAttribute('data-theme');
      var next = cur==='dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('sbt-theme', next); syncIcon();
    };
    // mobile menu
    var menuBtn = document.getElementById('menuBtn');
    var sidebar = document.getElementById('sidebar');
    menuBtn.onclick = function(){ sidebar.classList.toggle('open'); };
    document.querySelector('.main').addEventListener('click', function(){ sidebar.classList.remove('open'); });
    // search filter
    var search = document.getElementById('search');
    var tree = document.getElementById('navTree');
    var allItems = Array.prototype.slice.call(tree.querySelectorAll('li'));
    var countEl = document.getElementById('navCount');
    function applyFilter(q){
      q = q.trim().toLowerCase();
      var visible = 0;
      allItems.forEach(function(li){
        var a = li.querySelector('a');
        var t = (a ? a.getAttribute('data-text')||a.textContent : '').toLowerCase();
        var hit = !q || t.indexOf(q) !== -1;
        li.style.display = hit ? '' : 'none';
        if (hit) visible++;
        if (q){
          var d = li.closest('details');
          if (d && hit) d.open = true;
        }
      });
      countEl.textContent = q ? ('匹配 ' + visible + ' 项') : '';
    }
    search.addEventListener('input', function(){ applyFilter(this.value); });
  </script>
</body>
</html>
"""

HTML = HTML.replace("__NAV__", nav_html)
HTML = HTML.replace("__BASE__", BASE)
with io.open("index.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("nav items:", len(search_index))
print("root nodes:", len(roots))
print("wrote index.html")
