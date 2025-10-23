
# Cloud Platform GitHub Apps

Automate the registration, installation, and management of GitHub Apps for cloud platform workflows, with secure integration to Terraform Cloud.

---

## Overview

This project provides a modular solution for:

- Creating GitHub Apps using the Manifest Flow
- Automating app installation and credential retrieval
- Securely storing app secrets in Terraform Cloud workspaces
- Managing app installations and authentication for downstream automation

> [!TIP]
> Use the included GitHub Pages frontend for a user-friendly interface to trigger app creation and monitor status.

## Features

- **Frontend UI**: GitHub Pages dashboard for app creation and status
- **Backend Automation**: Python scripts and GitHub Actions for secure app provisioning
- **Terraform Cloud Integration**: Upload app credentials as sensitive variables
- **Issue-driven Automation**: Uses GitHub Issues to trigger backend workflows and track app registration & installation status
- **Modular Design**: Easily extend or customize for your organization

## Quick Start

1. **Configure your environment**

    - Set required secrets in your repository (e.g., `TFC_TOKEN`, `TFC_WORKSPACE_ID`, `GH_ISSUE_TOKEN`)
    - Update manifests in `docs/manifests.json` as needed

2. **Create a GitHub App**

    - Visit the GitHub Pages dashboard
    - Select or configure an app manifest
    - Follow the guided flow to register the app

3. **Automated Backend**

    - On issue creation, GitHub Actions will:
        - Parse the manifest and code
        - Complete app creation and installation
        - Upload credentials to Terraform Cloud
        - Close the issue when done

4. **Monitor Status**

    - Dashboard tiles reflect app status based on GitHub Issues:
        - ✅ Created (closed issue)
        - ⏳ In Progress (open issue)
        - 🚀 Ready (no issue)

## Project Structure

- `docs/` — Frontend UI (GitHub Pages)
- `automation/` — Python backend scripts
- `.github/workflows/` — GitHub Actions automation
- `manifests/` — App manifests
- `requirements.txt` — Python dependencies
- `package.json` — JS tooling (linting, formatting)

## Development

Clone the repo and install dependencies:

```sh
git clone https://github.com/dteenergy/cloud-platform-github-apps.git
cd cloud-platform-github-apps
python3 -m pip install -r requirements.txt
npm install
```

Run linting and formatting:

```sh
npm run lint
npm run format
```

## Contributing

To contribute to this project, you'll need to install several development tools and configure your environment. Please see our **[Contributing Guide](CONTRIBUTING.md)** for:

- Required software installation (pre-commit, Terraform, terraform-docs, tflint)
- Development environment setup for Windows and macOS
- Pre-commit hook configuration

### 💡 Need Help?

- Check the [Contributing Guide](CONTRIBUTING.md) for detailed instructions
- Review existing issues and pull requests for context
- Contact the development team if you encounter setup difficulties

**Note:** All contributions must pass our automated checks including Terraform validation, linting, and security scans before being merged.
