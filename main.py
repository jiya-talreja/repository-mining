import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
url=input("Enter the github url : ")
def extract_username(url:str)->str:
    git_url=url.strip()
    git_url=git_url.replace("https://","")
    git_url=git_url.replace("www.","")
    if git_url.endswith("/"):
        git_url=git_url[:-1]
    print(git_url)
    parts=git_url.split("/")
    if len(parts)>2 or parts[0]!="github.com":
        raise ValueError("Invalid git")
    username=parts[1]
    return username
username=extract_username(url)    
token=os.getenv("token_git")
def responses(user:str,token:str):
    headers={}
    if token:
        headers["Authorization"]=f"token {token}"
    url = f"https://api.github.com/users/{user}/repos?per_page=50"   
    headers["Accept"]= "application/vnd.github.mercy-preview+json" 
    response=requests.get(url,headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub API failed: {response.status_code} -> {response.text}")
    return response.json()    
r1=responses(username,token)
print("Github repos info : ")
for repo in r1:
    info={}
    name = repo.get("name", "")
    info["Name"]=name
    des= repo.get("description", "")
    info["Description"]=des
    updated_at = repo.get("updated_at", "")
    dates=datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ")
    info["Date"]=dates
    topics = repo.get("topics", [])
    info["topic"]=topics
    languages_url = repo.get("languages_url", "")
    repo_url = repo.get("html_url", "")  
    lan=requests.get(languages_url)
    if lan.status_code!=200:
        raise ValueError("NOt found")
    res=lan.json()
    language=[]
    max_lan={}
    language.extend(list(res))
    max_lan["languages"]=language
    if language==[]:
        max_used=""
    else:
        max_used=max(res,key=res.get)
        max_lan["main_language"]=max_used
    print(repo_url)
    print(info)
    print(max_lan)  
    print("_________________________________________")  
#to check active users


    
