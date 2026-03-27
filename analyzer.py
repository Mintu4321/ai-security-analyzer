import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
# from parser import parse_trivy_report
import json
from dotenv import load_dotenv

load_dotenv()

REPORT_FILE = os.getenv("REPORT_PATH", "trivy-report.json")


def parse_trivy_report(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    vulnerabilities = []

    for result in data.get("Results", []):
        for v in result.get("Vulnerabilities", []):
            vulnerabilities.append({
                "package": v.get("PkgName"),
                "severity": v.get("Severity"),
                "description": v.get("Description"),
                "fix_version": v.get("FixedVersion"),
                "file": result.get("Target")
            })

    return vulnerabilities

def analyze_vulnerabilities():

    vulns = parse_trivy_report(REPORT_FILE)

    if not vulns:
        return "✅ No vulnerabilities found. Good job!"

    # Filter important ones
    filtered = [v for v in vulns if v["severity"] in ["HIGH", "CRITICAL"]]

    template = """
You are a senior security engineer.

Analyze the vulnerabilities below:

{vulns}

For each vulnerability:
- Explain the issue simply
- Mention severity
- Suggest exact fix (version upgrade or code change)
- Give short actionable recommendation

Output clean markdown.
"""

    prompt = PromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_retries=3,
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    response = llm.invoke(prompt.format(vulns=filtered))

    return response.content


if __name__ == "__main__":

    result = analyze_vulnerabilities()
    print(result)

    with open("ai-output.txt", "w") as f:
        f.write(result)
