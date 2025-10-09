#! /usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""
import requests
import secrets
import json
from pathlib import Path
from typing import Dict, Any

class GitHubAppCreator:
    def __init__(self, org_name: str, github_token: str):
        self.org_name = org_name
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def load_manifest(self, manifest_path: str) -> Dict[str, Any]:
        """Load manifest file (YAML or JSON)"""
        path = Path(manifest_path)
        if not path.exists():
            raise FileNotFoundError(f"Manifest file {manifest_path} does not exist.")

        if path.suffix == ".json":
            with open(manifest_path, "r") as f:
                return json.load(f)
        else:
            raise ValueError("Unsupported manifest file format. Use .json")

    def generate_manifest_url(self, manifest_path: str) -> str:
        """Generate the GitHub URL to create app from manifest"""
        manifest = self.load_manifest(manifest_path)
        state = secrets.token_urlsafe(16)

        # Step 1: User must visit this URL in browser
        url = f"https://github.com/organizations/{self.org_name}/settings/apps/new?state={state}"

        return url


    def complete_app_creation(self, manifest_path: str) -> Dict[str, Any]:
        """Complete app creation using code from GitHub redirect"""
        # Step 2: Use the code from the redirect
        response = requests.post(
            f"{self.base_url}/app-manifests/{code}/conversions",
            headers=self.headers,
            json=manifest,
        )
        response.raise_for_status()

        app_data = response.json()

        return {
            "app_id": app_data["id"],
            "app_name": app_data["name"],
            "private_key": app_data["pem"],
        }

    def upload_to_terraform_cloud(self, app_data: Dict[str, Any], tfc_token: str, workspace_id: str):
        """Upload GitHub App info as variables to Terraform Cloud"""
        from terraform_cloud_client import TerraformCloudClient

        app_name = app_data["app_name"].upper().replace("-", "_").replace(" ", "_")
        tfc_client = TerraformCloudClient(tfc_token, workspace_id)

        variables = {
            f"{app_name}_GITHUB_APP_ID": app_data["app_id"],
            f"{app_name}_GITHUB_APP_INSTALLATION_ID": app_data["client_id"],
            f"{app_name}_GITHUB_APP_PRIVATE_KEY": app_data["private_key"],
        }

        for key, value in variables.items():
            description = f"GitHub App variable {key} for app {app_name}"
            tfc_client.create_variable(key, value, description=description, sensitive=True)
