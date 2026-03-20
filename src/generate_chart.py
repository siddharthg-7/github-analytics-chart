import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import os

USERNAME = "siddharthg-7"

# Create charts folder if not exists
os.makedirs("charts", exist_ok=True)

# GitHub API (recent events)
url = f"https://api.github.com/users/{USERNAME}/events"
response = requests.get(url)

if response.status_code != 200:
    raise Exception("Failed to fetch data from GitHub API")

events = response.json()

monthly_commits = defaultdict(int)

# Process events
for event in events:
    if event["type"] == "PushEvent":
        payload = event.get("payload", {})
        if "commits" in payload:
            dt = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            month = dt.strftime("%b %Y")
            commit_count = len(payload["commits"])
            monthly_commits[month] += commit_count

if not monthly_commits:
    print("No commits found in recent events.")
    # Create a dummy entry to avoid empty plot errors if needed, 
    # or just exit gracefully.
    exit(0)

# Sort months chronologically
months = sorted(monthly_commits.keys(), key=lambda x: datetime.strptime(x, "%b %Y"))
commits = [monthly_commits[m] for m in months]

# 🔥 DARK THEME (Tokyonight Inspired)
plt.style.use("dark_background")

plt.figure(figsize=(12, 6))

bars = plt.bar(months, commits)

# Customize colors
for bar in bars:
    bar.set_color("#7aa2f7")  # soft blue

# Labels & Title
plt.xlabel("Month", fontsize=12)
plt.ylabel("Commits", fontsize=12)
plt.title(f"Monthly GitHub Commits - {USERNAME}", fontsize=14, weight='bold')

# Rotate labels
plt.xticks(rotation=45)

# Add value labels on bars
for i, v in enumerate(commits):
    plt.text(i, v + 0.5, str(v), ha='center', fontsize=9)

plt.tight_layout()

# Save chart
plt.savefig("charts/monthly_commits.png", dpi=200)
plt.close()
