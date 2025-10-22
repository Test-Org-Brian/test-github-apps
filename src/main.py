#!/usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""
import argparse
import os
from pathlib import Path
from typing import Any, Dict
from github_app_creator import GitHubAppCreator
from terraform_cloud_client import TerraformCloudClient
from utils import get_app_name

def main():
    parser = argparse.ArgumentParser(description="Create GitHub Apps from manifests")
    parser.add_argument("manifest", help="Path to manifest file")
    parser.add_argument("--enterprise", required=True, help="GitHub Enterprise name")
    parser.add_argument("--org", required=True, help="GitHub Organization name")
    parser.add_argument("--token", required=True, help="GitHub token")

    args = parser.parse_args()

    # Get Terraform Cloud credentials from environment
    tfc_token = os.getenv("TFC_TOKEN")
    tfc_workspace_id = os.getenv("TFC_WORKSPACE_ID")
    tfc_client = TerraformCloudClient(tfc_token, tfc_workspace_id)

    if not all([tfc_token, tfc_workspace_id]):
        raise ValueError("TFC_TOKEN and TFC_WORKSPACE_ID environment variables are required")

    creator = GitHubAppCreator(args.enterprise, args.org, args.token)
    app_data = creator.complete_app_creation(args.manifest)
    installation_data = creator.install_app(app_data["client_id"])

    # Upload to Terraform Cloud
    creator.upload_to_terraform_cloud(
        app_id=str(app_data["id"]),
        slug=app_data["slug"],
        app_name=app_data["name"],
        client_id=app_data["client_id"],
        client_secret=app_data["client_secret"],
        webhook_secret=app_data["webhook_secret"],
        pem=app_data["pem"],
        installation_id=str(installation_data["id"]),
        tfc_client=tfc_client
    )


if __name__ == "__main__":
    main()
