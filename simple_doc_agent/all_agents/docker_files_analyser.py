"""Simple Docker Files Analyser"""
import yaml
from pathlib import Path
from dataclasses import asdict
from gitlab import Gitlab
from models import DockerMetadata

class DockerAnalyzer:
    """Analyzes Dockerfile"""
    
    def analyze(self, dockerfiles: dict[str, str]) -> list[DockerMetadata]:

        """Extract Docker metadata"""
        results = []
        for filename, content in dockerfiles.items():
            base_image = "unknown"
            exposed_ports = []
            volumes = []
            env_vars = []
            workdir = "/app"
            entrypoint=""

            if 'compose' in filename:
                env_vars=(self.extract_compose_env_vars(content))
            else:
                for line in content.split('\n'):
                    line = line.strip()
                    
                    if line.startswith('FROM '):
                        base_image = line.split('FROM ')[1].split(' ')[0]
                    
                    elif line.startswith('EXPOSE '):
                        ports = line.split('EXPOSE ')[1].split()
                        exposed_ports.extend(ports)
                    
                    elif line.startswith('VOLUME '):
                        vol = line.split('VOLUME ')[1].strip('[]"\'')
                        volumes.append(vol)
                    
                    elif line.startswith('ENV '):
                        # Handle multiple variables in one line
                        parts = line[4:].split()
                        for part in parts:
                            if '=' in part:
                                env_vars.append(part)
                    
                    elif line.startswith('WORKDIR '):
                        workdir = line.split('WORKDIR ')[1]
                    elif line.startswith('ENTRYPOINT '):
                        entrypoint = line.split('ENTRYPOINT ')[1]
                
            
        
            results.append(
                DockerMetadata(
                    filename=filename,
                    base_image=base_image,
                    exposed_ports=exposed_ports,
                    volumes=volumes,
                    workdir=workdir,
                    entrypoint=entrypoint,
                    env_vars=env_vars,
                    
                )
        )
        return results

    def parse_env_file(self, path: str) -> list[str]:
        vars = []
        try:
            for line in Path(path).read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    vars.append(line)
        except FileNotFoundError:
            pass 
        return vars

    def extract_compose_env_vars(self, content: str) -> list[str]:
        data = yaml.safe_load(content)
        env_vars = []

        services = data.get("services", {})
        for service_name, service in services.items():

            # environment: { KEY: value }
            env = service.get("environment", {})
            if isinstance(env, dict):
                for k, v in env.items():
                    env_vars.append(f"{k}={v}")

            # environment: [ KEY=value ]
            elif isinstance(env, list):
                for item in env:
                    if isinstance(item, str) and "=" in item:
                        env_vars.append(item)

            # env_file: [.env, secrets.env]
            env_files = service.get("env_file", [])
            if isinstance(env_files, str):
                env_files = [env_files]

            for env_file in env_files:
                env_vars.extend(self.parse_env_file(env_file))

        return env_vars