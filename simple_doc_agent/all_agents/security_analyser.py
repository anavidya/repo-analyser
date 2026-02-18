from simple_doc_agent.all_agents.security_auditor import SecurityAnalyzer
from models import Documentation

def analyse_security(metadata:Documentation):
    analyzer = SecurityAnalyzer()
    findings = []
# Audit Docker (since your template shows docker is a list of DockerMetadata)
    for d_meta in metadata.docker:
        env_findings = analyzer.check_env_list(d_meta)
        if env_findings:
            findings.extend(env_findings)
        # Add port checks here too
        for port in d_meta.exposed_ports:
            if port.split('/')[0] in {'22', '3306', '5432'}:
                findings.append({
                    "filename":d_meta.filename,
                    "vulnerabilies": {
                        "type": "Insecure Port", 
                        "item": f"{d_meta.filename}:{port}", 
                        "risk": "MEDIUM",
                        "reason": "Database or SSH port exposed in Dockerfile"
                    }
                })

        # Audit CI/CD
        for k, v in metadata.cicd.global_variables.items():
            if any(risk in k.lower() for risk in analyzer.risk_keywords):
                if str(v).lower() not in analyzer.placeholders:
                    findings.append({
                        "filename": "CICD yaml",
                        "vulnerabilies": {
                            "type": "CI/CD Variable", 
                            "item": k, 
                            "risk": "CRITICAL",
                            "reason": "Sensitive variable name with hardcoded value"
                        }
                    })
    return findings