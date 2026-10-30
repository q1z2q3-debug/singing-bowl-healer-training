# -*- coding: utf-8 -*-
import re, os

OUT = r"C:\Users\RunzeAI\AppData\Local\Temp\wb_l2_log.txt"
base = r"C:\Users\RunzeAI\WorkBuddy\疗愈天地\singing-bowl-healer-training"
md = os.path.join(base, "docs", "颂钵疗愈师培训7.0.md")

def p(*a):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(" ".join(str(x) for x in a) + "\n")
open(OUT, "w", encoding="utf-8").close()

# ---------- github slug ----------
def slug(content):
    s = content.strip().lower()
    s = re.sub(r'[^\w一-鿿㐀-䶿\s\-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    s = s.strip('-')
    return s

class Slugger:
    def __init__(self):
        self.seen = {}
    def get(self, content):
        base = slug(content)
        if base not in self.seen:
            self.seen[base] = 0
            return base
        self.seen[base] += 1
        return "%s-%d" % (base, self.seen[base])

slugger = Slugger()

def heading_content(line):
    m = re.match(r'^#{1,6}\s+(.*)$', line)
    return m.group(1).strip() if m else line.strip()

# ---------- chapter content ----------
chapter = {
"第一章 初识颂钵": (
"### 本章学习目标\n\n"
"- 认识颂钵的“型、名、质”与缘起发展；\n"
"- 区分传统钵与现代钵、满月钵等常见分类；\n"
"- 掌握请钵、持钵、敲钵、磨钵、移钵、放钵、止音等基础技法链条；\n"
"- 了解选钵要点与周边配件。\n",

"### 章节小结\n\n"
"本章从“什么是钵”出发，系统梳理了颂钵的型制、名称、材质与历史脉络，并拆解了从请钵到止音的完整操作技法。"
"器物与手感，是后续所有理论与实操的根基——先与钵“相处”，再谈疗愈。\n",

"### 思考题\n\n"
"1. 传统钵与现代钵在材质、音色与用途上有何差异？\n"
"2. 教材为何把“亲身感受”列为选钵的第一标准？\n"
"3. 请钵、持钵、敲钵三者之间，隐含着怎样的能量逻辑？\n"
),

"第二章 理论课题": (
"### 本章学习目标\n\n"
"- 理解声音要素与钵音（音调、泛音、五度音程）；\n"
"- 掌握同频共振、物理振动与能量场（三脉七轮、五大元素）的关系；\n"
"- 建立“疗愈原理”的科学—哲学统一框架。\n",

"### 章节小结\n\n"
"本章把声音、振动、能量三条线索编织成疗愈的理论地基：从“型质合一”到“脉轮星系”，再到“是什么让我们能量失衡”，"
"给出了一套可以解释的疗愈发生机制——疗愈，首先是“调频”。\n",

"### 思考题\n\n"
"1. 请用“同频共振”解释一次你体验过的颂钵疗愈。\n"
"2. 三大能量（瓦塔 / 皮塔 / 卡帕）如何对应你的体质？\n"
"3. 为什么说疗愈不是“修理”，而是“调频”？\n"
),

"第三章 实践操作": (
"### 本章学习目标\n\n"
"- 掌握气场清理、空间净化与单钵 / 多钵（含七钵综合）疗愈案例；\n"
"- 熟悉颂钵音乐会的环境布置与个案精品体验流程；\n"
"- 能针对失眠、肩颈、痛经等常见议题组合疗愈序列。\n",

"### 章节小结\n\n"
"本章把前两章的理论落到“手”上，提供了从减压、疏通经络到女性调理的大量可复用案例，"
"以及音乐会、个案的标准流程。技术会越练越熟，但“为人疗愈”的觉察，需要更长的时间。\n",

"### 思考题\n\n"
"1. 单钵疗愈与七钵综合疗法各自适合什么场景？\n"
"2. 个案流程中，为什么“自我能量保护”排在第一步？\n"
"3. 请为一位“失眠 + 头痛”的来访者设计一个疗愈序列。\n"
),

"第四章 颂钵生命智慧（高级）": (
"### 本章学习目标\n\n"
"- 体悟“人即钵”的生命观；\n"
"- 理解世界观（疗愈 / 易经 / 道德经 / 佛学 / 能量显化）与价值观（内丰盈、爱满溢、成长型思维）；\n"
"- 明确疗愈师的专业基础与元气自我修复方法。\n",

"### 章节小结\n\n"
"本章把疗愈从“技术”升华为“生命智慧”，给出疗愈师的伦理、状态要求，"
"以及三脉平衡、太极定桩、经络运动、持咒唱诵等元气自修功法。疗愈他人的前提，是被疗愈者先照看好自己。\n",

"### 思考题\n\n"
"1. “人即钵”对你而言意味着什么？\n"
"2. 疗愈师为何必须先做好自身的状态与能量管理？\n"
"3. 你会把哪一种自修功法纳入自己的日常？\n"
),

"第五章 自然疗法（初中高）": (
"### 本章学习目标\n\n"
"- 了解呼吸、瑜伽、芳香、颂钵、音乐、水晶、饮食、香道、冥想、气功等自然疗法；\n"
"- 理解它们与脉轮、音疗的协同关系；\n"
"- 初步形成“整合式自我养护”的思路。\n",

"### 章节小结\n\n"
"本章将颂钵置于更大的自然疗法图谱中，强调“整合”——以脉轮为轴，串联起身、心、息、境的全方位自我养护。"
"颂钵不是孤立的，它是最好的“承上启下”的疗愈媒介。\n",

"### 思考题\n\n"
"1. 你最想把哪两种自然疗法与颂钵结合？为什么？\n"
"2. 为什么“呼吸”被列在自然疗法的第一节？\n"
"3. 水晶疗愈与音疗可以如何配合？\n"
),

"附件": (
"### 本章学习目标\n\n"
"- 掌握冥想引导词、放松引导词的结构与用法；\n"
"- 能使用阿森斯失眠量表、焦虑 / 抑郁自评量表、阿育吠陀能量表做初步评估。\n",

"### 章节小结\n\n"
"附件是可直接使用的引导词模板与标准化自评量表，是教学演示与个案评估的实用工具箱。"
"量表只作初步筛查，不能替代专业诊断。\n",

"### 思考题\n\n"
"1. 引导词为何要从“坐姿 / 躺姿”再到“退出”？\n"
"2. 自评量表的局限是什么？什么情况下必须转介专业人士？\n"
),
}

front_matter = """## 序言（编者按）

《颂钵疗愈师培训 7.0（大字版）》是一份面向颂钵疗愈爱好者与准疗愈师的系统教材。它从“器物”讲起，经“理论”搭桥，落于“实操”，终归于“生命智慧”与“自然疗法”。

我们希望这份开源教材，能让更多人以低门槛、零成本的方式接触声音疗愈，也让从业者有一份可教学、可自学、可校验的参考。教材中的技法与观点，源自长期的实践教学沉淀；受篇幅与语境所限，部分表述偏重体感与经验，欢迎在开源社区中共同修订完善。

## 适用对象

- 颂钵疗愈零基础的爱好者；
- 希望系统学习的准疗愈师；
- 瑜伽、冥想、身心灵行业的从业者；
- 培训机构作为教学参考大纲。

## 使用说明

- **学习顺序**：建议按“初识 → 理论 → 实践 → 智慧 → 自然疗法”的脉络推进，由器入道。
- **自检工具**：每章开头设有“本章学习目标”，章末设有“章节小结”与“思考题”，用于自检掌握程度。
- **配图**：全书的图示集中于同目录 `media/` 文件夹，可对照正文查看。
- **开放共建**：本教材以 CC BY-NC-SA 4.0 协议开源，欢迎在仓库提交修订（见 `CONTRIBUTING.md`）。

## 疗愈安全须知

> ⚠️ 颂钵疗愈属于身心放松与自我探索的**辅助**方式，不能替代医疗诊断与治疗。出现明确病症，请及时就医。

禁忌与注意：

- 孕期（尤其前三个月）腹部避免直接放置颂钵与强振动；
- 植入心脏起搏器或体内有金属者，避免强磁场 / 强振动区域；
- 有癫痫史者，慎用强烈敲击与频闪类引导；
- 严重精神疾病发作期，应在专业医师指导下进行；
- 音量适中，避免长时间高分贝敲击损伤听力；
- 每位个案开始前，务必完成“自我能量保护”与“课前沟通”（见第三章个案流程）。

更多专业伦理与状态要求，见第四章《疗愈师专业基础要求》。

"""

glossary = """## 术语表

| 术语 | 释义 |
| --- | --- |
| 颂钵 | 喜马拉雅地区传统手工铜钵，现代广泛用于声音疗愈 |
| 泛音（Overtone） | 基音之外由共鸣体产生的和谐分音 |
| 同频共振 | 频率相近的物体相互带动振动的现象 |
| 三脉七轮 | 瑜伽能量体系：左 / 中 / 右三脉与七个能量中心 |
| 脉轮（Chakra） | 分布于人体的七个主要能量中心 |
| 止音 | 用手或软垫止住钵的持续振动，用于收束声波 |
| 五度音程 | 相距五个音级的音高关系，常用于定频与调音 |
| 瓦塔 / 皮塔 / 卡帕 | 阿育吠陀的三大体质能量（风 / 火 / 水） |
| 满月钵 | 体型较大、余音悠长的颂钵，适合空间疗愈 |

## 七轮速查表

| 脉轮 | 位置 | 对应元素 | 主题 |
| --- | --- | --- | --- |
| 海底轮 | 尾骨底部 | 土 | 安全感、生存、扎根 |
| 脐轮 | 下腹 | 水 | 创造力、性能量、愉悦 |
| 胃轮（太阳神经丛） | 上腹部 | 火 | 力量、意志、行动 |
| 心轮 | 胸口中央 | 风 | 爱、连接、慈悲 |
| 喉轮 | 喉咙 | 空 | 表达、真理、沟通 |
| 眉心轮 | 两眉之间 | — | 直觉、洞察、内视 |
| 顶轮 | 头顶 | — | 灵性、合一、超越 |

"""

# cross references: source heading content -> note (target anchors computed via slug)
cross = {
"第二节 振动基础（初中高）": "**相关阅读**：声音要素见 [2.1.2 声音要素](#%s)；疗愈原理见 [2.4 疗愈原理](#%s)。" % (slug("2.1.2 声音要素"), slug("第四节 疗愈原理（初中高）")),
"2.3.2 七轮": "**相关阅读**：常用七轮对照见 [七轮速查表](#%s)。" % slug("七轮速查表"),
"第四节 疗愈原理（初中高）": "**相关阅读**：实操禁忌与个案保护见 [疗愈安全须知](#%s)。" % slug("疗愈安全须知"),
"第一章 初识颂钵": "**相关阅读**：疗愈理论与能量体系见 [第二章 理论课题](#%s)。" % slug("第二章 理论课题"),
}

# ---------- process ----------
t = open(md, encoding="utf-8").read()
lines = t.split("\n")

toc_start = toc_end = None
for i, l in enumerate(lines):
    if toc_start is None and l.strip() == "## 目录":
        toc_start = i
    if toc_start is not None and re.match(r'^# 第一章 初识颂钵', l):
        toc_end = i
        break

new_lines = []
pending = None  # (chapter_key, summary, questions)
ref_inserted = set()

def flush_pending(nl, key):
    if key in chapter:
        _obj, _sum, _q = chapter[key]
        nl.append("")
        nl.append(_sum)
        nl.append("")
        nl.append(_q)
    else:
        nl.append("")
        nl.append("### 章节小结\n\n（本章小结待补。）\n")
        nl.append("")
        nl.append("### 思考题\n\n（思考题待补。）\n")

i = 0
N = len(lines)
while i < N:
    l = lines[i]
    # TOC block placeholder: emit nothing for now, will rebuild after loop
    if toc_start is not None and toc_start <= i < toc_end:
        i += 1
        continue
    # chapter H1
    if re.match(r'^# ', l):
        if pending is not None:
            flush_pending(new_lines, pending)
            pending = None
        key = heading_content(l)
        if key in chapter:
            new_lines.append(l)
            obj, _s, _q = chapter[key]
            new_lines.append("")
            new_lines.append(obj)
            pending = key
        else:
            new_lines.append(l)
        # cross ref after chapter heading
        if key in cross and key not in ref_inserted:
            new_lines.append("")
            new_lines.append(cross[key])
            ref_inserted.add(key)
        i += 1
        continue
    # cross ref on other headings
    hc = heading_content(l)
    if hc in cross and hc not in ref_inserted:
        new_lines.append(l)
        new_lines.append("")
        new_lines.append(cross[hc])
        ref_inserted.add(hc)
        i += 1
        continue
    new_lines.append(l)
    i += 1

# flush last pending (附件)
if pending is not None:
    flush_pending(new_lines, pending)
    pending = None

# insert front matter before # 第一章 (which is now in new_lines)
fm_idx = None
for idx, l in enumerate(new_lines):
    if re.match(r'^# 第一章 初识颂钵', l):
        fm_idx = idx
        break
if fm_idx is not None:
    new_lines[fm_idx:fm_idx] = front_matter.rstrip("\n").split("\n") + [""]

# insert glossary + chakra before ## 参考资料
ref_idx = None
for idx, l in enumerate(new_lines):
    if l.strip() == "## 参考资料":
        ref_idx = idx
        break
if ref_idx is not None:
    new_lines[ref_idx:ref_idx] = glossary.rstrip("\n").split("\n") + [""]

text = "\n".join(new_lines)

# ---------- rebuild TOC ----------
def rebuild_toc(txt):
    ls = txt.split("\n")
    toc = ["## 目录", ""]
    for l in ls:
        m = re.match(r'^(#{1,6})\s+(.*)$', l)
        if not m:
            continue
        content = m.group(2).strip()
        if content == "目录":
            continue
        if content in ("本章学习目标", "章节小结", "思考题"):
            continue
        anchor = slugger.get(content)
        level = len(m.group(1))
        indent = "  " * (level - 1)
        toc.append("%s- [%s](#%s)" % (indent, content, anchor))
    return "\n".join(toc) + "\n"

new_toc = rebuild_toc(text)

# the original TOC block was skipped while building new_lines; insert the
# rebuilt TOC at the very top of the document (before front matter).
new_lines[0:0] = new_toc.rstrip("\n").split("\n") + [""]
text = "\n".join(new_lines)

open(md, "w", encoding="utf-8").write(text)

p("front_matter_inserted", fm_idx is not None)
p("glossary_inserted", ref_idx is not None)
p("toc_rebuilt", True)
p("toc_entries", len([x for x in new_toc.split("\n") if x.strip().startswith("- ")]))
p("cross_inserted", len(ref_inserted), sorted(ref_inserted))
p("DONE")
