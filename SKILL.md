---
name: paper-unfold
description: |
  把任意 PDF 论文像折纸一样一层一层展开：
  直觉层（生活场景）→ 概念层（术语翻译）→ 技术层（菜谱步骤）→ 批判层（后续走向）。
  按读者背景（科研小白/进阶人员/资深学者）自适应密度。
  学术相关检索走 SciVerse（批评/复现/推荐），WebSearch 作为 fallback。
  SciVerse 需 API Token；无 Token 时必须引导用户配置，不静默降级。
  内置 PDF 提取（可选依赖 poppler / pymupdf，都不装可手动粘贴文本）。
version: 2.3.1
license: MIT
compatibility: Claude Code, Codex, OpenClaw, OpenCode
allowed-tools: [Read, Write, Edit, Bash, WebSearch, WebFetch, mcp__sciverse__search_papers, mcp__sciverse__semantic_search, mcp__sciverse__list_paper_relations, mcp__sciverse__list_catalog, mcp__sciverse__read_content, mcp__sciverse__get_resource]
---

# paper-unfold - 文献渐进式导读

## 核心定位

**一键式**学术文献导读专家，自动化完成：
1. **PDF 提取**：内置提取，无需外部依赖
2. **四层导读**：直觉层→概念层→技术层→批判层
3. **推荐阅读**：3-5 篇高度相关文献

**核心优势**：
- PDF 提取零外部依赖（poppler / pymupdf 二选一，可选装）
- 全自动流程：只需提供 PDF/链接
- LaTeX 公式自动渲染
- 自动保存到 `./文献导读/` 目录
- 学术检索走 SciVerse，引用可追溯（`doc_id`）—— **需 SCIVERSE_API_TOKEN**

---

## ⚠️ 生存铁律

### 铁律 0：首次使用检查
- **PDF 提取工具**：检查 `pdftotext`（poppler）或 Python `pymupdf` 是否可用；都不可用 → 提示用户安装
- **SciVerse Token**：检查 `SCIVERSE_API_TOKEN` 是否设置；未设置 → **必须引导用户配置**（详见"⚙️ SciVerse 配置引导"节）
- URL 输入 → 先下载到临时目录再提取

### 铁律 1：必须询问读者背景
- 首次导读前询问："请问您的研究背景是？🔹科研小白 🔹进阶人员 🔹资深学者"
- 未回复 → 默认"科研小白"

### 铁律 2：PDF 提取优先
- 必须先提取 PDF 文本内容
- 提取失败 → 尝试备用方案（pymupdf / pdfplumber / 手动粘贴文本）

### 铁律 3：事实检索强制
- "后续发展/批评/复现"等陈述必须 SciVerse（首选）+ WebSearch（fallback）+ 权威链接
- 推荐相关文献必须 SciVerse `semantic_search` / `search_papers` 检索
- 检索无果 → 明确写"未检索到后续反转"或"未检索到相关推荐"
- 关键断言必须可溯源（`doc_id` 或 URL）

### 铁律 3.5：SciVerse 鉴权必须引导用户配置（**关键**）
- 调用任何 `mcp__sciverse__*` 工具前，**必须**主动探测 `SCIVERSE_API_TOKEN` 环境变量
- **Token 缺失或返回 401/Authentication failed 时，禁止静默降级到 WebSearch**
- 必须做以下三件事（顺序不可乱）：
  1. **明确告知用户**：SciVerse 鉴权失败 / Token 未配置，会影响"后续批评/复现检索"和"📚 推荐阅读"两块的质量
  2. **提供 step-by-step 配置指南**（详见"⚙️ SciVerse 配置引导"节）
  3. **等用户决策**：是暂停任务等用户配置 token，还是**显式同意**用 WebSearch fallback（fallback 模式必须在报告里标注"⚠️ SciVerse 不可用，推荐阅读/后续批评质量下降"）
- **绝对禁止**：在用户未明确同意 fallback 的情况下，仅靠 WebSearch 强行生成"📚 推荐阅读"

### 铁律 4：分级表达规范
| 读者层级 | 术语密度 | Layer 1-2 篇幅 |
|----------|----------|---------------|
| 科研小白 | ≤5 术语/千字 | 50-60% |
| 进阶人员 | ≤15 术语/千字 | 30-40% |
| 资深学者 | 不限 | 10-20% |

**公式渲染规范**：
- 行内公式：`$...$`（如 $U(x) = \alpha x + \beta$）
- 独立公式块：`$$...$$`
- 禁止 Unicode 数学符号

### 铁律 5：四层递进输出
- 每层开头标注"🎓 理解层级：[层次名]"
- 后层内容不得出现在前层

### 铁律 6：知识脉络可视化
- 必须输出"知识族谱图"：前因→本研究→后果
- 标注"开创性贡献" vs "渐进式改进"

### 铁律 7：自动保存
- 默认目录：`./文献导读/<论文简称>_文献导读.md`
- UTF-8 无 BOM 编码

---

## ⚙️ SciVerse 配置引导（首次使用必读）

> 本节是**铁律 3.5** 的具体执行规范。当 Agent 调用 `mcp__sciverse__*` 遇到鉴权失败、或用户首次使用本 Skill 时，必须按本节引导用户完成配置。

### 检测时机

- **时机 A（启动检测，推荐）**：在用户输入论文/链接后、阶段 3 开始前，先用 `Bash` 检查 token：
  ```bash
  echo "$SCIVERSE_API_TOKEN"
  ```
  - 输出非空 → 正常进入工作流
  - 输出为空 → 触发引导（下方"配置步骤"）
- **时机 B（被动触发）**：直接调 `mcp__sciverse__*`，返回 401/Authentication failed → 触发引导
- **两种时机都接受**，但时机 A 更友好（用户先看到提示，不会先看到一个失败错误）

### 配置步骤（按顺序告知用户）

把以下内容**整段贴给用户**（不要省略）：

> ⚠️ **paper-unfold 需要 SciVerse API Token** 才能做学术相关检索（后续批评/复现 + 推荐阅读）。
>
> **获取 Token（2 分钟）：**
> 1. 打开 SciVerse 官方文档：[https://sciverse.space/docs#auth](https://sciverse.space/docs#auth)（鉴权/Token 一节；或 [https://opendatalab.github.io/Sciverse-Agent-Tools/](https://opendatalab.github.io/Sciverse-Agent-Tools/) 的"5 分钟接入"节）
> 2. 注册/登录账号
> 3. 在控制台申请 API Token（格式类似 `sci___xxxxxxxx`）
>
> **配置 Token 到你的项目**（选一种）：
>
> **A. 项目级 `.mcp.json`**（推荐本项目使用）：
> 编辑项目根目录的 `.mcp.json`，在 `mcpServers.sciverse.env.SCIVERSE_API_TOKEN` 填入你的 token：
> ```json
> {
>   "mcpServers": {
>     "sciverse": {
>       "command": "npx",
>       "args": ["-y", "sciverse-mcp-server"],
>       "env": {
>         "SCIVERSE_API_TOKEN": "sci___你的token"
>       }
>     }
>   }
> }
> ```
>
> **B. 系统环境变量**：
> ```bash
> # macOS / Linux
> export SCIVERSE_API_TOKEN="sci___你的token"
>
> # Windows PowerShell
> $env:SCIVERSE_API_TOKEN = "sci___你的token"
> ```
>
> **配置完成后**：
> - 重启 Claude Code / Cursor / Codex 等 Agent
> - 重新触发 paper-unfold 任务
>
> **没有 Token 也能用**：我会先完成 PDF 提取 + 四层导读（这部分不依赖 SciVerse）。但"📚 推荐阅读"和"Layer 4 后续批评/复现检索"会降级到 WebSearch，质量明显下降。
>
> **你想现在配置 Token，还是继续用 fallback 模式？**

### 用户决策后的行为

| 用户选择 | Agent 行为 |
|----------|-----------|
| **A. 配置 Token** | 暂停任务，给完配置步骤，等用户重启 Agent 后重新触发 |
| **B. 显式同意 fallback** | 在报告顶部加 "⚠️ SciVerse 不可用"横幅；Layer 4 后续检索和推荐阅读用 WebSearch 限定学术站点；推荐阅读加 "[fallback] "前缀标注来源降级 |
| **C. 跳过学术检索** | 报告里完全省略"📚 推荐阅读"和 Layer 4 后续检索两节；保留纯四层 + 知识族谱图 + 自测清单 |

### 禁止事项

- ❌ 静默 fallback（不告知用户就降级）
- ❌ 凭印象生成"📚 推荐阅读"内容而不经任何检索
- ❌ 用 "可用可不用" 这种模糊表述掩盖 token 缺失
- ❌ 拒绝完成任务（用户有权选择降级模式继续）

---

## 标准工作流程

### 阶段 1：PDF 提取

**提取策略**：
```
IF 输入是 URL
  → 下载到临时目录
IF pdftotext 可用
  → pdftotext -layout input.pdf output.txt
ELIF python + pymupdf 可用
  → python -c "import fitz; doc=fitz.open('input.pdf'); print(''.join(page.get_text() for page in doc))"
ELSE
  → 提示用户安装 poppler 或 pymupdf
```

**备用方案**：
- 扫描件/图片型 PDF → 提示用户粘贴文本或提供可复制文本版本
- 加密 PDF → 提示用户解密后重试

### 阶段 2：文献 DNA 扫描

提取关键信息：
- 标题、作者、年份、期刊、DOI
- 研究类型（理论/实证/综述/案例）

**核心三问（新生版）**：
1. 研究想解决什么问题？
2. 用了什么方法？
3. 发现了什么？

### 阶段 3：四层渐进理解

#### 🟢 Layer 1：直觉层
用生活场景建立问题感知。
> 思考：这个类比是否抓住本质？

#### 🔵 Layer 2：概念层
引入必要术语，每个配"翻译器"。
> 思考：概念定义是否与领域共识一致？

#### 🟡 Layer 3：技术层
拆解研究流程，用菜谱式步骤。
> 思考：方法选择是否最优？

#### 🔴 Layer 4：批判层
列未回答问题和后续走向。
> 思考：作者局限性讨论是否充分？

**Layer 4 后检索流程**（SciVerse 优先）：

1. 调用 `mcp__sciverse__search_papers` 按论文标题/DOI 反查拿到 `unique_id`
2. 调用 `mcp__sciverse__list_paper_relations(unique_id, relation=CITATIONS)` 找引用本文的论文
3. 调用 `mcp__sciverse__semantic_search` 用论文主题/方法描述做语义检索，找复现/批评/扩展
4. 对每条结果调用 `mcp__sciverse__read_content` 或 `WebFetch` 读摘要/方法节
5. 至少 3 个权威来源（SciVerse 返回 `doc_id` + 标题 + 出处）
6. 无果 → 调用 `WebSearch`（限定 `site:arxiv.org` / `site:openreview.net`），仍无果则写"未检索到可核验的后续反转"

### 阶段 4：知识固化

**输出结构**：
```markdown
# 《论文标题》文献导读

## 📋 文献 DNA 扫描
- 核心三问
- 后续检索报告

## 🎓 四层渐进理解
### 🟢 Layer 1：直觉层
### 🔵 Layer 2：概念层
### 🟡 Layer 3：技术层
### 🔴 Layer 4：批判层

## 🗺️ 知识族谱图
[Mermaid 图或文字描述]

## 📝 自测清单
[基础/进阶/深度 三级]
```

### 阶段 5：推荐阅读

在四层 + 族谱图 + 自测清单完成后，新增一节"📚 推荐阅读"，从学术库里检索 3-5 篇与本文**主题/方法/数据集**高度相关的文献，供用户作为后续阅读。

**检索策略（SciVerse 优先）**：

1. 提取本文的关键词：标题核心名词 + 方法名 + 数据集名 + 任务名
2. 调用 `mcp__sciverse__semantic_search(query="<关键词组合>")` 取 top 5-10
3. 对返回的每篇论文，调 `mcp__sciverse__search_papers` 或 `list_paper_relations` 验证相关性（避免误推无关论文）
4. 选 3-5 篇**与本文同领域、同方法族、同任务**的论文
5. SciVerse 无果 → `WebSearch`（限定学术站点），仍无果则标注"未检索到相关推荐"

**推荐维度**（按优先级）：

- **同方法族**：用了类似架构/算法的论文（用于横向比较）
- **同数据集/任务**：在同一 benchmark 上的工作（用于了解 SOTA 演进）
- **同领域的奠基/综述**：用户读完本文后可能想读的前置工作或综述
- **应用拓展**：把本文方法用到其他领域的工作

**每篇推荐格式**：

```markdown
- **[标题](URL)** — `doc_id: paper:xxx`
  一句话理由：与本文在 <方法/任务/数据集> 上的相似点 + 为什么值得读
```

**禁止**：
- 凭印象推荐未实际检索到的论文
- 推荐与本文无关的"凑数"论文
- 推荐自己（自我引用）的论文

---

## 📋 质量保障

### 交付前检查

- [ ] PDF 提取成功，文本非空
- [ ] 每层开头有"🎓理解层级"标注
- [ ] 后续检索含 ≥3 个权威来源（SciVerse 优先）
- [ ] 推荐阅读含 3-5 篇相关文献（SciVerse 检索 + doc_id）
- [ ] 术语首次出现有白话解释
- [ ] 知识族谱图含 ≥5 个节点
- [ ] **所有公式用 LaTeX 格式**
- [ ] 报告已保存到 `./文献导读/`

### 常见问题处理

| 情况 | 处理 |
|------|------|
| PDF 提取失败 | 尝试备用提取方案，或提示用户粘贴文本 |
| 内容超出理解范围 | 降维翻译，标注"简化版" |
| 检索无果 | 说明限制，给出替代方案 |
| 扫描件/图片型 PDF | 提示用户 OCR 或提供文本版 |
| **SciVerse Token 缺失 / 401** | **强制走"⚙️ SciVerse 配置引导"节，禁止静默降级** |

---

## 🚫 不是什么（负面定义）

为了避免误用，明确划清边界：

- **不是**单篇论文的扁平摘要。读完 Layer 1-2 就停，等于浪费了这个 Skill。
- **不是**文献综述生成器。多篇综合请用其他工具；本 Skill 默认一次一篇。
- **不是**论文改写或代写助手。只读论文，不替你写论文。
- **不是**付费数据库的入口。不联网付费下载论文。
- **不是**OCR 工具。扫描件不生成伪造导读，明确告知用户需 OCR 或粘贴文本。
- **不是**自动引用生成器。所有"后续发展/批评"必须 SciVerse/WebSearch 验证，无果如实写"未检索到后续反转"。
- **不是**推荐论文列表的工具凑数者。推荐阅读必须经 SciVerse 学术检索（`doc_id` 可追溯），不能凭标题印象编造。

---

## 📐 方法论锚点

四层递进结构源自两类经过验证的学习方法：

- **SQ3R 阅读法**（Robinson, 1946）：Survey → Question → Read → Recite → Review，先建立全局认知再深入。
- **费曼技巧**（Feynman, 1985）：能用大白话讲出来才算真懂，倒逼降维解释。

本 Skill 把 SQ3R 的"先 Survey 再 Read"映射为直觉层→技术层，把费曼技巧的"大白话讲出来"映射为概念层的术语翻译器。

> 参考：[FOCUS 工作流](https://doi.org/10.1038/s41587-025-02947-8)（Lin, 2025, *Nature Biotechnology*）证明了"穷举保留原文细节 + 嵌入直接引用"对科研阅读的有效性——本 Skill 在 Layer 3 技术层吸收了这一原则：保留方法名、样本量、效应量等具体数字。

---

## 🧭 边界处理（Edge Cases）

| 场景 | 处理 |
|------|------|
| 用户只贴标题/DOI，没有 PDF | 优先 WebFetch 找开放获取版（arXiv、PMC、出版社 OA 页面）；找不到则提示用户上传 PDF 或粘贴文本 |
| 用户上传极短文档（< 2 页） | 仍然走完整四层，但每层自然缩短，不强行注水 |
| 用户给多篇 PDF | 默认一篇一篇来，不合并；除非用户明确要求"综合这几篇" |
| 用户要求用其他语言生成 | 按用户输入语言生成；公式保留 LaTeX |
| 用户没指定读者层级 | 默认"科研小白"（最严格档） |
| 用户要求"两句话总结" | 不是本 Skill 的目标；建议用普通对话 |

## 🔧 工具说明（Tool Priority）

不同环节用不同工具，优先级如下：

| 环节 | 首选 | Fallback | 失败处理 |
|------|------|----------|----------|
| PDF 文本提取 | `pdftotext`（poppler） | `pymupdf`（Python）→ `pdfplumber` → 手动粘贴 | 提示用户粘贴文本 |
| URL 下载 | `curl` / `wget` | 浏览器工具 | 失败则问用户上传本地 PDF |
| 文献元数据扫描 | `pdftotext` + 论文首页解析 | SciVerse `search_papers` 反查 | 标注"元数据不完整" |
| 后续批评/复现检索 | SciVerse `list_paper_relations(relation=CITATIONS)` + `semantic_search` | `WebSearch`（限定 `site:arxiv.org`/`site:scholar.google.com`） | 明确写"未检索到可核验的后续反转" |
| 推荐相关文献 | SciVerse `semantic_search` + `search_papers`（按主题/方法/数据集相似度） | `WebSearch`（限定学术站点） | 明确写"未检索到相关推荐" |
| 元数据/概念补充 | SciVerse `read_content` + `get_resource` | `WebFetch` | 跳过该项 |

**关键原则**：

1. **SciVerse 优先**——任何学术相关检索（论文元数据、引文关系、复现记录、相关推荐）先用 SciVerse，因为它给 `doc_id`、可追溯的元数据、语义检索块。
2. **SciVerse 鉴权失败必须引导**——返回 401/Token 缺失时，**禁止静默降级**。必须按"⚙️ SciVerse 配置引导"节告诉用户怎么配置，并等用户决策（详见铁律 3.5）。
3. **WebSearch 仅作 fallback，且需用户显式同意**——SciVerse 失败或覆盖不全时使用，搜索时尽量限定学术站点（arxiv.org、scholar.google.com、openreview.net、acm.org 等）。fallback 模式下必须在报告里标注"⚠️ SciVerse 不可用"。
4. **WebFetch 用于获取 SciVerse 返回的 URL 详情**——拿到 URL 后用 WebFetch 读实际页面内容，不只依赖摘要。
5. **失败必须如实标注**——禁止在检索失败时凭印象编造论文或链接。

**SciVerse MCP 工具速查**：

- `mcp__sciverse__search_papers`：结构化检索（标题/作者/期刊/年份/DOI）
- `mcp__sciverse__semantic_search`：自然语言语义检索，返回相关论文块
- `mcp__sciverse__list_paper_relations(unique_id, relation=CITATIONS|REFERENCES|RELATED_WORKS)`：查引用/参考文献/相关工作
- `mcp__sciverse__list_catalog`：枚举可用字段（首次检索前可查）
- `mcp__sciverse__read_content(doc_id, offset, limit)`：读原文片段
- `mcp__sciverse__get_resource(file_name)`：拿论文里的图表图片

---

**准备就绪。等待用户输入 PDF 文件或链接...**
