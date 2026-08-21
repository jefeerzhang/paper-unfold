#!/usr/bin/env python3
"""paper-unfold 工程自检脚本（CI 可复用）。

检查内容:
  1. 必需文件齐全
  2. 版本一致性（SKILL.md frontmatter / _meta.json / .claude-plugin/marketplace.json）
  3. 占位符残留（<owner> / @user / TODO / FIXME 等）
  4. SKILL.md 铁律完整性（铁律 0-7 及 3.5）
  5. SKILL.md frontmatter 必需字段
  6. tests/test-prompts.json 可解析且非空
  7. README 安装命令与仓库 owner 一致
  8. 各清单文件中的技能名一致（paper-unfold）

用法（在仓库根目录执行）:
  python scripts/validate_skill.py                  # 人类可读输出
  python scripts/validate_skill.py --json           # CI 友好 JSON 输出
  python scripts/validate_skill.py --expect-version 2.3.0   # 校验指定版本

依赖: Python 3.10+，PyYAML（pip install pyyaml）
退出码: 0 = 全部通过；1 = 存在失败项
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖 PyYAML，请先执行: pip install pyyaml")

# 仓库根目录（脚本位于 scripts/ 子目录下）
BASE_DIR = Path(__file__).resolve().parent.parent

# 仓库 owner（用于校验 README / _meta.json 安装命令是否已替换占位符）
OWNER = "jefeerzhang"
SKILL_NAME = "paper-unfold"

# 必需文件
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "_meta.json",
    ".claude-plugin/marketplace.json",
    "examples/example-output.md",
    "tests/test-prompts.json",
]

# SKILL.md frontmatter 必需字段
FRONTMATTER_FIELDS = ["name", "description", "version", "license"]

# 必须出现的铁律编号（含 3.5）
REQUIRED_IRON_LAWS = ["0", "1", "2", "3", "3.5", "4", "5", "6", "7"]

# 占位符 / 待办残留模式（针对 md/json/yml/yaml 文本文件）
PLACEHOLDER_PATTERNS = [
    (re.compile(r"<owner>|@user|\bowner/\b", re.IGNORECASE), "占位符 owner/@user"),
    (re.compile(r"\b(TODO|FIXME|XXX)\b"), "待办标记 TODO/FIXME/XXX（仅匹配大写，避免误伤模板示例如 paper:xxx）"),
    (re.compile(r"your[_-]?token\b", re.IGNORECASE), "占位符 your-token"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "占位文本 lorem ipsum"),
]

# 跳过扫描的路径（按目录名）
SCAN_SKIP = {".git", ".github"}

# 跳过扫描的文件（按文件名）：CHANGELOG 会合法引用 TODO/FIXME 等标记描述历史修复
SCAN_SKIP_FILES = {"CHANGELOG.md"}


def read_text(rel_path: str) -> str | None:
    p = BASE_DIR / rel_path
    if not p.exists():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def parse_meta() -> dict | None:
    text = read_text("_meta.json")
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_marketplace() -> dict | None:
    text = read_text(".claude-plugin/marketplace.json")
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def parse_frontmatter() -> dict:
    """解析 SKILL.md 的 YAML frontmatter（PyYAML），返回值统一转为字符串。"""
    text = read_text("SKILL.md")
    if text is None or not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items() if v is not None}


def list_scannable_files() -> list[Path]:
    """返回需要扫描占位符的文本文件（md/json/yml/yaml），跳过 .git 与 .github 及豁免文件。"""
    result = []
    for p in BASE_DIR.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(BASE_DIR)
        if any(part in SCAN_SKIP for part in rel.parts):
            continue
        if rel.name in SCAN_SKIP_FILES:
            continue
        if p.suffix.lower() in {".md", ".json", ".yml", ".yaml"}:
            result.append(p)
    return result


def check_required_files() -> tuple[bool, str]:
    missing = [f for f in REQUIRED_FILES if not (BASE_DIR / f).exists()]
    if missing:
        return False, f"缺少必需文件: {', '.join(missing)}"
    return True, f"必需文件齐全（{len(REQUIRED_FILES)} 个）"


def _version_str(value) -> str | None:
    """版本号归一化为字符串（防止 JSON/YAML 把 2.5 之类解析成数字）。"""
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def check_version_consistency(expect: str | None) -> tuple[bool, str]:
    meta = parse_meta()
    market = parse_marketplace()
    fm = parse_frontmatter()

    versions = {
        "SKILL.md": _version_str(fm.get("version")),
        "_meta.json": _version_str(meta.get("version")) if meta else None,
        "marketplace.json": _version_str(market.get("version")) if market else None,
    }
    missing = [src for src, v in versions.items() if not v]
    if missing:
        return False, f"版本源缺失（任一必需源缺失即失败，不再静默放行）: {', '.join(missing)}"
    known = set(versions.values())
    if len(known) > 1:
        return False, f"版本不一致: {versions}"
    version = known.pop()
    if expect and version != expect:
        return False, f"版本 {version} ≠ 期望 {expect}"
    return True, f"版本一致: v{version}" + (f"（符合期望 v{expect}）" if expect else "")


def check_placeholders() -> tuple[bool, str]:
    hits = []
    for p in list_scannable_files():
        text = read_text(str(p.relative_to(BASE_DIR)))
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for pat, label in PLACEHOLDER_PATTERNS:
                if pat.search(line):
                    hits.append(f"{p.relative_to(BASE_DIR)}:{lineno} [{label}]")
    if hits:
        return False, "发现占位符/待办残留:\n    " + "\n    ".join(hits)
    return True, "未发现占位符/待办残留"


def check_iron_laws() -> tuple[bool, str]:
    text = read_text("SKILL.md") or ""
    found = set(re.findall(r"铁律\s*(\d+(?:\.\d+)?)", text))
    missing = [n for n in REQUIRED_IRON_LAWS if n not in found]
    if missing:
        return False, f"SKILL.md 缺少铁律: {', '.join('铁律 ' + n for n in missing)}"
    return True, f"铁律完整（0-7 及 3.5，共 {len(REQUIRED_IRON_LAWS)} 条）"


def check_frontmatter() -> tuple[bool, str]:
    fm = parse_frontmatter()
    missing = [f for f in FRONTMATTER_FIELDS if not fm.get(f)]
    if missing:
        return False, f"SKILL.md frontmatter 缺少字段: {', '.join(missing)}"
    return True, "SKILL.md frontmatter 字段完整"


def check_test_prompts() -> tuple[bool, str]:
    text = read_text("tests/test-prompts.json")
    if text is None:
        return False, "tests/test-prompts.json 不存在"
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return False, f"tests/test-prompts.json 解析失败: {e}"
    prompts = data.get("test_prompts", [])
    if not isinstance(prompts, list) or not prompts:
        return False, "tests/test-prompts.json 的 test_prompts 为空或缺失"
    bad = [i for i, t in enumerate(prompts, 1)
           if not isinstance(t, dict) or not t.get("prompt") or not t.get("expect")]
    if bad:
        return False, f"tests/test-prompts.json 第 {', '.join(map(str, bad))} 项缺少 prompt 或 expect"
    return True, f"tests/test-prompts.json 有效（{len(prompts)} 组测试）"


def check_install_cmd() -> tuple[bool, str]:
    meta = parse_meta()
    readme = read_text("README.md") or ""
    install_cmd = meta.get("install_cmd", "") if meta else ""
    expected = f"npx skills add {OWNER}/{SKILL_NAME}"
    problems = []
    if install_cmd != expected:
        problems.append(f"_meta.json install_cmd = {install_cmd!r}")
    if expected not in readme:
        problems.append("README.md 缺少正确安装命令")
    if f"<{OWNER}>" in readme or "<owner>" in readme:
        problems.append("README.md 仍有 <owner> 占位")
    if problems:
        return False, "; ".join(problems)
    return True, f"安装命令一致（npx skills add {OWNER}/{SKILL_NAME}）"


def check_skill_names() -> tuple[bool, str]:
    fm = parse_frontmatter()
    meta = parse_meta()
    market = parse_marketplace()
    names = {
        "SKILL.md": fm.get("name"),
        "_meta.json": meta.get("name") if meta else None,
        "marketplace.json": market.get("name") if market else None,
    }
    market_skill = None
    if market:
        skills = market.get("skills", [])
        if isinstance(skills, list) and skills:
            market_skill = skills[0].get("name")
    names["marketplace.json skills[0]"] = market_skill
    bad = [f"{k}={v!r}" for k, v in names.items() if v != SKILL_NAME]
    if bad:
        return False, "技能名不一致: " + ", ".join(bad)
    return True, f"技能名一致（{SKILL_NAME}）"


CHECKS = [
    ("required_files", "必需文件", check_required_files),
    ("version_consistency", "版本一致性", check_version_consistency),
    ("placeholders", "占位符检查", check_placeholders),
    ("iron_laws", "铁律完整性", check_iron_laws),
    ("frontmatter", "frontmatter 字段", check_frontmatter),
    ("test_prompts", "测试契约", check_test_prompts),
    ("install_cmd", "安装命令", check_install_cmd),
    ("skill_names", "技能名一致", check_skill_names),
]


def run(expect_version: str | None) -> list[dict]:
    results = []
    for key, label, fn in CHECKS:
        if key == "version_consistency":
            ok, msg = fn(expect_version)
        else:
            ok, msg = fn()
        results.append({"name": key, "label": label, "ok": ok, "message": msg})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="paper-unfold 工程自检脚本（CI 可复用）")
    parser.add_argument("--json", action="store_true", help="CI 友好 JSON 输出")
    parser.add_argument("--expect-version", metavar="VERSION", help="校验指定版本（缺值时报错）")
    args = parser.parse_args()

    results = run(args.expect_version)
    passed = sum(1 for r in results if r["ok"])

    if args.json:
        print(json.dumps({"ok": passed == len(results), "passed": passed, "total": len(results), "checks": results}, ensure_ascii=False, indent=2))
    else:
        print(f"paper-unfold 自检报告（{passed}/{len(results)} 通过）")
        print("=" * 48)
        for r in results:
            mark = "✅" if r["ok"] else "❌"
            print(f"{mark} [{r['label']}] {r['message']}")
        print("=" * 48)
        print("结论: " + ("全部通过" if passed == len(results) else "存在失败项，请修复后重试"))

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
