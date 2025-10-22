// GitHub Issue Operations for GitHub Pages
// Requires a GitHub App token (do not expose in production)

class GitHubIssueOps {
  contructor ({ owner, repo, token }) {
    this.owner = owner;
    this.repo = repo;
    this.token = token;
    this.baseUrl = `https://api.github.com/repos/${owner}/${repo}/issues`;
    this.headers = {
      Accept: 'application/vnd.github+json',
      Authorization: `Bearer ${token}`,
      'X-GitHub-Api-Version': '2022-11-28',
      'Content-Type': 'application/json'
    };
  }
}

function createIssueBody(code, manifestName) {
  return (
    `### GitHub App Creation Automation\n` +
    `**Code:**\n\n` +
    '```json\n' +
    JSON.stringify({ code, manifest_name: manifestName }, null, 2) +
    '\n```'
  );
}

async function createIssue({ title, body, labels = [] }) {
  const payload = { title, body, labels };
  const response = await fetch(this.baseUrl, {
    method: 'POST',
    headers: this.headers,
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
  }
  return await response.json();
}

async function listIssues({ state = 'open', labels = [] } = {}) {
  const response = await fetch(`${this.baseUrl}?state=${state}&labels=${labels.join(',')}`, {
    method: 'GET',
    headers: this.headers
  });

  if (!response.ok) {
    throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
  }
  return await response.json();
}

// Export for use in other scripts
window.GitHubIssueOps = GitHubIssueOps;
