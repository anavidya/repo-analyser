#!/usr/bin/env python3
"""Simple Documentation Agent - Runner. This is version 1 when not using as agent"""
import os
import sys
from pathlib import Path
from agents_orchestrator import DocumentationOrchestrator
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_NAMESPACE = os.getenv('GITLAB_NAMESPACE', 'nocacuk/BODC/software')


def get_credentials():
    """Get GitLab credentials from environment or prompt"""
    
    # Try environment variables first
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    
    
    # If not set, try .env file
    if not gitlab_token:
        env_file = Path('.env')
        if env_file.exists():
            print("📋 Loading credentials from .env file...")
            from dotenv import load_dotenv
            load_dotenv()
            gitlab_token = os.getenv('GITLAB_TOKEN')
    
    # If still not set, prompt user
    if not gitlab_token:
        print("\n🔑 GitLab credentials not found in environment.")
        print("\nHow to get a token:")
        print("1. Go to GitLab → Preferences → Access Tokens")
        print("2. Create token with 'read_api' and 'read_repository' scopes")
        print("3. Copy the token\n")
        
        gitlab_token = input("Enter your GitLab personal access token: ").strip()
        
        if not gitlab_token:
            print("❌ Token is required!")
            sys.exit(1)
    
    return gitlab_url, gitlab_token

def main():
    # Get project ID from command line
    if len(sys.argv) < 2:
        print("Usage: python run.py <repo_path>")
        print("Example: python run.py British-Oceanographic-Data-Centre/APDS-Pusher")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    # Get credentials
    try:
        gitlab_url, gitlab_token = get_credentials()
    except Exception as e:
        print(f"❌ Error getting credentials: {e}")
        sys.exit(1)
    

    repo_project_path = f"{GITLAB_NAMESPACE}/{repo_path}" 
    print(f"\n🔗 Connecting to: {gitlab_url}")
    print(f"📦 Analyzing project: {repo_project_path}\n")
    # Run the orchestrator
    orchestrator = DocumentationOrchestrator(gitlab_url, gitlab_token)
    
    try:
        docs, md_docs, _= orchestrator.run(repo_project_path)
        outputfilename = Path(repo_project_path).name
        output_dir: str = "docs"
        html_path = output_dir / f"{outputfilename}.html"
        md_path = output_dir / f"{outputfilename}.md"
        # Save to file
        output_file = Path(html_path)
        output_file.write_text(docs)

         # Save to file
        output_md_file = Path(md_path)
        output_md_file.write_text(md_docs)
        
        print(f"📄 Documentation saved to: {output_file}")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()