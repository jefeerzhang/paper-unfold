<sub>🌐 <b>中文</b></sub>

<div align="center">

# paper-unfold · 文献渐进式导读 + 研究空白识别

> *「把一篇论文读三遍？不如先让它像折纸一样一层一层展开。」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-paper--unfold-blueviolet)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/jefeerzhang/paper-unfold)](https://skills.sh/jefeerzhang/paper-unfold)

**输入 PDF 或链接，得到一份统一报告：四层导读 + 知识族谱图 + Miles 七分法空白分析。**

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

默认**一份** Markdown：前半四层导读 + 知识族谱图，后半研究空白。不拆成两个文件。

完整样例（同一产物结构，两篇并列）：

- [examples/example-output.md](examples/example-output.md)  
  王嘉鑫、赵牧（2025，《管理世界》）《“人工智能+”如何赋能券商高质量发展？》——四层导读、知识族谱图、七项空白、空白地图与 SciVerse 实跑记录（`doc_id` / 未入库 / 接口限制均如实标注）写在同一文件。
- [examples/example-output-yuyongze.md](examples/example-output-yuyongze.md)  
  余泳泽、胡鹏、朱子政（2025，《中国工业经济》）《耐心资本与企业颠覆性创新——基于企业机构投资者视角》——同一套结构；SciVerse 未命中本文 DOI，相邻文献（Deeg & Hardie、Danneels、外资机构与创新）给出 `doc_id` / `unique_id`。

```text
输入：一篇 PDF 或 arXiv 链接（说「展开」或「识别研究空白」均可）
输出：一份 Markdown = 四层导读 + 知识族谱图 + 七项空白扫描 + 空白地图
保存：./文献导读/<论文简称>_文献展开.md
禁止：再写 ./研究空白/ 或第二份报告
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

学术检索（后续批评/复现、推荐阅读、空白交叉验证）依赖 SciVerse。**首次使用 Agent 会主动检测配置（先查项目 `.mcp.json`，再查环境变量 `SCIVERSE_API_TOKEN`）**。手动配置：

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

装完对 Agent 说（两种说法产出**同一份**报告，只是篇幅侧重不同）：

```text
帮我展开这篇论文：https://arxiv.org/pdf/2509.22186
```

```text
识别这篇论文的研究空白：<本地 PDF 或链接>
```

---

## 触发方式

以下说法都生成**同一份** `_文献展开.md`（含族谱图与空白后半）：

- 帮我展开/解读这篇 PDF：`<path>`
- 解读这个链接的论文：`<url>`
- 我是科研小白，帮我读这篇论文
- 用资深学者视角分析这篇论文
- 生成这篇论文的知识族谱图
- 这篇论文之后有什么批评或复现？
- 推荐和这篇相关的 3-5 篇文献
- 帮我识别这篇论文的研究空白：`<path>`
- 分析这篇论文的 research gap：`<url>`
- 基于刚才的导读，把研究空白补进同一份报告
- 首次使用 paper-unfold，帮我展开这篇论文（触发 SciVerse Token 检测与配置引导）

---

## 它会交付什么？

**一份文件**，目录如下：

| 章节 | 说明 |
|------|------|
| 四层导读 | 直觉层 → 概念层 → 技术层 → 批判层 |
| 知识族谱图 | 前因 → 本研究 → 后果；「未填」节点对接后半空白 |
| 后续检索 | SciVerse 验证批评/复现（无 token 须显式同意 fallback） |
| 推荐阅读 | 3–5 篇（优先 SciVerse `doc_id` / `unique_id`） |
| 自测清单 | 基础/进阶/深度 |
| 七项空白扫描 | Miles 七分法；存在性 + 证据 + 置信度；节前 ⚠️ 单篇局限声明 |
| 空白地图 | 7 行表 + SciVerse 交叉验证记录 |
| 高价值建议 | 1–3 个方向 |
| 自动保存 | **仅** `./文献导读/<论文简称>_文献展开.md` |

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

无 token、401 或检索无果时：**停下来告知**，不得静默改用网页搜索。中文新刊可能尚未入库（见王嘉鑫、余泳泽两份样例的 DOI 未命中记录）。

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
- **不是**两份报告生成器。族谱图与空白分析必须写在同一文件，拒绝「导读一份、空白一份」。
- **不是**静默降级的工具。SciVerse Token 缺失会主动告知，不会偷偷用 WebSearch 替代而不告诉你。

---

## 文件结构

```text
paper-unfold/
├── SKILL.md                 # 技能定义（一份文献展开 = 导读 + 族谱图 + 空白）
├── README.md                # 安装与使用说明
├── LICENSE                  # MIT
├── _meta.json               # 元信息（兼容旧版）
├── CHANGELOG.md             # 变更记录
├── 研究空白.md              # 空白识别知识底座（G3 前必读，不是输出目录）
├── examples/
│   ├── example-output.md            # 完整样例（王嘉鑫等，券商 AI × IPO 抑价）
│   └── example-output-yuyongze.md   # 完整样例（余泳泽等，耐心资本 × 颠覆性创新）
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
# 依赖 PyYAML：pip install pyyaml
python scripts/validate_skill.py

# 干跑测试（不调用真实 PDF 提取）
# 让 Agent 读取 SKILL.md 和 tests/test-prompts.json，
# 验证它能否复述四层结构、输出路径和失败处理策略。
```

验收 prompt：

```text
不实际提取 PDF，只根据 SKILL.md 说明：如果用户给一个扫描版 PDF，你会怎么处理？输出报告保存在哪里？
```

合格表现：回答提示用户 OCR 或手动粘贴文本，输出到 `./文献导读/<论文简称>_文献展开.md`。

```text
不实际检索，只根据 SKILL.md：用户说「识别这篇论文的研究空白」时，空白节必须有什么？七项里能否只写存在的几项？知识底座是哪个文件？保存在哪？能否另存第二份？
```

合格表现：空白节须有单篇论文局限性声明；七项全部扫描、不允许跳过；先读 `研究空白.md`；与导读、族谱图写在同一份 `./文献导读/<论文简称>_文献展开.md`；禁止 `./研究空白/`。

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