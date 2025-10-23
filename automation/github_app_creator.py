#! /usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""

from typing import Any, Dict

import requests
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
        try:
            response = requests.post(
                f"{self.base_url}/app-manifests/{code}/conversions",
                headers=self.headers,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"App-Manifests Request failed: {e}")
            return {}

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

        try:
            response = requests.post(install_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Installations Request failed: {e}")
            return {}

        installation_data = response.json()
        return installation_data

    def upload_to_terraform_cloud(
        self,
        app_name: str,
        app_id: str,
        slug: str,
        installation_id: str,
        client_id: str,
        client_secret: str,
        webhook_secret: str,
        pem: str,
        tfc_client: Any,
    ):
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

        failed_uploads = []
        successful_uploads = []

        for key, value in vals_to_upload.items():
            description = f"GitHub App variable {key} for app {app_name}, provisioned through automation in cloud-platform-github-apps"
            try:
                result = tfc_client.create_variable(
                    key, value, description=description, sensitive=True
                )
                if result:
                    successful_uploads.append(key)
                    print(f"✅ Successfully uploaded variable: {key}")
                else:
                    failed_uploads.append(key)
                    print(f"❌ Failed to upload variable: {key}")
            except Exception as e:
                failed_uploads.append(key)
                print(f"❌ Error uploading variable {key}: {e}")

        # Summary
        if successful_uploads:
            print(
                f"\n✅ Successfully uploaded {len(successful_uploads)} variables: {', '.join(successful_uploads)}"
            )

        if failed_uploads:
            print(
                f"\n❌ Failed to upload {len(failed_uploads)} variables: {', '.join(failed_uploads)}"
            )
            print(
                "⚠️  Some variables failed to upload. Please check the logs above for details."
            )
        else:
            print(
                f"\n🎉 All {len(successful_uploads)} variables uploaded successfully!"
            )

        return {"successful": successful_uploads, "failed": failed_uploads}
