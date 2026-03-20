#!/usr/bin/env python3
"""
Documentation Agent Tool

Reads a GitLab repository and generates Markdown + HTML documentation.
Writes ONLY to docs/.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

from agents_orchestrator import DocumentationOrchestrator


from dotenv import load_dotenv
from dataclasses import is_dataclass

load_dotenv()
output_dir = os.getenv("OUTPUT_DIR")

def detect_platform(repo_url: str) -> str:
    """Detect if the URL is GitHub or GitLab."""
    if "github.com" in repo_url:
        return "github"
    return "gitlab"

def run(repo_project_path: str, output_dir: str = "docs") -> dict:
    started_at = datetime.utcnow().isoformat()
    platform = detect_platform(repo_project_path)

    if platform == "github":
        repo_url = os.getenv("GITHUB_URL", "https://github.com")
        token = os.getenv("GITHUB_TOKEN")
        namespace = os.getenv("GITHUB_NAMESPACE", "")
        platform_label = "GitHub"
    else:
        repo_url = os.getenv("GITLAB_URL", "https://gitlab.com")
        token = os.getenv("GITLAB_TOKEN")
        namespace = os.getenv("GITLAB_NAMESPACE", "nocacuk/BODC/software")
        platform_label = "GitLab"
        #gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
        #gitlab_token = os.getenv("GITLAB_TOKEN")
        #namespace = os.getenv("GITLAB_NAMESPACE","nocacuk/BODC/software")
    if not token:
        raise RuntimeError(
            f"{platform_label.upper()}_TOKEN not set. Agent requires non-interactive credentials."
        )

    repo_project_full_path = f"{namespace}/{repo_project_path}" if namespace else repo_project_path
    #repo_project_full_path = f"{namespace}/{repo_project_path}" 
    print(f"\n🔗 Connecting to: {repo_url} ({platform_label})")
    print(f"📦 Analyzing project: {repo_project_full_path}\n")

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    orchestrator = DocumentationOrchestrator(
        url=repo_url,
        token=token,
        platform=platform,
    )
    
    html_docs, md_docs, security_issues, test_coverage, review_result = orchestrator.run(repo_project_full_path)
    outputfilename = Path(repo_project_path).name
    html_path = output_dir / f"{outputfilename}.html"
    md_path = output_dir / f"{outputfilename}.md"
    pdf_path = output_dir / f"{outputfilename}.pdf"
    orchestrator.save_as_pdf(html_docs, pdf_path)

    html_path.write_text(html_docs, encoding="utf-8")
    md_path.write_text(md_docs, encoding="utf-8")

    finished_at = datetime.utcnow().isoformat()
    
    return {
        "agent": "docs-agent",
        "status": "success",
        "repo": repo_project_path,
        "output_dir": str(output_dir),
        "files_written": [
            str(html_path),
            str(md_path),
        ],
        "Security issues":security_issues,
        "Test Coverage":asdict(test_coverage) if is_dataclass(test_coverage) else {},
        "review results":asdict(review_result) if is_dataclass(test_coverage) else {},
        "started_at": started_at,
        "finished_at": finished_at,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: run.py <gitlab-namespace/project>", file=sys.stderr)
        sys.exit(1)

    try:
        result = run(sys.argv[1])
        print(json.dumps(result, indent=2))
    except Exception as e:
        error = {
            "agent": "docs-agent",
            "status": "error",
            "error": str(e),
        }
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
