import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
url = input("Enter the github url : ")
def extract_username(url: str) -> str:
    git_url = url.strip()
    git_url = git_url.replace("https://", "")
    git_url = git_url.replace("www.", "")
    if git_url.endswith("/"):
        git_url = git_url[:-1]
    parts = git_url.split("/")
    if len(parts) > 2 or parts[0] != "github.com":
        raise ValueError("Invalid git")
    return parts[1]
username = extract_username(url)
token = os.getenv("token_git")
headers = {}
if token:
    headers["Authorization"] = f"token {token}"
headers["Accept"] = "application/vnd.github.mercy-preview+json"
def responses(user: str):
    url = f"https://api.github.com/users/{user}/repos?per_page=50"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub API failed: {response.status_code}")
    return response.json()
r1 = responses(username)
all_repo = []
for repo in r1:
    repo_score = 0
    info = {}
    name = repo.get("name", "")
    info["Name"] = name
    des = repo.get("description", "")
    info["Description"] = des
    if des:
        repo_score += 1
    updated_at = repo.get("updated_at", "")
    info["Date"] = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    topics = repo.get("topics", [])
    info["topic"] = topics
    if topics:
        repo_score += 1
    languages_url = repo.get("languages_url", "")
    lan = requests.get(languages_url, headers=headers)
    if lan.status_code != 200:
        continue
    res = lan.json()
    language = list(res.keys())
    info["languages"] = language
    if language:
        max_used = max(res, key=res.get)
        info["main_language"] = max_used
    readme_url = f"https://api.github.com/repos/{username}/{name}/readme"
    readme = requests.get(readme_url, headers=headers)
    if readme.status_code == 200:
        repo_score += 2
    homepage = repo.get("homepage", "")
    info["Deploy"] = homepage
    if homepage:
        repo_score += 2
    stars = repo.get("stargazers_count", 0)
    info["star"] = stars
    if stars >= 5:
        repo_score += 1
    size = repo.get("size", 0)
    if size > 50:
        repo_score += 1
    if size > 200:
        repo_score += 1
    info["score"] = repo_score
    all_repo.append(info)
sorted_repos = sorted(all_repo, key=lambda x: x["Date"], reverse=True)
top_five = sorted_repos[:5]
def calculate_activity_score(top_five):
    rules = [
        (30, 5),
        (60, 4),
        (90, 3),
        (120, 2),
        (180, 1)
    ]
    score = 0
    today = datetime.today()
    for repo in top_five:
        diff = (today - repo["Date"]).days
        for limit, points in rules:
            if diff <= limit:
                score += points
                break
    return score
indi_score = calculate_activity_score(top_five)
if 18 <= indi_score <= 25:
    activity_score = 5
elif 10 <= indi_score <= 17:
    activity_score = 3
elif 5 <= indi_score <= 9:
    activity_score = 1
else:
    activity_score = 0
total_score = sum(repo["score"] for repo in all_repo)
print(total_score)
top_quality = sorted(all_repo, key=lambda x: x["score"], reverse=True)[:5]
avg_score = sum(r["score"] for r in top_quality) / len(top_quality)
quality_score = min(avg_score, 15)
final_score = round(quality_score + activity_score, 2)
print("Final Score:", final_score, "/20")
