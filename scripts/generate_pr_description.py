import os
import subprocess
from litellm import completion

MODEL = os.environ.get("MODEL", "openrouter/openai/gpt-4o")

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

base = os.environ["BASE_BRANCH"]
head = os.environ["HEAD_BRANCH"]

# Fetch branches
run(f"git fetch origin {base} {head}")

commits = run(f"git log origin/{base}..origin/{head} --pretty=format:'- %s'")
diff = run(f"git diff origin/{base}...origin/{head} --unified=0 --no-color --minimal")

prompt = f"""
You are a senior developer assistant. Write a clear, concise pull request description based on the following commit messages and code changes.

Commit messages:
{commits}

Code diff:
{diff}

Keep it short but informative, suitable for reviewers.
"""

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)

summary = response["choices"][0]["message"]["content"]

# Save for PR comment
with open("pr_description.txt", "w") as f:
    f.write(summary)
