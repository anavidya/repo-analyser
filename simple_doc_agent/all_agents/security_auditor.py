import math
from typing import List, Dict, Any
from models import	Documentation, DockerMetadata

class SecurityAnalyzer:
    def __init__(self):
        # High risk keywords in variable names
        self.risk_keywords = {'key', 'secret', 'password', 'token', 'auth', 'pwd', 'credential', 'pass', 'RABBIT_PASS'}
        # Values that are clearly placeholders
        self.placeholders = {'true', 'false', 'none', 'null', 'default', 'change_me', 'todo'}

    def get_entropy(self, text: str) -> float:
        """Determines if a string is a random hash/key vs. a normal word."""
        if not text or len(text) < 5: return 0
        st = {c: text.count(c) / len(text) for c in set(text)}
        return -sum(p * math.log(p, 2) for p in st.values())

    def check_env_list(self, dockermetadata:DockerMetadata) -> List[Dict]:
        """Analyzes strings in format 'KEY=VALUE' or 'KEY'."""
        issues = []
        issue = {}
        env_list = dockermetadata.env_vars
        issuedetails = []
        
        for item in env_list:
            parts = item.split('=', 1)
            key = parts[0].lower()
            value = parts[1] if len(parts) > 1 else ""

            # Logic: If name is suspicious AND value isn't a known placeholder
            if any(k in key for k in self.risk_keywords):
                if value and value.lower() not in self.placeholders:
                    entropy = self.get_entropy(value)
                    # Anything above 3.5 entropy is likely a real leaked string
                    risk = "CRITICAL" if entropy > 3.7 else "WARNING"
                    issuedetails.append({"type": "Env Leak", "item": key, "risk": risk, "val_preview": f"{value[:3]}***"})
        if issuedetails:
            issue["filename"] = dockermetadata.filename
            issue["vulnerabilities"] = issuedetails
            issues.append(issue)

        return issues

    def audit(self, doc: Documentation) -> List[Dict]:
        findings = []

        # 1. Audit Docker Env Vars
        findings.extend(self.check_env_list(doc.docker))

        # 2. Audit CI/CD Global Variables
        # Since this is a Dict[str, Any], we iterate items directly
        for k, v in doc.cicd.global_variables.items():
            if any(risk in k.lower() for risk in self.risk_keywords):
                if str(v).lower() not in self.placeholders:
                    findings.append({"type": "CI/CD Variable", "item": k, "risk": "HIGH"})

        # 3. Audit Hardcoded Ports in Docker
        # Flagging non-standard/sensitive ports like 22 (SSH) or 3306 (DB)
        sensitive_ports = {'22', '3306', '5432', '27017'}
        for port in doc.docker.exposed_ports:
            p = port.split('/')[0] # handle '80/tcp'
            if p in sensitive_ports:
                findings.append({"type": "Insecure Port", "item": port, "risk": "MEDIUM"})

        return findings