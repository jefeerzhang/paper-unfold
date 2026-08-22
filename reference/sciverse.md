# SciVerse 配置与工具参考

本文件是 SKILL.md **铁律 3.5** 的具体执行规范。Agent 在首次使用本 Skill、或调用 `mcp__sciverse__*` 遇到鉴权失败时，按本文件引导用户完成配置。

## 检测时机

- **时机 A（启动检测，推荐）**：在用户输入论文/链接后、阶段 3 开始前，按顺序探测 token：
  1. 读取项目根目录 `.mcp.json`，检查 `mcpServers.sciverse.env.SCIVERSE_API_TOKEN` 是否已填真实值（非 `sci___你的token` 等占位符）
  2. `.mcp.json` 不存在或未配置 → 再用 `Bash` 检查系统环境变量：
     ```bash
     echo "$SCIVERSE_API_TOKEN"
     ```
  - 任一命中 → 正常进入工作流
  - 都未配置 → 触发引导（下方"配置步骤"）
  - 注意：`.mcp.json` 里的 `env` 只注入 MCP server 进程，Agent 的 shell 探测不到属正常——所以必须先查文件，不能只看环境变量
- **时机 B（被动触发）**：直接调 `mcp__sciverse__*`，返回 401/Authentication failed → 触发引导
- **两种时机都接受**，但时机 A 更友好（用户先看到提示，不会先看到一个失败错误）

## 配置步骤（按顺序告知用户）

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

## 用户决策后的行为

| 用户选择 | Agent 行为 |
|----------|-----------|
| **A. 配置 Token** | 暂停任务，给完配置步骤，等用户重启 Agent 后重新触发 |
| **B. 显式同意 fallback** | 在报告顶部加 "⚠️ SciVerse 不可用"横幅；Layer 4 后续检索和推荐阅读用 WebSearch 限定学术站点；推荐阅读加 "[fallback] "前缀标注来源降级 |
| **C. 跳过学术检索** | 报告里完全省略"📚 推荐阅读"和 Layer 4 后续检索两节；保留纯四层 + 知识族谱图 + 自测清单 |

## 禁止事项

- ❌ 静默 fallback（不告知用户就降级）
- ❌ 凭印象生成"📚 推荐阅读"内容而不经任何检索
- ❌ 用 "可用可不用" 这种模糊表述掩盖 token 缺失
- ❌ 拒绝完成任务（用户有权选择降级模式继续）

---

# SciVerse MCP 工具参考

## 工具优先级表

| 环节 | 首选 | Fallback | 失败处理 |
|------|------|----------|----------|
| PDF 文本提取 | `pdftotext`（poppler） | `pymupdf`（Python）→ `pdfplumber` → 手动粘贴 | 提示用户粘贴文本 |
| URL 下载 | `curl` / `wget` | 浏览器工具 | 失败则问用户上传本地 PDF |
| 文献元数据扫描 | `pdftotext` + 论文首页解析 | SciVerse `search_papers` 反查 | 标注"元数据不完整" |
| 后续批评/复现检索 | SciVerse `list_paper_relations(relation=CITATIONS)` + `semantic_search` | `WebSearch`（限定 `site:arxiv.org`/`site:scholar.google.com`） | 明确写"未检索到可核验的后续反转" |
| 推荐相关文献 | SciVerse `semantic_search` + `search_papers`（按主题/方法/数据集相似度） | `WebSearch`（限定学术站点） | 明确写"未检索到相关推荐" |
| 空白交叉验证 | SciVerse `semantic_search` + `search_papers` + `list_paper_relations` | `WebSearch`（须用户显式同意） | 标「需进一步确认 / 未检索到相关验证文献」 |
| 元数据/概念补充 | SciVerse `read_content` + `get_resource` | `WebFetch` | 跳过该项 |

## 关键原则

1. **SciVerse 优先**——任何学术相关检索（论文元数据、引文关系、复现记录、相关推荐、空白交叉验证）先用 SciVerse，因为它给 `doc_id` / `unique_id`、可追溯的元数据、语义检索块。
2. **SciVerse 鉴权失败必须引导**——返回 401/Token 缺失时，**禁止静默降级**。必须按本文"配置步骤"节告诉用户怎么配置，并等用户决策（详见 SKILL.md 铁律 3.5）。
3. **WebSearch 仅作 fallback，且需用户显式同意**——SciVerse 失败或覆盖不全时使用，搜索时尽量限定学术站点（arxiv.org、scholar.google.com、openreview.net、acm.org 等）。fallback 模式下必须在报告里标注"⚠️ SciVerse 不可用"。
4. **WebFetch 用于获取 SciVerse 返回的 URL 详情**——拿到 URL 后用 WebFetch 读实际页面内容，不只依赖摘要。
5. **失败必须如实标注**——禁止在检索失败时凭印象编造论文或链接。

## SciVerse MCP 工具速查

- `mcp__sciverse__search_papers`：结构化检索（标题/作者/期刊/年份/DOI）
- `mcp__sciverse__semantic_search`：自然语言语义检索，返回相关论文块
- `mcp__sciverse__list_paper_relations(unique_id, relation=CITATIONS|REFERENCES|RELATED_WORKS)`：查引用/参考文献/相关工作
- `mcp__sciverse__list_catalog`：枚举可用字段（首次检索前可查）
- `mcp__sciverse__read_content(doc_id, offset, limit)`：读原文片段
- `mcp__sciverse__get_resource(file_name)`：拿论文里的图表图片
