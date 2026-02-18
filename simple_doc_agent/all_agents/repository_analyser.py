"""Simple Repository Fetcher"""
from pathlib import Path
from typing import Dict, List
from dataclasses import asdict
from gitlab import Gitlab


class RepositoryFetcher:
    """Fetches repository files"""
    
    def __init__(self, gitlab_url: str, token: str):
        self.gl = Gitlab(gitlab_url, private_token=token)
    
    def fetch(self, project_path: str) -> Dict[str, str]:
        """Fetch key files from repository"""
        project = self.gl.projects.get(project_path)
        branches = [b.name for b in project.branches.list()]
        ref = 'main' if 'main' in branches else ('master' if 'master' in branches else branches[0])

        files = {}
        file_list = [
            'pyproject.toml',
            '.gitlab-ci.yml',
            'README.md',
            'README.rst'
        ]
        
        for filename in file_list:
            try:
                file = project.files.get(file_path=filename, ref=ref)
                files[filename] = file.decode().decode('utf-8')
            except Exception as e:
                print(f"✗ Could not fetch {filename}: {e}")
        
        # Also get Python files for entry point detection
        python_files = self._get_python_files(project)
        docker_file_paths = self._get_docker_files(project)

        for df in docker_file_paths:
            try:
                file = project.files.get(file_path=df, ref=ref)
                files[df] = file.decode().decode('utf-8')
                print(f"✓ Fetched Dockerfile: {df}")
            except Exception as e:
                print(f"✗ Could not fetch Dockerfile {df}: {e}")
        for pf in python_files:
            try:
                file = project.files.get(file_path=pf, ref=ref)
                files[pf] = file.decode().decode('utf-8')
            except Exception as e:
                print(f"✗ Could not fetch Python File {pf}: {e}")
        return files, project, ref
        
    def _get_python_files(self, project) -> List[str]:
        """Get all Python files in src/ or root"""
        python_files = []
        
        try:
            tree = project.repository_tree(recursive=True, get_all=True)
            for item in tree:
                if item['path'].endswith('.py'):
                    python_files.append(item['path'])
        except Exception as e:
            print(f"Warning: Could not get file tree: {e}")
        
        return python_files
    
    def _get_docker_files(self, project) -> List[str]:
        """Get all docker files in src/ or root"""
        docker_files = []
        
        try:
            tree = project.repository_tree(recursive=True, get_all=True)
            for item in tree:
                path = item["path"].lower()
                if "dockerfile" in path or "compose" in path:
                    docker_files.append(item['path'])
        except Exception as e:
            print(f"Warning: Could not get file tree: {e}")
        
        return docker_files