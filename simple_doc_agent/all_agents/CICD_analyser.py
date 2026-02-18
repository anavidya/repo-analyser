"""Simple Documentation Agents - No LLM needed"""

import yaml

from models import CICDMetadata

def reference_constructor(loader, node):
        return loader.construct_sequence(node) 
class CICDAnalyzer:
    """Analyzes GitLab CI/CD pipeline"""
    
    def analyze(self, gitlab_ci_content: str) -> CICDMetadata:
        """Extract CI/CD metadata"""
        yaml.SafeLoader.add_constructor('!reference', reference_constructor)
        config = yaml.safe_load(gitlab_ci_content)
        
        # Extract stages
        stages = config.get('stages', [])
        # Extract global variables
        global_variables = config.get('variables', {})
        #Extract included files
        files_from_runners= [entry['file'] for entry in config.get('include', [])]
        # Extract jobs
        jobs = []
        for key, value in config.items():
            if isinstance(value, dict) and 'stage' in value:
                job = {
                    'name': key,
                    'stage': value.get('stage'),
                    'image': value.get('image', 'default'),
                    'script_lines': len(value.get('script', [])),
                    'tags': value.get('tags', []),
                    'only': value.get('only', []),
                    'when': value.get('when', 'on_success'),
                    'artifacts': bool(value.get('artifacts'))
                }
                if isinstance(job['stage'], str) and job['stage'].startswith('!reference'):
                    # Extract the reference
                    ref = job['stage'].split("[")[1].split("]")[0].split(",")[-1].strip()
                    job['stage'] = ref
                jobs.append(job)
        
        return CICDMetadata(
            stages=stages,
            global_variables=global_variables,
            files_from_runners=files_from_runners,
            jobs=jobs
        )
