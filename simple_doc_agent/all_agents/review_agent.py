"""
code_review_agent.py

Agent 8: Code Review Agent
Performs static analysis on Python code using:
  - ruff:   code quality, style, best practices
  - bandit: security vulnerabilities
  - radon:  complexity metrics

Returns structured feedback for inclusion in documentation.
"""

import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from models import CodeReviewResult, CodeIssue

class CodeReviewAgent:
    """
    Runs static analysis on Python files in a repository.
    
    Tools used:
      1. ruff    — linting, style, best practices
      2. bandit  — security vulnerabilities
      3. radon   — cyclomatic complexity, maintainability index
    """

    def __init__(self):
        self._check_tools()

    def _check_tools(self) -> None:
        """Verify all required tools are installed."""
        for tool in ["ruff", "bandit", "radon"]:
            try:
                subprocess.run(
                    [tool, "--version"],
                    capture_output=True,
                    check=True,
                    timeout=300,
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError(
                    f"{tool} is not installed. Install with: pip install {tool}"
                )
    
    def run(self, files: dict[str, str], progress=None) -> CodeReviewResult:
        """
        Analyze Python files for issues.

        Args:
            files:    Dict mapping relative paths to file contents.
                      e.g., {"src/app.py": "import os\n...", ...}
            progress: Optional callback for progress updates.

        Returns:
            CodeReviewResult with all detected issues categorized.
        """
        def emit(msg: str) -> None:
            if progress:
                progress(msg)
        
        excluded = {"tests/"}
        python_files = {
            path: content
            for path, content in files.items()
            if path.endswith(".py") and not any(path.startswith(ex) for ex in excluded)
        }

        if not python_files:
            emit("⚠ No Python files found to review")
            return CodeReviewResult(total_issues=0)

        emit(f"🔍 Found {len(python_files)} Python file(s) to analyze")

        # Write files to temp dir for tool execution
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            for rel_path, content in python_files.items():
                file_path = tmp_path / rel_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding="utf-8")

            issues: list[CodeIssue] = []

            # 1. ruff — code quality, style, best practices
            emit("  → Running ruff (linting & style)...")
            issues.extend(self._run_ruff(tmp_path))

            # 2. bandit — security vulnerabilities
            emit("  → Running bandit (security scan)...")
            issues.extend(self._run_bandit(tmp_path))

            # 3. radon — complexity metrics
            emit("  → Running radon (complexity analysis)...")
            issues.extend(self._run_radon(tmp_path))

        # Categorize by severity
        result = CodeReviewResult(total_issues=len(issues))
        for issue in issues:
            if issue.severity == "critical":
                result.critical.append(issue)
            elif issue.severity == "high":
                result.high.append(issue)
            elif issue.severity == "medium":
                result.medium.append(issue)
            else:
                result.low.append(issue)

        # Summary metrics
        result.metrics = {
            "files_analyzed": len(python_files),
            "total_issues":   len(issues),
            "by_severity": {
                "critical": len(result.critical),
                "high":     len(result.high),
                "medium":   len(result.medium),
                "low":      len(result.low),
            },
            "by_category": {
                cat: len(items)
                for cat, items in result.by_category().items()
            },
        }

        emit(f"✓ Code review complete: {len(issues)} issue(s) found")
        return result
    
    def _run_ruff(self, path: Path) -> list[CodeIssue]:
        """Run ruff and parse JSON output."""
        try:
            result = subprocess.run(
                ["ruff", "check", str(path), "--output-format=json"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            # ruff exits non-zero when issues are found, which is expected
            data = json.loads(result.stdout) if result.stdout else []
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            return []

        issues = []
        for item in data:
            severity = self._map_ruff_severity(item.get("code", ""))
            category = self._map_ruff_category(item.get("code", ""))
            issues.append(
                CodeIssue(
                    severity=severity,
                    category=category,
                    file=item.get("filename", ""),
                    line=item.get("location", {}).get("row"),
                    column=item.get("location", {}).get("column"),
                    code=item.get("code", ""),
                    message=item.get("message", ""),
                    tool="ruff",
                )
            )
        return issues

    @staticmethod
    def _map_ruff_severity(code: str) -> str:
        """Map ruff rule codes to severity levels."""
        # Security issues (S) are high priority
        if code.startswith("S"):
            return "high"
        # Complexity (C901), potential bugs (B) are medium
        if code.startswith(("C", "B", "E7", "F")):
            return "medium"
        # Style, naming, etc. are low
        return "low"

    @staticmethod
    def _map_ruff_category(code: str) -> str:
        """Map ruff rule codes to categories."""
        if code.startswith("S"):
            return "security"
        if code.startswith(("C", "PLR")):
            return "complexity"
        if code.startswith(("E", "W", "N", "D")):
            return "style"
        return "quality"

    # ────────────────────────────────────────────────────────────────────
    # BANDIT
    # ────────────────────────────────────────────────────────────────────

    def _run_bandit(self, path: Path) -> list[CodeIssue]:
        """Run bandit security scanner and parse JSON output."""
        try:
            result = subprocess.run(
                ["bandit", "-r", str(path), "-f", "json"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            data = json.loads(result.stdout) if result.stdout else {}
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            return []

        issues = []
        for item in data.get("results", []):
            severity = self._map_bandit_severity(
                item.get("issue_severity", "LOW")
            )
            issues.append(
                CodeIssue(
                    severity=severity,
                    category="security",
                    file=item.get("filename", ""),
                    line=item.get("line_number"),
                    column=item.get("col_offset"),
                    code=item.get("test_id", ""),
                    message=item.get("issue_text", ""),
                    tool="bandit",
                )
            )
        return issues

    @staticmethod
    def _map_bandit_severity(level: str) -> str:
        """Map bandit severity to our scale."""
        mapping = {
            "HIGH":   "critical",
            "MEDIUM": "high",
            "LOW":    "medium",
        }
        return mapping.get(level.upper(), "medium")

    # ────────────────────────────────────────────────────────────────────
    # RADON
    # ────────────────────────────────────────────────────────────────────

    def _run_radon(self, path: Path) -> list[CodeIssue]:
        """Run radon complexity analysis and flag high-complexity functions."""
        try:
            result = subprocess.run(
                ["radon", "cc", str(path), "-s", "-j"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            data = json.loads(result.stdout) if result.stdout else {}
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            return []

        issues = []
        for filepath, functions in data.items():
            for func in functions:
                complexity = func.get("complexity", 0)
                rank       = func.get("rank", "A")

                # Flag complexity > 10 (rank C or worse)
                if complexity > 10:
                    severity = "high" if complexity > 20 else "medium"
                    issues.append(
                        CodeIssue(
                            severity=severity,
                            category="complexity",
                            file=filepath,
                            line=func.get("lineno"),
                            column=func.get("col_offset"),
                            code=f"CC{complexity}",
                            message=(
                                f"High cyclomatic complexity ({complexity}, rank {rank}) "
                                f"in function '{func.get('name', 'unknown')}'"
                            ),
                            tool="radon",
                        )
                    )
        return issues