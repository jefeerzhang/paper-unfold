<sub>🌐 <b>中文</b></sub>

<div align="center">

# paper-unfold · 文献渐进式导读 + 研究空白识别

> *「把一篇论文读三遍？不如先让它像折纸一样一层一层展开。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-paper--unfold-blueviolet)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/jefeerzhang/paper-unfold)](https://skills.sh/jefeerzhang/paper-unfold)

**输入 PDF 或链接，展开四层导读；再说「识别研究空白」，得到 Miles 七分法扫描与交叉验证报告。**

[看效果](#效果示例) · [安装](#快速开始) · [触发方式](#触发方式) · [安全边界](#安全边界)

</div>

---

## 你什么时候需要它？

- 导师丢给你一篇论文，你需要 10 分钟判断值不值得精读。
- 跨学科读文献，术语密度总是不对：太浅没收获，太深读不动。
- 读完就忘，想要一份能存档、能追问的结构化笔记。
- 开题前想知道这个领域还有什么没被研究过，需要一份结构化的空白分析。

---

## 效果示例

| 模式 | 样例 | 说明 |
|------|------|------|
| 导读 | [example-output.md](examples/example-output.md) | 四层结构节选（Attention Is All You Need） |
| 空白 | [example-gap-output.md](examples/example-gap-output.md) | Miles 七分法 + 空白地图（《耐心资本与企业颠覆性创新》） |
| 导读 + 空白 | [example-output-wangjiaxin.md](examples/example-output-wangjiaxin.md) · [example-gap-output-wangjiaxin.md](examples/example-gap-output-wangjiaxin.md) | 同一篇《管理世界》论文；含 SciVerse 实跑记录（工具、`doc_id`、未入库与接口限制均如实标注） |

```text
输入：一篇 PDF 或 arXiv 链接
输出：Markdown 报告，含四层理解、知识族谱图、自测清单
保存：./文献导读/<论文简称>_文献导读.md
```

```text
输入：一篇 PDF + 说「识别研究空白」
输出：Markdown 报告，含七项空白扫描、空白地图、高价值方向建议
保存：./研究空白/<论文简称>_研究空白分析.md
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

学术检索（后续批评/复现、推荐阅读、空白交叉验证）依赖 SciVerse。**首次使用 Agent 会主动检测 `SCIVERSE_API_TOKEN`**。手动配置：

1. 打开 [SciVerse 鉴权说明](https://sciverse.space/docs#auth) 申请 API Token（控制台签发，前缀以控制台为准，常见为 `sci___` 或 `sv-`）
2. 任选其一：导出环境变量，或写入项目 `.mcp.json`：

```bash
export SCIVERSE_API_TOKEN=你的token
```

```json
{
  "mcpServers": {
    "sciverse": {
      "command": "npx",
      "args": ["-y", "sciverse-mcp-server"],
      "env": {
        "SCIVERSE_API_TOKEN": "你的token"
      }
    }
  }
}
```

3. 重启 Claude Code / Cursor / Codex

> 没配 token 也能继续，但推荐阅读、后续批评/复现、空白 G4 交叉验证只能**在你显式同意后**降级到 WebSearch（**禁止静默降级**）。报告须标注「⚠️ SciVerse 不可用」。

### 3. 安装 Skill

```bash
npx skills add jefeerzhang/paper-unfold
```

装完对 Agent 说（二选一）：

```text
帮我展开这篇论文：https://arxiv.org/pdf/2509.22186
```

```text
识别这篇论文的研究空白：<本地 PDF 或链接>
```

---

## 触发方式

### 文献导读

- 帮我展开/解读这篇 PDF：`<path>`
- 解读这个链接的论文：`<url>`
- 我是科研小白，帮我读这篇论文
- 用资深学者视角分析这篇论文
- 生成这篇论文的知识族谱图
- 这篇论文之后有什么批评或复现？
- 推荐和这篇相关的 3-5 篇文献
- 首次使用 paper-unfold，帮我展开这篇论文（触发 SciVerse Token 检测与配置引导）

### 识别研究空白

- 帮我识别这篇论文的研究空白：`<path>`
- 分析这篇论文的 research gap：`<url>`
- 基于这篇论文，找研究空白
- 这篇论文有哪些 gap 还没被填补？

---

## 它会交付什么？

### 文献导读模式

| 产物 | 说明 |
|------|------|
| 四层导读报告 | 直觉层 → 概念层 → 技术层 → 批判层 |
| 知识族谱图 | 前因 → 本研究 → 后果，标注开创性/渐进式贡献 |
| 后续检索报告 | SciVerse 验证后续批评、复现、反转（无 token 须显式同意 fallback） |
| 推荐阅读 | 3–5 篇相关文献（优先 SciVerse `doc_id` / `unique_id`） |
| 自测清单 | 基础/进阶/深度三级问题 |
| 自动保存 | `./文献导读/<论文简称>_文献导读.md` |

### 识别研究空白模式

| 产物 | 说明 |
|------|------|
| 文献概览 | 核心问题、方法、样本、主要发现 |
| 七项空白扫描 | Miles 七分法逐项分析，含存在性判断 + 证据 + 置信度 |
| 空白地图 | 汇总表格，一眼看清哪些空白存在、哪些已被填补 |
| 交叉验证 | SciVerse：`semantic_search` + `search_papers` + `list_paper_relations`；未命中如实写「需进一步确认」 |
| 高价值建议 | 1-3 个最值得跟进的空白方向 + 推荐阅读 |
| 自动保存 | `./研究空白/<论文简称>_研究空白分析.md` |

---

## SciVerse 在本项目中做什么

SciVerse 是学术检索后端，不是 PDF 阅读器。Agent 用它给**可追溯**的论文元数据、段落 chunk 和原文切片，避免凭印象编造引用。

| 环节 | 工具 | 用途 |
|------|------|------|
| 学字段 | `list_catalog` | 查 DOI/年份等可过滤字段，避免猜参数 |
| 精确查找 | `search_papers` | 作者、标题、DOI、主题；返回 `unique_id`，有全文时才有 `doc_id` |
| 语义 RAG | `semantic_search` | 自然语言找相关段落（批评/复现/空白交叉验证） |
| 扩读原文 | `read_content` | 按 `doc_id` + `offset` 拉字节切片 |
| 引文网络 | `list_paper_relations` | `CITATIONS` / `REFERENCES`；`total_count=0` 只表示库内关系空，不等于零引用 |
| 图表 | `get_resource` | `read_content` Markdown 里的图/表 |

无 token、401 或检索无果时：**停下来告知**，不得静默改用网页搜索。中文新刊可能尚未入库（见王嘉鑫样例的 DOI 未命中记录）。

接入说明：[Sciverse 文档](https://sciverse.opendatalab.com/docs) · [Agent Tools 仓库](https://github.com/opendatalab/Sciverse-Agent-Tools)

## 提取方式

| 方式 | 命令/工具 | 适用场景 |
|------|-----------|----------|
| `pdftotext` | poppler | 文本型 PDF，速度最快 |
| `pymupdf` | Python 库 | 需要更精细控制时 |
| `pdfplumber` | Python 库 | 本机未装 poppler/pymupdf 时的常用备选 |
| 手动粘贴 | 用户直接提供文本 | 扫描件、加密 PDF、提取失败时 |

**建议**：有 `pdftotext` 先用；否则 `pymupdf` / `pdfplumber`；再不行就粘贴文本。不要把 PDF 上传到外部解析服务。

---

## 安全边界

- **不会**自动联网付费下载论文。
- **不会**把 PDF 上传到任何外部服务。
- **不会**替你改写论文内容或生成未标注的引用。
- 如果 PDF 加密、扫描质量差或 URL 无法访问，会停下来说明并给出替代方案。
- 学术相关检索走 SciVerse（推荐/批评/复现/空白交叉验证）；失败时才用 WebSearch fallback，且**必须经用户显式同意**，禁止静默降级。

---

## 它不是什么

- **不是**单篇论文的扁平摘要。
- **不是**文献综述生成器（多篇综合不在范围）。
- **不是**论文改写或代写助手。
- **不是**自动引用生成器（推荐/批评必须 SciVerse 检索验证）。
- **不是**开题报告代写工具（研究空白分析只做建议，不替用户撰写选题论证）。
- **不是**万能空白探测器（分析基于单篇论文 + 有限检索，用户需结合领域知识做最终判断）。
- **不是**静默降级的工具。SciVerse Token 缺失会主动告知，不会偷偷用 WebSearch 替代而不告诉你。

---

## 文件结构

```text
paper-unfold/
├── SKILL.md                 # 技能定义（导读 + 识别研究空白）
├── README.md                # 安装与使用说明
├── LICENSE                  # MIT
├── _meta.json               # 元信息（兼容旧版）
├── CHANGELOG.md             # 变更记录
├── 研究空白.md              # 空白识别知识底座（G3 前必读）
├── examples/
│   ├── example-output.md                 # 导读样例
│   ├── example-gap-output.md             # 空白样例（耐心资本）
│   ├── example-output-wangjiaxin.md      # 导读样例（券商 AI × IPO 抑价）
│   └── example-gap-output-wangjiaxin.md  # 空白样例（同上，含 SciVerse 记录）
├── scripts/
│   └── validate_skill.py        # 工程自检脚本（版本/占位符/铁律）
├── tests/
│   └── test-prompts.json        # 测试 prompt 与期望输出
└── .github/
    └── workflows/
        └── skill-check.yml      # CI：push/PR 自动跑自检
```

---

## 验证与测试

```bash
# 工程自检（版本一致性 / 占位符残留 / 铁律完整性 / 必需文件）
python scripts/validate_skill.py

# 干跑测试（不调用真实 PDF 提取）
# 让 Agent 读取 SKILL.md 和 tests/test-prompts.json，
# 验证它能否复述四层结构、输出路径和失败处理策略。
```

验收 prompt：

```text
不实际提取 PDF，只根据 SKILL.md 说明：如果用户给一个扫描版 PDF，你会怎么处理？输出报告保存在哪里？
```

合格表现：回答提示用户 OCR 或手动粘贴文本，输出到 `./文献导读/`。

```text
不实际检索，只根据 SKILL.md：用户说「识别这篇论文的研究空白」时，报告顶部必须有什么？七项里能否只写存在的几项？知识底座是哪个文件？
```

合格表现：顶部必须有单篇论文局限性声明；七项全部扫描、不允许跳过；先读 `研究空白.md`；保存到 `./研究空白/`。

---

## 致谢

- [Poppler](https://poppler.freedesktop.org/)：`pdftotext` 提取工具
- [PyMuPDF](https://pymupdf.readthedocs.io/)：Python PDF 提取库
- [Sciverse](https://sciverse.opendatalab.com/docs)：学术检索与可追溯引用
- 四层渐进阅读法灵感来自 [SQ3R](https://en.wikipedia.org/wiki/SQ3R) (Robinson, 1946) 与费曼学习法
- 研究空白分类参考 Miles (2017) 七分法、Robinson et al. (2011) PICOS、Müller-Bloch & Kranz (2015)
- 细节保留原则参考 [FOCUS 工作流](https://doi.org/10.1038/s41587-025-02947-8) (Lin, 2025, *Nature Biotechnology*)

---

## License

[MIT](LICENSE)