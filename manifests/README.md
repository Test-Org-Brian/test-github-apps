# GitHub App Manifests

This directory contains GitHub App manifest files that define the configuration for automated GitHub App creation. Each manifest specifies the permissions, events, and settings required for a specific use case.

## Overview

GitHub App manifests allow you to pre-configure GitHub Apps with specific permissions and webhook events. When a manifest is processed, GitHub automatically creates the app with the specified configuration, eliminating manual setup.

## Manifest Structure

Each manifest file follows the [GitHub App Manifest specification](https://docs.github.com/en/apps/sharing-github-apps/registering-a-github-app-from-a-manifest):

```json
{
  "name": "string",                    // Required: Display name of the GitHub App
  "description": "string",             // Optional: Description of the app's purpose
  "url": "string",                     // Required: Homepage URL for the app
  "callback_urls": ["string"],         // Optional: OAuth callback URLs
  "redirect_url": "string",            // Optional: Setup redirect URL
  "webhook_url": "string",             // Optional: Webhook endpoint URL
  "setup_url": "string",               // Optional: Post-installation setup URL
  "setup_on_update": boolean,          // Optional: Redirect to setup_url on updates
  "public": boolean,                   // Optional: Whether app is publicly available
  "request_oauth_on_install": boolean, // Optional: Request OAuth during installation
  "default_permissions": {             // Required: Repository and organization permissions
    "permission_name": "access_level"  // See permissions section below
  },
  "default_events": ["string"],        // Required: Webhook events to subscribe to
  "hook_attributes": {                 // Optional: Webhook configuration
    "url": "string",
    "active": boolean
  }
}
```

## Permission Levels

Each permission in `default_permissions` can have one of these access levels:

- **`read`**: Read-only access
- **`write`**: Read and write access

Please review this article for fine grained [permissions details](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#repository-permissions)

## Common Permissions

### Repository Permissions

- **`contents`**: Repository contents (code, files)
- **`issues`**: Issues and comments
- **`pull_requests`**: Pull requests and reviews
- **`metadata`**: Repository metadata (required for most apps)
- **`checks`**: Check runs and check suites
- **`actions`**: GitHub Actions workflows and runs
- **`deployments`**: Deployment statuses
- **`packages`**: GitHub Packages
- **`pages`**: GitHub Pages
- **`secrets`**: Repository secrets
- **`security_events`**: Security advisories and alerts
- **`statuses`**: Commit statuses
- **`vulnerability_alerts`**: Vulnerability alerts

### Organization Permissions

- **`members`**: Organization members
- **`administration`**: Organization settings
- **`secrets`**: Organization secrets
- **`self_hosted_runners`**: Self-hosted runners
- **`blocking`**: Block users

## Webhook Events

Common webhook events for `default_events`:

### Code Events

- **`push`**: Code pushed to repository
- **`pull_request`**: Pull request opened, closed, etc.
- **`create`**: Branch or tag created
- **`delete`**: Branch or tag deleted

### Issue Events

- **`issues`**: Issues opened, closed, etc.
- **`issue_comment`**: Comments on issues and pull requests

### Check Events

- **`check_run`**: Check runs completed
- **`check_suite`**: Check suites completed
- **`status`**: Commit status updates

### Security Events

- **`security_advisory`**: Security advisories published
- **`code_scanning_alert`**: Code scanning alerts
- **`secret_scanning_alert`**: Secret scanning alerts

## Example Manifest

```json
{
  "name": "CI/CD Automation",
  "description": "Automates continuous integration and deployment workflows",
  "url": "https://github.com/your-org/cicd-app",
  "public": false,
  "request_oauth_on_install": false,
  "setup_on_update": false,
  "default_permissions": {
    "contents": "write",
    "metadata": "read",
    "checks": "write",
    "actions": "write",
    "pull_requests": "write",
    "issues": "write",
    "statuses": "write"
  },
  "default_events": [
    "push",
    "pull_request",
    "check_run",
    "check_suite",
    "workflow_run"
  ],
  "hook_attributes": {
    "url": "https://your-webhook-endpoint.com/github",
    "active": true
  }
}
```

## Permissions Boundaries

For detailed information about permission boundaries and security considerations, see:

- [GitHub Repository Permissions](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#repository-permissions)
- [GitHub App Permissions](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app#permissions)

## Adding New Manifests

1. **Create a new `.json` file** in this directory
2. **Follow the structure** outlined above
3. **Use descriptive naming**: `{purpose}-{environment}.json` (e.g., `cicd-production.json`)
4. **Validate JSON syntax** before committing
5. **Test permissions** with minimal required access first

## Validation

Before committing manifest files:

```bash
# Validate JSON syntax
jq empty your-manifest.json

# Check required fields are present
jq '.name, .url, .default_permissions, .default_events' your-manifest.json
```

## Security Notes

- **Principle of least privilege**: Only request permissions your app actually needs
- **Regular audits**: Review and update permissions as requirements change
- **Environment separation**: Use different manifests for development, staging, and production
- **Webhook security**: Always use HTTPS for webhook URLs and validate webhook signatures

## Automation

These manifests are automatically processed by the GitHub App Creator workflow. When you add or modify a manifest file, the system will:

1. **Update the manifest index** (`docs/manifests.json`)
2. **Make the app available** for creation in the web interface
3. **Validate the manifest structure** during processing

For more information about the automation workflow, see the main project README.
