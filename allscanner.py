import requests
import subprocess
import time

GITHUB_TOKEN = "ghp_REPLACE_THIS"  # 🔥 Your GitHub Token here
ORG_NAME = "digitalocean"  # 🎯 Target Org
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
DELAY = 1.5  # Rate-limit delay
TRUFFLEHOG_CMD = "trufflehog"

def get_paginated(url):
    results = []
    while url:
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"❌ Failed to fetch: {url} | Code: {r.status_code}")
            break
        results += r.json()
        url = r.links.get("next", {}).get("url")
        time.sleep(DELAY)
    return results

def get_org_repos(org):
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public"
    return [r["full_name"] for r in get_paginated(url)]

def get_org_members(org):
    url = f"https://api.github.com/orgs/{org}/members?per_page=100"
    return [u["login"] for u in get_paginated(url)]

def get_contributors(repo):
    url = f"https://api.github.com/repos/{repo}/contributors?per_page=100"
    return [u["login"] for u in get_paginated(url)]

def get_user_repos(user):
    url = f"https://api.github.com/users/{user}/repos?per_page=100&type=owner"
    repos = get_paginated(url)
    return [r["full_name"] for r in repos if not r["fork"] and not r["archived"]]

def scan_repo(repo_url):
    print(f"🔍 Scanning https://github.com/{repo_url}")
    try:
        subprocess.run(
            [TRUFFLEHOG_CMD, "github", "--repo", f"https://github.com/{repo_url}", "--only-verified"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Failed scan: {repo_url} | {e}")

# 🔥 Main Logic
org_repos = get_org_repos(ORG_NAME)
print(f"📦 {len(org_repos)} repos in org")

org_members = get_org_members(ORG_NAME)
contributors = set()
for repo in org_repos:
    contributors.update(get_contributors(repo))

all_users = set(org_members) | contributors
print(f"👤 Scanning {len(all_users)} org members/contributors")

personal_repos = []
for user in all_users:
    personal_repos += get_user_repos(user)

target_repos = org_repos + personal_repos
print(f"💥 Total targets: {len(target_repos)} repos")

for repo in target_repos:
    scan_repo(repo)
