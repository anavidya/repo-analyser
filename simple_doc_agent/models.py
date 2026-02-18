from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any
# ==============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Command:
    name: str
    docstring: str
    arguments: List[Dict[str, Any]]


@dataclass
class PythonMetadata:
    project_name: str
    python_version: str
    dependencies: List[str]
    commands: List[Command]
    entry_points: List[str]
    docstrings: Dict[str, List[Dict[str, str]]] = field(default_factory=dict) 


@dataclass
class DockerMetadata:
    filename: str
    base_image: str
    exposed_ports: list[str]
    volumes: list[str]
    workdir: str
    entrypoint:str
    env_vars: list[str] = field(default_factory=list)
    


@dataclass
class CICDMetadata:
    stages: List[str]
    global_variables:Dict[str, Any]
    jobs: List[Dict[str, Any]]
    files_from_runners: list[str]


@dataclass
class Documentation:
    python: PythonMetadata
    docker: DockerMetadata
    cicd: CICDMetadata
    mermaid: str
    
@dataclass
class TestCoverage:
    test_coverage:list[dict]
    summary_coverage: str

@dataclass
class CodeIssue:
    """Single code quality/security issue."""
    severity: str       # "critical" | "high" | "medium" | "low"
    category: str       # "security" | "quality" | "complexity" | "style"
    file: str
    line: int | None
    column: int | None
    code: str           # rule code (e.g., "S101", "C901")
    message: str
    tool: str           # "ruff" | "bandit" | "radon"


@dataclass
class CodeReviewResult:
    """Complete code review output."""
    total_issues: int
    critical: list[CodeIssue] = field(default_factory=list)
    high: list[CodeIssue] = field(default_factory=list)
    medium: list[CodeIssue] = field(default_factory=list)
    low: list[CodeIssue] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    def by_severity(self) -> dict[str, list[CodeIssue]]:
        return {
            "critical": self.critical,
            "high":     self.high,
            "medium":   self.medium,
            "low":      self.low,
        }

    def by_category(self) -> dict[str, list[CodeIssue]]:
        """Group issues by category (security, quality, complexity, style)."""
        cats: dict[str, list[CodeIssue]] = {
            "security": [], "quality": [], "complexity": [], "style": []
        }
        for issues in [self.critical, self.high, self.medium, self.low]:
            for issue in issues:
                cats[issue.category].append(issue)
        return cats

