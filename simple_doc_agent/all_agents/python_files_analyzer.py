"""Simple Documentation Agents - No LLM needed"""
import os
import ast
import tomli
from pathlib import Path
from typing import Dict, List

from gitlab import Gitlab
import markdown
import re
from models import PythonMetadata, Command


class PythonAnalyzer:
    """Analyzes Python code structure"""
    
    def analyze(self, files: Dict[str, str]) -> PythonMetadata:
        """Extract Python metadata"""
        
        # Parse pyproject.toml
        pyproject = tomli.loads(files.get('pyproject.toml', ''))
        # PEP 621 / uv / hatch format
        if 'project' in pyproject:
            project = pyproject['project']
            project_name = project.get('name', 'unknown')
            python_version = project.get('requires-python', '3.10+')

            raw_deps = project.get('dependencies', [])
            dependencies = []
            for dep in raw_deps:
                # deps are strings like "xarray>=2025.11.0"
                for op in ['>=', '<=', '==', '~=', '!=', '>','<']:
                    if op in dep:
                        name, version = dep.split(op, 1)
                        dependencies.append({
                            "name": name.strip(),
                            "version": f"{op}{version.strip()}",
                            "raw": dep,
                        })
                        break
                else:
                    dependencies.append({"name": dep.strip(), "version": None, "raw": dep})

            # optional dependencies
            optional_deps = project.get('optional-dependencies', {})
            for group, deps in optional_deps.items():
                for dep in deps:
                    dependencies.append({"name": dep.strip(), "version": None, "raw": dep, "group": group})

        # Poetry format
        elif 'tool' in pyproject and 'poetry' in pyproject.get('tool', {}):
            poetry = pyproject['tool']['poetry']
            project_name = poetry.get('name', 'unknown')
            python_version = poetry.get('dependencies', {}).get('python', '3.10+')
            dependencies = [
                {
                    "name": name,
                    "version": spec.get("version") if isinstance(spec, dict) else spec,
                    "raw": spec,
                }
                for name, spec in poetry.get('dependencies', {}).items()
                if name != "python"
            ]

        else:
            project_name = 'unknown'
            python_version = '3.10+'
            dependencies = []
        # Extract CLI commands if Click is used
        commands = []
        if any(dep["name"] == "click" for dep in dependencies):
            commands = self._extract_click_commands(files)
        
        # Find entry points
        entry_points = self._find_entry_points(pyproject)
        all_docstrings = {}
        for filepath, content in files.items():
            if filepath.endswith('.py'):
                docstrings = self._extract_docstrings(content, filepath)
                all_docstrings.update(docstrings)

        readme_raw = self._extract_readme(files)
        readme_html = markdown.markdown(readme_raw, extensions=["fenced_code", "tables"]) if readme_raw else None
        return PythonMetadata(
            project_name=project_name,
            python_version=python_version,
            dependencies=dependencies,
            commands=commands,
            entry_points=entry_points,
            docstrings=all_docstrings,
            readme_raw=readme_raw,
            readme_html=readme_html
        )
    def generate_mermaid(self, all_docstrings: dict) -> str:
        """
        Generate Mermaid diagram code for Python modules, classes, and functions.
        """
        blocks = []

        for filepath, docs in all_docstrings.items():
            lines = ["flowchart TB"]

            # Safe module node ID
            module_id = re.sub(r'\W+', '_', filepath)
            module_label = f"Module: {filepath.split('/')[-1]}"
            lines.append(f'{module_id}["{module_label}"]')

            for doc in docs:
                # Safe node ID
                safe_name = re.sub(r'\W+', '_', doc["name"])
                node_id = f"{module_id}_{safe_name}"

                if doc["type"] == "ClassDef":
                    lines.append(f'{node_id}["Class: {doc["name"]}"]')
                    lines.append(f'{module_id} --> {node_id}')
                elif doc["type"] == "FunctionDef":
                    lines.append(f'{node_id}["Function: {doc["name"]}"]')
                    lines.append(f'{module_id} --> {node_id}')

            # Join lines and wrap in div
            content = "\n".join(lines)
            block = f'<div class ="mermaid-container"> <pre class="mermaid">\n{content}\n</pre></div>'
            blocks.append(block)
        return "\n\n".join(blocks)
        


    def _extract_click_commands(self, files: Dict[str, str]) -> List[Command]:
        """Extract Click CLI commands from Python files"""
        commands = []
        
        # Look through Python files for @click.command decorators
        for filepath in files.get('python_files', []):
            if 'cli' in filepath.lower() or 'main' in filepath.lower():
                # Would need to fetch actual file content here
                # For now, simplified
                pass
        
        return commands
    
    def _find_entry_points(self, pyproject: dict) -> List[str]:
        """Find script entry points"""
        scripts = pyproject.get('tool', {}).get('poetry', {}).get('scripts', {})
        return list(scripts.keys())

    def _extract_docstrings(self, content: str, filepath: str) -> Dict[str, List[Dict[str, str]]]:
        """Extract module, class, and function docstrings from a Python file"""
        docstrings = {}

        try:
            tree = ast.parse(content)
            file_docs = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                    doc = ast.get_docstring(node)
                    if doc:
                        file_docs.append({
                            "type": type(node).__name__,
                            "name": getattr(node, 'name', '<module>'),
                            "doc": doc
                        })
            if file_docs:
                docstrings[filepath] = file_docs
        except Exception as e:
            # skip unparsable filess
            print(f"⚠ Could not parse {filepath}: {e}")
        
        return docstrings

    def _extract_readme(self, files: Dict[str, str]) -> list[str|None]:
        for name in files:
            lower = name.lower()
            if lower in ("readme.md", "readme.rst", "readme.txt"):
                return files[name]
        return None
    