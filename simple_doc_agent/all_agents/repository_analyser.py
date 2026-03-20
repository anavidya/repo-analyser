"""Simple Repository Fetcher"""
from pathlib import Path
from typing import Dict, List
from dataclasses import asdict
from gitlab import Gitlab
from github import Github


class RepositoryFetcher:
    """Fetches repository files"""
    
    def __init__(self, url: str, token: str, platform: str = "gitlab"):
        self.platform = platform
        self.token = token
        self.url = url

        if platform == "github":
            self.client = Github(token)
        else:
            self.client = Gitlab(url, private_token=token)
    
    def fetch(self, project_path: str) -> Dict[str, str]:
        """Fetch key files from repository"""
        if self.platform == "github":
            return self._fetch_github(project_path)
        return self._fetch_gitlab(project_path)
        
    def _fetch_gitlab(self, project_path: str) -> Dict[str, str]:
        """Fetch key files from GitLab repository"""
        project = self.client.projects.get(project_path)
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


    def _fetch_github(self, project_path: str) -> Dict[str, str]:
        """Fetch key files from GitHub repository"""
        if "github.com" in project_path:
            project_path = project_path.split("github.com/")[-1].strip("/")
        repo = self.client.get_repo(project_path)
        ref = repo.default_branch

        files = {}
        file_list = [
            'pyproject.toml',
            '.github/workflows',
            'README.md',
            'README.rst'
        ]
        for filename in file_list:
            try:
                content = repo.get_contents(filename, ref=ref)
                files[filename] = content.decoded_content.decode('utf-8')
            except Exception as e:
                print(f"✗ Could not fetch {filename}: {e}")

        python_files = self._get_python_files_github(repo, ref)
        docker_file_paths = self._get_docker_files_github(repo, ref)
      
        for df in docker_file_paths:
            try:
                content = repo.get_contents(df, ref=ref)
                files[df] = content.decoded_content.decode('utf-8')
                print(f"✓ Fetched Dockerfile: {df}")
            except Exception as e:
                print(f"✗ Could not fetch Dockerfile {df}: {e}")

        for pf in python_files:
            try:
                content = repo.get_contents(pf, ref=ref)
                files[pf] = content.decoded_content.decode('utf-8')
            except Exception as e:
                print(f"✗ Could not fetch Python file {pf}: {e}")

        return files, repo, ref


    def _get_python_files_github(self, repo, ref: str) -> list:
        """Recursively get Python files from GitHub repo"""
        python_files = []
        try:
            tree = repo.get_git_tree(ref, recursive=True)
            python_files = [
                item.path for item in tree.tree
                if item.path.endswith('.py') and item.type == 'blob'
            ]
        except Exception as e:
            print(f"✗ Could not list Python files: {e}")
        return python_files


    def _get_docker_files_github(self, repo, ref: str) -> list:
        """Recursively get Dockerfiles from GitHub repo"""
        docker_files = []
        try:
            tree = repo.get_git_tree(ref, recursive=True)
            docker_files = [
                item.path for item in tree.tree
                if 'dockerfile' in item.path.lower() and item.type == 'blob'
            ]
        except Exception as e:
            print(f"✗ Could not list Dockerfiles: {e}")
        return docker_files
            
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