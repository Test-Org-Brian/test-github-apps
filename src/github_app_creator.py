#! /usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""
import requests
import secrets
import json
from pathlib import Path
from typing import Dict, Any
from utils import get_app_name

class GitHubAppCreator:
    def __init__(self, enterprise: str, org_name: str, github_token: str):
        self.enterprise = enterprise
        self.org = org_name
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def complete_app_creation(self, code: str) -> Dict[str, Any]:
        """Complete app creation using code from GitHub redirect"""
        # Step 2: Use the code from the redirect
        response = requests.post(
            f"{self.base_url}/app-manifests/{code}/conversions",
            headers=self.headers,
        )
        response.raise_for_status()

        app_data = response.json()

        return {
            "id": app_data["id"],
            "slug": app_data["slug"],
            "name": app_data["name"],
            "client_id": app_data["client_id"],
            "client_secret": app_data["client_secret"],
            "webhook_secret": app_data["webhook_secret"],
            "pem": app_data["pem"],
            "html_url": app_data["html_url"],
        }

    def install_app(self, client_id: str) -> Dict[str, Any]:
        """Install the GitHub App to the organization using client_id"""
        install_url = f"{self.base_url}/enterprises/{self.enterprise}/apps/organizations/{self.org}/installations"
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.github_token}"

        payload = {
            "client_id": client_id,
            "repository_selection": "none",
        }

        response = requests.post(
            install_url,
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        installation_data = response.json()
        return installation_data

    def upload_to_terraform_cloud(self, app_name: str, app_id: str, slug: str, installation_id: str, client_id: str, client_secret: str, webhook_secret: str, pem: str, tfc_client: Any):
        """Upload GitHub App info as variables to Terraform Cloud in the new style"""
        app_name = get_app_name(app_name)

        vals_to_upload = {
            f"{app_name}_APP_ID": app_id,
            f"{app_name}_SLUG": slug,
            f"{app_name}_CLIENT_ID": client_id,
            f"{app_name}_CLIENT_SECRET": client_secret,
            f"{app_name}_WEBHOOK_SECRET": webhook_secret,
            f"{app_name}_INSTALLATION_ID": installation_id,
            f"{app_name}_PEM": pem,
        }

        for key, value in vals_to_upload.items():
            description = f"GitHub App variable {key} for app {app_name}, provisioned through automation in cloud-platform-github-apps"
            tfc_client.create_variable(key, value, description=description, sensitive=True)
