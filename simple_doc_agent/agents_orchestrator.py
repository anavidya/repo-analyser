"""Simple Documentation Agents - No LLM needed"""


from models import Documentation

from all_agents.repository_analyser import RepositoryFetcher
from all_agents.python_files_analyzer import PythonAnalyzer
from all_agents.docker_files_analyser import DockerAnalyzer
from all_agents.CICD_analyser import CICDAnalyzer
from all_agents.document_generator import DocumentationGenerator
from all_agents.security_analyser import analyse_security
from all_agents.test_coverage_analyzer import RepositoryTestCoverageFetcher
from all_agents.review_agent import CodeReviewAgent
from playwright.sync_api import sync_playwright
from all_agents.constants import PDF_STYLES, PDF_TAB_ORDER


def reference_constructor(loader, node):
        return loader.construct_sequence(node) 

class DocumentationOrchestrator:
    """Orchestrates all agents in sequence"""
    
    def __init__(self, url: str, token: str, platform: str = "gitlab"):
        self.fetcher = RepositoryFetcher(url, token, platform)
        self.python_analyzer = PythonAnalyzer()
        self.docker_analyzer = DockerAnalyzer()
        self.cicd_analyzer = CICDAnalyzer()
        self.test_coverage_analyzer = RepositoryTestCoverageFetcher()
        self.generator = DocumentationGenerator()
        self.reviewer = CodeReviewAgent()
    
    def save_as_pdf(self, html_content, output_path):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content, wait_until="networkidle")
            # Show all tab content before capturing
            page.evaluate(f"""
            document.querySelectorAll('.tabcontent').forEach(el => {{
                el.style.display = 'block';
            }});

            document.querySelector('.tabs').style.display = 'none';

            const style = document.createElement('style');
            style.textContent = `{PDF_STYLES}`;
            document.head.appendChild(style);

            const tabOrder = {PDF_TAB_ORDER};
            tabOrder.forEach(id => {{
                const el = document.getElementById(id);
                if (el) document.body.appendChild(el);
            }});
            """)

        # Wait for Mermaid diagrams to render
            page.wait_for_timeout(2000)
            page.pdf(
                path=output_path,
                format="A4",
                margin={"top": "0.75in", "right": "0.75in", 
                        "bottom": "0.75in", "left": "0.75in"}
            )
            browser.close()
            print(f"Report saved successfully to {output_path}")
    def run(self, project_id: str) -> str:
        """Run the complete agent flow"""
        
        print("\n🤖 Starting Documentation Agent Flow...\n")
        
        # Agent 1: Fetch files
        print("📥 Agent 1: Fetching repository files...")
        files, project, ref = self.fetcher.fetch(project_id)
        
        # Agent 2: Analyze Python
        print("🐍 Agent 2: Analyzing Python code...")
        python_metadata = self.python_analyzer.analyze(files)
        
        # Agent 3: Analyze Docker
        print("🐳 Agent 3: Analyzing Dockerfile...")
        docker_files_with_content = {
            name: content
            for name, content in files.items()
            if any(k in name.lower() for k in ("docker", "compose"))
        }
        docker_metadata = self.docker_analyzer.analyze(docker_files_with_content)
        
        # Agent 4: Analyze CI/CD
        print("⚙️  Agent 4: Analyzing CI/CD pipeline...")
        cicd_yml = files.get('.gitlab-ci.yml') or files.get('.github/workflows')
        cicd_metadata = self.cicd_analyzer.analyze(cicd_yml) if cicd_yml else None
        
        # Agent 5: Generate mermaid code
        print("🧜 Agent 5: Generating mermaid code...")
        mermaid_code = self.python_analyzer.generate_mermaid(python_metadata.docstrings)
        metadata = Documentation(
            python=python_metadata,
            docker=docker_metadata,
            cicd=cicd_metadata,
            mermaid=mermaid_code
        )
         # Agent 6: analysing security
        print("🔒 Agent 6: analysing security")
        findings = analyse_security(metadata)
        
        # Agent 7: Analyze test coverage
        print("🔬 Agent 7: Analyzing test Coverage...")
        test_coverage = self.test_coverage_analyzer.get_latest_tag_coverage(project)

        # Agent 8: Review the code
        print("🔨 Agent 8: Reviewing the python code")
        review_result = self.reviewer.run(files)


        docs, md_docs = self.generator.generate(metadata, findings, test_coverage, review_result)
        
        print("\n✅ Documentation generated successfully!\n")
        
        return docs, md_docs, findings, test_coverage, review_result