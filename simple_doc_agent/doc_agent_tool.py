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

load_dotenv()
output_dir = os.getenv("OUTPUT_DIR")

def run(repo_project_path: str, output_dir: str = "docs") -> dict:
    started_at = datetime.utcnow().isoformat()

    gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
    gitlab_token = os.getenv("GITLAB_TOKEN")
    namespace = os.getenv("GITLAB_NAMESPACE","nocacuk/BODC/software")

    repo_project_full_path = f"{namespace}/{repo_project_path}" 
    print(f"\n🔗 Connecting to: {gitlab_url}")
    print(f"📦 Analyzing project: {repo_project_full_path}\n")

    if not gitlab_token:
        raise RuntimeError(
            "GITLAB_TOKEN not set. Agent requires non-interactive credentials."
        )

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    orchestrator = DocumentationOrchestrator(
        gitlab_url=gitlab_url,
        gitlab_token=gitlab_token,
    )
    
    html_docs, md_docs, security_issues, test_coverage, review_result = orchestrator.run(repo_project_full_path)
    outputfilename = Path(repo_project_path).name
    html_path = output_dir / f"{outputfilename}.html"
    md_path = output_dir / f"{outputfilename}.md"

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
        "Test Coverage":asdict(test_coverage),
        "review results":asdict(review_result),
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
