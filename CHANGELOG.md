# Changelog

本项目的所有重要变更都会记录在此文件。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循[语义化版本](https://semver.org/lang/zh-CN/)。

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
