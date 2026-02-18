""" A agemt to check test coverage from the latest pipeline on main"""
from gitlab.v4.objects.projects import Project
import xml.etree.ElementTree as ET
import re
import io
import zipfile
from models import TestCoverage

class RepositoryTestCoverageFetcher:
    """Fetches repository files"""
    def get_latest_coverage(self, project: Project, ref: str):
            overall_coverage = "0.0%"
            pipelines = project.pipelines.list(ref=ref, status='success', per_page=1, get_all=False)
        
            if pipelines:
                # We need to fetch the 'full' pipeline object to get the coverage attribute
                latest_pipeline = project.pipelines.get(pipelines[0].id)
                jobs = latest_pipeline.jobs.list()
                test_job = next((j for j in jobs if j.name in ['test', 'pytest', 'unit-tests']), None)

                if latest_pipeline.coverage:
                    overall_coverage = f"{float(latest_pipeline.coverage):.2f}%"
                if not test_job:
                    return TestCoverage(test_coverage=[], summary_coverage=overall_coverage)
                
                if test_job:
                    try:
                        # 3. Download and unzip the coverage.xml artifact
                        job_obj = project.jobs.get(test_job.id)
                        log_text = job_obj.trace().decode('utf-8')
                        table_pattern = re.compile(r'^([\w\-/]+\.py)\s+\d+\s+\d+\s+(\d+)%', re.MULTILINE)
                        detailed_coverage = []
                        for match in table_pattern.finditer(log_text):
                            filename, percent = match.groups()
                            detailed_coverage.append({
                                "name": filename,
                                "line_rate": float(percent),
                                "branch_rate": 0.0  # Log doesn't show branch rate, so we default to 0
                            })

                        # 5. Extract the TOTAL
                        total_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', log_text)
                        overall_coverage = f"{total_match.group(1)}%" if total_match else "0.0%"

                    except Exception as e:
                        print(f"Error retrieving artifacts: {e}")

            # Return a tuple so you have the summary AND the details
            return TestCoverage(test_coverage=detailed_coverage, summary_coverage=overall_coverage)

    def get_latest_tag_coverage(self, project: Project) -> str:
        # 1. Get all tags, sorted by creation (GitLab returns latest first by default)
        tags = project.tags.list(get_all=False, per_page=50)
        
        if not tags:
            return "No tags found"

        # 2. Find the latest tag that matches the version pattern vD.D.D
        version_pattern = re.compile(r'^v?\d+\.\d+\.\d+$')
        latest_version_tag = None
        
        for tag in tags:
            if version_pattern.match(tag.name):
                latest_version_tag = tag.name
                break
                
        if not latest_version_tag:
            # Fallback to the absolute latest tag if no version pattern matches
            latest_version_tag = tags[0].name

        # 3. Use your existing logic but pass the tag name as the 'ref'
        return self.get_latest_coverage(project, ref=latest_version_tag)

    def get_coverage_data(self, xml_string):
        if not xml_string:
            return []
        
        root = ET.fromstring(xml_string)
        file_data = []
        
        # Cobertura format usually stores files in <class> tags
        for cls in root.findall(".//class"):
            file_data.append({
                "name": cls.get("filename"),
                "line_rate": round(float(cls.get("line-rate")) * 100, 2),
                "branch_rate": round(float(cls.get("branch-rate", 0)) * 100, 2)
            })
        return file_data