import os
import requests
import re

USERNAME = "vallabhpadhye"
GITHUB_API_URL = f"https://api.github.com/users/{USERNAME}/repos"

def get_recent_repos(count=3):
    """Fetch recent public repositories from GitHub API"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    
    # Add token if available for higher rate limits
    token = os.environ.get("readmepy")
    if token:
        headers["Authorization"] = f"token {token}"
    
    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": count,
        "type": "owner"
    }
    
    response = requests.get(GITHUB_API_URL, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()

def get_language_emoji(language):
    """Return emoji for programming language"""
    emojis = {
        "Python": "🐍",
        "JavaScript": "📜",
        "TypeScript": "📘",
        "Java": "☕",
        "C++": "⚡",
        "Go": "🐹",
        "Rust": "🦀",
        "Ruby": "💎",
        "PHP": "🐘",
        "Shell": "🐚",
        "HTML": "🌐",
        "CSS": "🎨",
    }
    return emojis.get(language, "📁")

def format_repo_section(repos):
    """Format repositories into markdown"""
    section = ""
    
    for repo in repos:
        name = repo.get("name", "Unknown")
        description = repo.get("description", "No description provided")
        html_url = repo.get("html_url", "")
        language = repo.get("language", "")
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        
        emoji = get_language_emoji(language)
        
        section += f"### {emoji} [{name}]({html_url})\n"
        section += f"{description}\n\n"
        
        if language:
            section += f"**Language:** `{language}` "
        if stars > 0:
            section += f"⭐ {stars} "
        if forks > 0:
            section += f"🍴 {forks}"
        
        section += "\n\n"
    
    return section.strip()

def update_readme():
    """Update README.md with recent repositories"""
    try:
        repos = get_recent_repos(3)
        
        if not repos:
            print("No repositories found")
            return
        
        # Read current README
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
        
        # Generate new section
        new_section = format_repo_section(repos)
        
        # Replace the section between markers
        start_marker = "<!--START_SECTION:repositories-->"
        end_marker = "<!--END_SECTION:repositories-->"
        
        pattern = f"{start_marker}.*?{end_marker}"
        replacement = f"{start_marker}\n{new_section}\n{end_marker}"
        
        updated_content = re.sub(
            pattern,
            replacement,
            readme_content,
            flags=re.DOTALL
        )
        
        # Write updated README
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print("✅ README updated successfully!")
        print(f"Updated with {len(repos)} repositories")
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        raise

if __name__ == "__main__":
    update_readme()
