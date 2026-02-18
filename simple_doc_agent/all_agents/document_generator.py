"""Simple Documentation generator"""
from dataclasses import asdict
from jinja2 import Environment, FileSystemLoader
import markdown
from models import Documentation, TestCoverage

class DocumentationGenerator:
    """Generates final documentation"""
    
    def __init__(self, templates_dir: str = './templates'):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
    
    def generate(self, metadata: Documentation, findings:list, coverage:TestCoverage, review_result:dict) -> str:
        """Generate markdown documentation"""
        
        template_html = self.env.get_template('docs.html.j2')
        template_md = self.env.get_template('docs.md.j2')
        # Convert dataclasses to dicts for template
        context = {
            'python': asdict(metadata.python),
            'docker': [asdict(d) for d in metadata.docker],
            'cicd': asdict(metadata.cicd),
            'mermaid': metadata.mermaid,
            'security_findings':findings,
            'test_coverage':asdict(coverage),
            'review_results': review_result
        }
        
        markdown_only_content = template_md.render(**context)
        markdown_html_content = template_html.render(**context)
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_html_content, extensions=['tables', "fenced_code"])
        
        return html_content, markdown_only_content

