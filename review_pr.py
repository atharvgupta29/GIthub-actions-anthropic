import os
import json
import requests
from anthropic import Anthropic

# -----------------------------
# Environment variables
# -----------------------------
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]

# -----------------------------
# Read GitHub event payload
# -----------------------------
with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
    event = json.load(f)

pull_request = event["pull_request"]
PR_NUMBER = pull_request["number"]

print(f"Reviewing PR #{PR_NUMBER}")

# -----------------------------
# GitHub API headers
# -----------------------------
github_headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# -----------------------------
# Fetch PR details
# -----------------------------
pr_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/pulls/{PR_NUMBER}"
pr_response = requests.get(pr_url, headers=github_headers)
pr_response.raise_for_status()
pr_data = pr_response.json()

title = pr_data["title"]
body = pr_data.get("body") or ""
diff_url = pr_data["diff_url"]

# -----------------------------
# Fetch PR diff
# -----------------------------
diff_response = requests.get(diff_url, headers=github_headers)
diff_response.raise_for_status()
diff_text = diff_response.text

# -----------------------------
# Initialize Claude client
# -----------------------------
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# -----------------------------
# Build review prompt
# -----------------------------
prompt = f"""
You are a senior software engineer performing a GitHub pull request review.

Repository: {GITHUB_REPOSITORY}
Pull Request Title: {title}

Pull Request Description:
{body}

Below is the full diff of the pull request.

Your task:
- Provide a concise summary
- Identify major issues (correctness, bugs, security)
- Identify minor suggestions (style, clarity, maintainability)
- Ask clarifying questions if intent is unclear

Use clear section headers:
Summary
Major Issues
Minor Suggestions
Questions for the Author

Diff:
{diff_text}
"""

# -----------------------------
# Call Claude
# -----------------------------
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1200,
    temperature=0.2,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

review_text = response.content[0].text

# -----------------------------
# Post review comment to PR
# -----------------------------
comment_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{PR_NUMBER}/comments"

comment_payload = {
    "body": f"## 🤖 AI PR Review (Claude)\n\n{review_text}"
}

comment_response = requests.post(
    comment_url,
    headers=github_headers,
    json=comment_payload,
)
comment_response.raise_for_status()

print("Claude PR review posted successfully.")
