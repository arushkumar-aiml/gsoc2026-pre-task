import requests
from datetime import datetime

def get_repo_data(owner, repo, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"  ERROR: Repository not found.")
        return None
    elif response.status_code == 403:
        print(f"  ERROR: API rate limit exceeded.")
        return None
    else:
        print(f"  ERROR: Status code {response.status_code}")
        return None

def get_commit_count(owner, repo, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        if 'Link' in response.headers:
            link = response.headers['Link']
            last_page = [x for x in link.split(',') if 'last' in x]
            if last_page:
                page_num = last_page[0].split('page=')[-1].split('>')[0]
                return int(page_num)
    return 0

def calculate_activity_score(data, commits):
    stars      = data.get("stargazers_count", 0)
    forks      = data.get("forks_count", 0)
    open_issues = data.get("open_issues_count", 0)
    watchers   = data.get("watchers_count", 0)

    score = (stars * 0.3) + (forks * 0.3) + \
            (open_issues * 0.2) + (commits * 0.1) + \
            (watchers * 0.1)
    return round(score, 2)

def estimate_complexity(data):
    size        = data.get("size", 0)
    open_issues = data.get("open_issues_count", 0)
    language    = data.get("language", "")
    
    complexity_score = 0
    
    if size > 10000:
        complexity_score += 3
    elif size > 2000:
        complexity_score += 2
    else:
        complexity_score += 1

    if open_issues > 100:
        complexity_score += 3
    elif open_issues > 20:
        complexity_score += 2
    else:
        complexity_score += 1

    hard_langs = ["C", "C++", "Rust", "Assembly"]
    if language in hard_langs:
        complexity_score += 2
    else:
        complexity_score += 1

    return complexity_score

def classify_difficulty(complexity_score):
    if complexity_score <= 4:
        return "Beginner"
    elif complexity_score <= 7:
        return "Intermediate"
    else:
        return "Advanced"

def analyze_repo(repo_url, token=None):
    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo  = parts[-1]

    print(f"  Fetching data...")
    data = get_repo_data(owner, repo, token)
    if not data:
        return None

    commits = get_commit_count(owner, repo, token)
    complexity_score = estimate_complexity(data)
    difficulty = classify_difficulty(complexity_score)
    activity   = calculate_activity_score(data, commits)

    report = {
        "Repository"      : data.get("full_name", "N/A"),
        "Language"        : data.get("language", "N/A"),
        "Stars"           : data.get("stargazers_count", 0),
        "Forks"           : data.get("forks_count", 0),
        "Open Issues"     : data.get("open_issues_count", 0),
        "Watchers"        : data.get("watchers_count", 0),
        "Commits (approx)": commits,
        "Size (KB)"       : data.get("size", 0),
        "Activity Score"  : activity,
        "Complexity Score": complexity_score,
        "Difficulty"      : difficulty,
    }
    return report

def print_report(report):
    print()
    print("-" * 50)
    for key, value in report.items():
        print(f"  {key:<25}: {value}")
    print("-" * 50)

def main():
    repos = [
        "https://github.com/c2siorg/Webiu",
        "https://github.com/numpy/numpy",
        "https://github.com/psf/requests",
        "https://github.com/pallets/flask",
        "https://github.com/scikit-learn/scikit-learn",
    ]

    print("=" * 50)
    print("  GitHub Repository Intelligence Analyzer")
    print("  Built by Arush Kumar — GSoC 2026 C2SI")
    print("=" * 50)

    results = []
    for repo_url in repos:
        print(f"\nAnalyzing: {repo_url}")
        report = analyze_repo(repo_url)
        if report:
            print_report(report)
            results.append(report)

    print("\n" + "=" * 50)
    print("  SUMMARY")
    print("=" * 50)
    print(f"  Total repos analyzed : {len(results)}")
    
    if results:
        easiest = min(results, key=lambda x: x["Complexity Score"])
        hardest = max(results, key=lambda x: x["Complexity Score"])
        most_active = max(results, key=lambda x: x["Activity Score"])
        
        print(f"  Easiest repo         : {easiest['Repository']}")
        print(f"  Hardest repo         : {hardest['Repository']}")
        print(f"  Most active repo     : {most_active['Repository']}")
    
    print("=" * 50)
    print("  Analysis Complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
