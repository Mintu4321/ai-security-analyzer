import requests
import os

def post_pr_comment():

    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    if not all([github_token, repo, pr_number]):
        print("❌ Missing environment variables")
        return

    with open("ai-output.txt", "r") as f:
        comment_body = f.read()

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "body": comment_body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ Comment posted successfully")
    else:
        print("❌ Failed to post comment:", response.text)


if __name__ == "__main__":
    post_pr_comment()
