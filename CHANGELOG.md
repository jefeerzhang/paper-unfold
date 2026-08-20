# Changelog

本项目的所有重要变更都会记录在此文件。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循[语义化版本](https://semver.org/lang/zh-CN/)。

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
