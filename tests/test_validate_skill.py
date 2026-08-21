#!/usr/bin/env python3
"""validate_skill.py 回归测试套件。

覆盖前次代码审查发现、且已在 2.5.2 根除的边界缺陷：

  H1  frontmatter 解析（手写解析器 -> yaml.safe_load）
      - sub1: 块标量内含冒号 / URL 不截断
      - sub2: 块标量内含空行不截断            <-- 关键回归点
      - sub3: YAML 列表写法不静默丢失
  M1  版本一致性：任一版本源缺失即失败（不再静默放行）
  M2  命令行参数：--expect-version 缺值立即报错（returncode != 0）

运行：
  python tests/test_validate_skill.py          # 直接运行
  python -m unittest tests.test_validate_skill -v
依赖：Python 3.10+，PyYAML（同 validate_skill.py）
"""
import importlib.util
import os
import subprocess
import sys
import unittest

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPT = os.path.join(_REPO, "scripts", "validate_skill.py")

_spec = importlib.util.spec_from_file_location("validate_skill_under_test", _SCRIPT)
vs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vs)


def _fm(text: str) -> dict:
    """用给定 frontmatter 文本调用真实 parse_frontmatter，不影响其他测试。"""
    original = vs.read_text
    try:
        vs.read_text = lambda rel: text if rel == "SKILL.md" else None
        return vs.parse_frontmatter()
    finally:
        vs.read_text = original


class FrontmatterTests(unittest.TestCase):
    def test_sub2_blank_line_in_block(self):
        """H1-sub2：块标量 description 含空行，必须完整保留（核心回归）。"""
        fm = _fm(
            "---\n"
            "name: paper-unfold\n"
            "description: |\n"
            "  第一行内容\n"
            "\n"
            "  空行之后的内容（必须保留）\n"
            "version: 2.5.2\n"
            "license: MIT\n"
            "---\n"
        )
        self.assertIn("空行之后的内容", fm["description"])
        self.assertTrue(fm["description"].strip().startswith("第一行内容"))

    def test_sub1_colon_and_url_in_block(self):
        """H1-sub1：块标量内含冒号与 URL 不截断（回归确认）。"""
        fm = _fm(
            "---\n"
            "name: paper-unfold\n"
            "description: |\n"
            "  见 https://example.com/docs#auth 与说明: 保留此行\n"
            "version: 2.5.2\n"
            "license: MIT\n"
            "---\n"
        )
        self.assertIn("https://example.com/docs#auth", fm["description"])
        self.assertIn("保留此行", fm["description"])

    def test_sub3_yaml_list_not_lost(self):
        """H1-sub3：YAML 换行列写法不再静默丢失。"""
        fm = _fm(
            "---\n"
            "name: paper-unfold\n"
            "description: 一个技能\n"
            "version: 2.5.2\n"
            "license: MIT\n"
            "allowed-tools:\n"
            "  - Read\n"
            "  - Write\n"
            "  - Edit\n"
            "---\n"
        )
        at = fm.get("allowed-tools", "")
        for tool in ("Read", "Write", "Edit"):
            self.assertIn(tool, at)

    def test_plain_scalar(self):
        fm = _fm(
            "---\n"
            "name: paper-unfold\n"
            "description: 普通单行\n"
            "version: 2.5.2\n"
            "license: MIT\n"
            "---\n"
        )
        self.assertEqual(fm["description"], "普通单行")

    def test_no_frontmatter_returns_empty(self):
        fm = _fm("# 没有 frontmatter 的文档\n正文")
        self.assertEqual(fm, {})

    def test_broken_yaml_does_not_crash(self):
        fm = _fm("---\nname: paper-unfold\ndescription: [未闭合\n---\n")
        # 损坏的 YAML 不应让脚本崩溃，至少返回 dict（损坏 frontmatter 视为无）
        self.assertIsInstance(fm, dict)


class VersionConsistencyTests(unittest.TestCase):
    def setUp(self):
        self._orig_read = vs.read_text
        self._orig_meta = vs.parse_meta
        self._orig_market = vs.parse_marketplace

    def tearDown(self):
        vs.read_text = self._orig_read
        vs.parse_meta = self._orig_meta
        vs.parse_marketplace = self._orig_market

    def _setup(self, meta, market, skill_text):
        vs.parse_meta = lambda: meta
        vs.parse_marketplace = lambda: market
        vs.read_text = lambda rel: skill_text if rel == "SKILL.md" else None

    def test_all_consistent_ok(self):
        self._setup(
            {"name": "paper-unfold", "version": "2.5.2"},
            {"name": "paper-unfold", "version": "2.5.2"},
            "---\nname: paper-unfold\nversion: 2.5.2\nlicense: MIT\n---\n",
        )
        ok, _ = vs.check_version_consistency(None)
        self.assertTrue(ok)

    def test_marketplace_missing_version_fails(self):
        """M1：marketplace.json 缺 version，其余一致 -> 必须失败。"""
        self._setup(
            {"name": "paper-unfold", "version": "2.5.2"},
            {"name": "paper-unfold"},  # 无 version
            "---\nname: paper-unfold\nversion: 2.5.2\nlicense: MIT\n---\n",
        )
        ok, msg = vs.check_version_consistency(None)
        self.assertFalse(ok)
        self.assertIn("marketplace.json", msg)

    def test_meta_missing_version_fails(self):
        self._setup(
            {"name": "paper-unfold"},  # 无 version
            {"name": "paper-unfold", "version": "2.5.2"},
            "---\nname: paper-unfold\nversion: 2.5.2\nlicense: MIT\n---\n",
        )
        ok, msg = vs.check_version_consistency(None)
        self.assertFalse(ok)
        self.assertIn("_meta.json", msg)

    def test_version_mismatch_fails(self):
        self._setup(
            {"name": "paper-unfold", "version": "2.5.1"},
            {"name": "paper-unfold", "version": "2.5.2"},
            "---\nname: paper-unfold\nversion: 2.5.2\nlicense: MIT\n---\n",
        )
        ok, _ = vs.check_version_consistency(None)
        self.assertFalse(ok)

    def test_numeric_version_normalized(self):
        """YAML/JSON 把 2.5 解析成 float 时，归一化为字符串比较仍一致。"""
        self._setup(
            {"name": "paper-unfold", "version": 2.5},
            {"name": "paper-unfold", "version": "2.5"},
            "---\nname: paper-unfold\nversion: 2.5\nlicense: MIT\n---\n",
        )
        ok, _ = vs.check_version_consistency(None)
        self.assertTrue(ok)


class CliArgTests(unittest.TestCase):
    def test_expect_version_missing_value_errors(self):
        """M2：--expect-version 缺值 -> argparse 报错（returncode != 0）。"""
        r = subprocess.run(
            [sys.executable, _SCRIPT, "--expect-version"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(r.returncode, 0)

    def test_help_ok(self):
        r = subprocess.run(
            [sys.executable, _SCRIPT, "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
