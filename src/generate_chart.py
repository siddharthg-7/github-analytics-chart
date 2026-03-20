import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import os

USERNAME = "siddharthg-7"

# Create charts folder if not exists
os.makedirs("charts", exist_ok=True)

# GitHub API (fetch multiple pages to get more history)
events = []
for page in range(1, 4):  # Fetch up to 3 pages (300 events)
    url = f"https://api.github.com/users/{USERNAME}/events?per_page=100&page={page}"
    response = requests.get(url)
    if response.status_code != 200:
        break
    page_events = response.json()
    if not page_events:
        break
    events.extend(page_events)

if not events:
    print("Failed to fetch any events from GitHub API")
    exit(0)

monthly_commits = defaultdict(int)

# Process events
for event in events:
    if event["type"] == "PushEvent":
        payload = event.get("payload", {})
        
        # Get commit count: use distinct_size, size, or length of commits list
        commit_count = payload.get("distinct_size", payload.get("size", 0))
        if commit_count == 0 and "commits" in payload:
            commit_count = len(payload["commits"])
            
        if commit_count > 0:
            dt = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            month = dt.strftime("%b %Y")
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
