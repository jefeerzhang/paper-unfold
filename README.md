<sub>🌐 <b>中文</b></sub>

<div align="center">

# paper-unfold · 文献渐进式导读

> *「把一篇论文读三遍？不如先让它像折纸一样一层一层展开。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-paper--unfold-blueviolet)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/jefeerzhang/paper-unfold)](https://skills.sh/jefeerzhang/paper-unfold)

**输入 PDF 或链接，自动展开直觉层→概念层→技术层→批判层的导读报告。**

[看效果](#效果示例) · [安装](#快速开始) · [触发方式](#触发方式) · [安全边界](#安全边界)

</div>

---

## 你什么时候需要它？

- 导师丢给你一篇论文，你需要 10 分钟判断值不值得精读。
- 跨学科读文献，术语密度总是不对：太浅没收获，太深读不动。
- 读完就忘，想要一份能存档、能追问的结构化笔记。

---

## 效果示例

👉 [examples/example-output.md](examples/example-output.md)：真实生成的四层导读报告框架。

```text
输入：一篇 PDF 或 arXiv 链接
输出：Markdown 报告，含四层理解、知识族谱图、自测清单
保存：./文献导读/<论文简称>_文献导读.md
```

---

## 快速开始

### 1. 安装 PDF 提取工具（二选一，可选）

```bash
# 方案 A：poppler（推荐，跨平台）
# Windows: 下载 https://github.com/oschwartz10612/poppler-windows/releases
# macOS:   brew install poppler
# Linux:   sudo apt install poppler-utils

# 方案 B：Python + pymupdf
pip install pymupdf
```

> 两个都不装也能运行，但会提示你手动粘贴 PDF 文本。

### 2. 配置 SciVerse API Token（强烈推荐）

学术相关检索（后续批评/复现、📚 推荐阅读）依赖 SciVerse MCP。**首次使用 Agent 会主动提示你配置 token**。手动配置步骤：

1. 打开 [SciVerse 官方文档](https://sciverse.space/docs#auth)（鉴权/Token 一节）注册并申请 API Token
2. 编辑项目 `.mcp.json`，在 `mcpServers.sciverse.env.SCIVERSE_API_TOKEN` 填入你的 token：

```json
{
  "mcpServers": {
    "sciverse": {
      "command": "npx",
      "args": ["-y", "sciverse-mcp-server"],
      "env": {
        "SCIVERSE_API_TOKEN": "sci___你的token"
      }
    }
  }
}
```

3. 重启 Claude Code / Cursor / Codex

> 没配 token 也能继续，但"📚 推荐阅读"和"后续批评/复现"只能**在你显式同意后**降级到 WebSearch（**禁止静默降级**），质量会下降。首次使用 Agent 会先引导你配置 token。

### 3. 安装 Skill

```bash
npx skills add jefeerzhang/paper-unfold
```

装完对 Agent 说：

```text
帮我展开这篇论文：https://arxiv.org/pdf/2509.22186
```

---

## 触发方式

- 帮我展开/解读这篇 PDF：`<path>`
- 解读这个链接的论文：`<url>`
- 我是科研小白，帮我读这篇论文
- 用资深学者视角分析这篇论文
- 生成这篇论文的知识族谱图
- 这篇论文之后有什么批评或复现？
- 推荐和这篇相关的 3-5 篇文献

---

## 它会交付什么？

| 产物 | 说明 |
|------|------|
| 四层导读报告 | 直觉层 → 概念层 → 技术层 → 批判层 |
| 知识族谱图 | 前因 → 本研究 → 后果，标注开创性/渐进式贡献 |
| 后续检索报告 | SciVerse + WebSearch 验证后续批评、复现、反转 |
| 推荐阅读 | 3-5 篇高度相关文献（SciVerse `doc_id` 可追溯） |
| 自测清单 | 基础/进阶/深度三级问题 |
| 自动保存 | `./文献导读/<论文简称>_文献导读.md` |

---

## 提取方式

| 方式 | 命令/工具 | 适用场景 |
|------|-----------|----------|
| `pdftotext` | poppler 自带 | 文本型 PDF，速度最快 |
| `pymupdf` | Python 库 | 需要更精细控制时 |
| 手动粘贴 | 用户直接提供文本 | 扫描件、加密 PDF、提取失败时 |

**建议**：优先用 `pdftotext`；遇到扫描件或复杂排版时换 `pymupdf` 或手动粘贴。

---

## 安全边界

- **不会**自动联网付费下载论文。
- **不会**把 PDF 上传到任何外部服务。
- **不会**替你改写论文内容或生成未标注的引用。
- 如果 PDF 加密、扫描质量差或 URL 无法访问，会停下来说明并给出替代方案。
- 学术相关检索走 SciVerse（推荐/批评/复现）；SciVerse 失败时才用 WebSearch fallback，且**必须经用户显式同意**，禁止静默降级。

---

## 它不是什么

- **不是**单篇论文的扁平摘要。
- **不是**文献综述生成器（多篇综合不在范围）。
- **不是**论文改写或代写助手。
- **不是**自动引用生成器（推荐/批评必须 SciVerse 检索验证）。
- **不是**静默降级的工具。SciVerse Token 缺失会主动告知，不会偷偷用 WebSearch 替代而不告诉你。

---

## 文件结构

```text
paper-unfold/
├── SKILL.md              # 技能定义与四层工作流
├── README.md             # 安装与使用说明
├── LICENSE               # MIT
├── _meta.json            # 元信息（兼容旧版）
├── CHANGELOG.md          # 变更记录
├── validate_skill.py     # 工程自检脚本（版本/占位符/铁律）
├── examples/
│   └── example-output.md    # 真实导读报告样例
├── test-prompts.json     # 测试 prompt 与期望输出
└── .github/
    └── workflows/
        └── skill-check.yml  # CI：push/PR 自动跑自检
```

---

## 验证与测试

```bash
# 工程自检（版本一致性 / 占位符残留 / 铁律完整性 / 必需文件）
python validate_skill.py

# 干跑测试（不调用真实 PDF 提取）
# 让 Agent 读取 SKILL.md 和 test-prompts.json，
# 验证它能否复述四层结构、输出路径和失败处理策略。
```

一条验收 prompt：

```text
不实际提取 PDF，只根据 SKILL.md 说明：如果用户给一个扫描版 PDF，你会怎么处理？输出报告保存在哪里？
```

合格表现：回答提示用户 OCR 或手动粘贴文本，输出到 `./文献导读/`。

---

## 致谢

- [Poppler](https://poppler.freedesktop.org/)：`pdftotext` 提取工具
- [PyMuPDF](https://pymupdf.readthedocs.io/)：Python PDF 提取库
- 四层渐进阅读法灵感来自 [SQ3R](https://en.wikipedia.org/wiki/SQ3R) (Robinson, 1946) 与费曼学习法
- 细节保留原则参考 [FOCUS 工作流](https://doi.org/10.1038/s41587-025-02947-8) (Lin, 2025, *Nature Biotechnology*)

---

## License

[MIT](LICENSE)