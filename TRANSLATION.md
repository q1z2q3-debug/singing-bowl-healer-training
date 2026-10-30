# 翻译贡献指南 · Translation Guide

本教材正在建设多语言版本。当前 **英文版（`en/`）** 已完成“前言 + 目录 + 术语表 + 七轮速查表 + 参考资料”等框架性内容的翻译，章节正文正在由社区逐步翻译。

> The textbook is being localized into multiple languages. The **English edition (`en/`)** currently has its framing material (preface, TOC, glossary, chakra reference, references) translated; chapter bodies are being translated incrementally by the community.

---

## 一、目录结构

```
en/
├── README.md        # 英文版说明 + 已翻译的前言 / 适用对象 / 使用说明 / 安全须知 / 目录 / 术语表 / 七轮速查表 / 参考资料
└── book.md          # （规划中）英文版正文，按章节逐步填充
```

英文版落地页：`en/index.html`（从根目录 `index.html` 右上角 `EN` 进入）。

---

## 二、翻译约定

1. **文件与标题**：正文翻译放入 `en/book.md`，保持与中文版一致的 `#`–`####` 层级与顺序。
2. **图片**：直接复用 `../docs/media/` 下的图片，路径写为 `![alt](../docs/media/xxx.png)`。
3. **术语统一**：专有名词首次出现时给出中英文对照，例如 `颂钵（Singing Bowl）`、`脉轮（Chakra）`、`止音（Stillness / muting the bowl）`。术语表以 `en/README.md` 中的 *Glossary* 为准。
4. **锚点与目录**：英文版目录的链接可指向中文正文对应锚点（便于对照阅读），待 `en/book.md` 完成后改为指向英文锚点。
5. **语气与风格**：教材偏“体感 + 经验”的口吻，翻译时保留平实、引导式的语气，避免过度学术化。
6. **协议与署名**：英文版同样遵循 **CC BY-NC-SA 4.0**，须保留原作者署名“润泽（五感六觉） / Runze (WuGanLiuJue)”，且**不得用于商业用途**。
7. **免责声明**：涉及健康的内容务必保留“不构成医疗建议，不能替代专业诊疗”的声明。

---

## 三、如何认领章节

1. 在仓库开一个 Issue，标题形如 `翻译认领：第三章 实践操作`，说明你计划翻译的范围。
2. 在 `en/book.md` 中对应章节下填写译文，尚未翻译的小节保留占位注释：
   ```markdown
   <!-- TODO: translate this section (3.1.3 单钵疗愈案例) -->
   ```
3. 提交 PR，并在描述中关闭对应的认领 Issue。

---

## 四、工具建议

- 可借助翻译模型做初稿，但**务必人工校对**专业术语与疗愈语境，避免机翻腔。
- 校验表格列数、图片路径、锚点是否一致（参考根目录 `scripts/check_integrity.py` 的思路）。

感谢你让声音疗愈被更多人听见 🌀
