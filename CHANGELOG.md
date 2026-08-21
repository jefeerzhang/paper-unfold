# Changelog

本项目的所有重要变更都会记录在此文件。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [2.5.0] - 2026-08-21

### 变更
- **统一产物**：四层导读、知识族谱图与研究空白写进同一份 `./文献导读/<论文简称>_文献展开.md`；废除 `./研究空白/` 第二份输出。
- 用户说「展开」或「识别研究空白」只改变篇幅侧重，不改变文件数；导读后追加空白须补进已保存文件。
- README / SKILL / 测试契约 / 示例同步：官方样例改为完整统一报告，不再分拆导读/空白文件。并列两篇：`examples/example-output.md`（王嘉鑫等）与 `examples/example-output-yuyongze.md`（余泳泽等，耐心资本）。
- SciVerse 工具表补「空白交叉验证」行；`list_paper_relations` 的空结果不得写成零引用。

## [2.4.0] - 2026-08-20

### 新增
- **识别研究空白专项模式**：新增与文献导读并列的第二工作流（阶段 G1-G5），基于 Miles (2017) 七分法逐项分析 + SciVerse 交叉验证，输出结构化空白报告。
  - G1 输入获取：复用 PDF 提取，额外支持粘贴文本和导读报告输入。
  - G2 文献结构化扫描：提取研究问题、方法、样本、主要发现、作者自述局限性、未来方向。
  - G3 空白分类扫描：七项逐一分析（证据/知识/实践-知识冲突/方法/实证/理论/群体），每项输出存在性判断 + 证据 + 置信度。
  - G4 交叉验证：SciVerse 语义检索 + 引文关系查证，更新空白状态为「已填补 / 仍开放 / 需进一步确认」。
  - G5 报告输出：空白地图汇总表 + 高价值空白建议（≤3 个）+ 推荐阅读，保存到 `./研究空白/`。
- 报告顶部强制加入 ⚠️ 局限性声明：分析基于单篇论文 + 有限检索，不保证穷尽。
- 质量检查清单新增空白模式 8 项检查（局限性声明、七项全扫、三要素、空白地图、交叉验证、建议上限、推荐阅读、保存路径）。
- 边界处理新增 3 场景：综述论文特殊处理（跳过 G3 直接 G4）、导读后追加分析（复用 G2-G5）、无 Limitations 小节兜底。
- 方法论锚点补充 Miles (2017) 七分法、Robinson et al. (2011) AHRQ/PICOS 框架、Müller-Bloch & Kranz (2015) 可复现识别流程。
- 负面定义补充：不是开题报告代写工具、不是万能空白探测器。
- 添加 `研究空白.md` 知识底座文档，整合研究空白的定义、分类框架（Miles 七分法 + Robinson PICOS + Naqvi-Gabr 14 类）、学术演进脉络、识别策略、AI 工具应用、表述方法、常见误区。

### 变更
- SKILL.md frontmatter description 补充研究空白触发词（识别研究空白、分析 gap、找研究空白）；G3 前强制读取 `研究空白.md`。
- README.md 同步更新：标题加「+ 研究空白识别」、触发方式新增空白分析 4 条、交付物表格新增空白模式 6 项、安全边界和负面定义同步扩展；补充 SciVerse 工具表、双模式安装后第一句话、效果表示例入口。
- `_meta.json` description 补充空白模式触发场景与关键词。
- `.claude-plugin/marketplace.json` description 同步更新。
- 示例：`examples/example-gap-output.md`（余泳泽等，耐心资本）；`examples/example-output-wangjiaxin.md` 与 `example-gap-output-wangjiaxin.md`（王嘉鑫等，券商 AI × IPO 抑价，含 SciVerse 实跑记录）。
- 测试契约增至 15 组，覆盖空白模式（七项全扫、综述跳 G3、导读后追加、Token 缺失不静默）。

## [2.3.2] - 2026-08-20

### 修复
- 修正 `SKILL.md` 核心优势中「无需外部依赖」与 frontmatter「可选依赖 poppler/pymupdf」的矛盾，统一为「零必装依赖（可选，不装可手动粘贴）」。
- 修正 `README.md` 效果示例措辞：「真实生成」→「节选自真实论文导读」，与 `example-output.md` 实际内容一致。
- 标注 `examples/example-output.md` 中推荐文献的 `doc_id` 为示例值，以实际 SciVerse 检索为准。

### 新增
- 添加 `.gitignore`，排除 Python 缓存、编辑器临时文件、Claude Code 运行时目录。
- `README.md` 触发方式新增「首次使用 paper-unfold」场景，覆盖 SciVerse Token 缺失检测与配置引导。

### 变更
- 仓库目录结构调整：`validate_skill.py` 移至 `scripts/`，`test-prompts.json` 移至 `tests/`，根目录只保留技能定义与项目文档。
- 自检命令与 CI 同步更新为 `python scripts/validate_skill.py`。
- 技能入口 `SKILL.md` 保持在仓库根目录不变，安装命令（`npx skills add jefeerzhang/paper-unfold`）不受影响。

## [2.3.1] - 2026-08-20

### 新增
- 新增 `validate_skill.py` 工程自检脚本：校验必需文件、版本一致性、占位符残留、铁律完整性、frontmatter 字段、测试契约、安装命令与技能名。
- 新增 GitHub Actions CI（`.github/workflows/skill-check.yml`）：push / PR 自动运行自检。

### 修复
- 替换 `_meta.json` 与 `README.md` 中的 owner / author 占位符为真实值（owner=`jefeerzhang`、author=`jefeer`）。
- 统一 SciVerse 文档链接至官方 `https://sciverse.space/docs#auth`（替换无内容的 `sciverse.ai/dashboard`）。
- 澄清 README 中「未配置 Token 时降级」的表述：必须经用户**显式同意**才能 fallback，禁止静默降级（与铁律 3.5 对齐）。
- 修正 `_meta.json` 中 poppler/pymupdf 为「可选依赖」的表述，消除与 README「都不装也能运行」的矛盾。
- 修正 `SKILL.md` frontmatter 中「无需外部 CLI」的误导表述，明确 poppler/pymupdf 为可选依赖。

## [2.3.0] - 2026-08-02

初始发布：四层渐进式文献导读（直觉→概念→技术→批判），按读者背景自适应密度；内置 PDF 提取；SciVerse 检索（后续批评/复现 + 推荐阅读）+ Token 配置引导；知识族谱图与自测清单；自动保存到 `./文献导读/`。
