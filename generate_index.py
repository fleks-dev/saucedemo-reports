import os
import re
from datetime import datetime

# Configuration
REPORTS_DIR = "reports"
README_FILE = "README.md"
REPO_URL_BASE = "https://fleks-dev.github.io/saucedemo-reports"
MAX_REPORTS = 10
MARKER_START = "<!-- REPORT_LINKS_START -->"
MARKER_END = "<!-- REPORT_LINKS_END -->"

def get_reports(reports_dir):
    reports = []
    # Walk through the reports directory
    # Expected structure: reports/YYYY-MM-DD/FEATURE/RUN_ID
    if not os.path.exists(reports_dir):
        print(f"Directory {reports_dir} does not exist.")
        return []

    for date_str in os.listdir(reports_dir):
        date_path = os.path.join(reports_dir, date_str)
        if not os.path.isdir(date_path):
            continue
        
        # Validate date format YYYY-MM-DD
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            continue

        for feature_name in os.listdir(date_path):
            feature_path = os.path.join(date_path, feature_name)
            if not os.path.isdir(feature_path):
                continue

            for run_id in os.listdir(feature_path):
                run_path = os.path.join(feature_path, run_id)
                if not os.path.isdir(run_path):
                    continue
                
                # Check for index.html to confirm it's a report
                # if not os.path.exists(os.path.join(run_path, "index.html")):
                #    continue 
                # Relaxed check: just assume folder is a report for now, or check for index.html if strict.
                
                reports.append({
                    "date": date_obj,
                    "date_str": date_str,
                    "feature": feature_name,
                    "run_id": run_id,
                    "path": f"{REPORTS_DIR}/{date_str}/{feature_name}/{run_id}/index.html"
                })

    return reports

def sort_reports(reports):
    # Sort by date (desc), then run_id (desc, assuming numeric or lexicographical is fine, usually higher ID is newer)
    # Run ID is numeric in GitHub Actions, so let's try to parse it as int if possible for better sorting
    def sort_key(r):
        try:
            run_id_int = int(r["run_id"])
        except ValueError:
            run_id_int = 0
        return (r["date"], run_id_int)

    return sorted(reports, key=sort_key, reverse=True)

def generate_markdown(reports):
    lines = [MARKER_START, "### Latest Test Reports", ""]
    lines.append("| Date | Feature | Run ID | Link |")
    lines.append("|---|---|---|---|")
    
    for r in reports[:MAX_REPORTS]:
        link = f"{REPO_URL_BASE}/{r['path']}"
        lines.append(f"| {r['date_str']} | {r['feature']} | {r['run_id']} | [View Report]({link}) |")
    
    lines.append("")
    lines.append(MARKER_END)
    return "\n".join(lines)

def update_readme(readme_path, new_content):
    if not os.path.exists(readme_path):
        # Create if not exists
        with open(readme_path, "w") as f:
            f.write(f"# Reports\n\n{new_content}\n")
        return

    with open(readme_path, "r") as f:
        content = f.read()

    # Regex to find existing block
    pattern = re.compile(f"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}", re.DOTALL)
    
    if pattern.search(content):
        updated_content = pattern.sub(new_content, content)
    else:
        # Append to end if not found
        updated_content = content + "\n\n" + new_content

    with open(readme_path, "w") as f:
        f.write(updated_content)

def main():
    reports = get_reports(REPORTS_DIR)
    sorted_reports = sort_reports(reports)
    markdown_content = generate_markdown(sorted_reports)
    update_readme(README_FILE, markdown_content)
    print(f"Updated {README_FILE} with {min(len(sorted_reports), MAX_REPORTS)} reports.")

if __name__ == "__main__":
    main()
