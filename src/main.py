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

def main():
    parser = argparse.ArgumentParser(description="Create GitHub Apps from manifests")
    parser.add_argument("manifest", help="Path to manifest file")
    parser.add_argument("--org", required=True, help="GitHub organization name")
    parser.add_argument("--token", required=True, help="GitHub token")

    args = parser.parse_args()

    # Get Terraform Cloud credentials from environment
    tfc_token = os.getenv("TFC_TOKEN")
    tfc_workspace_id = os.getenv("TFC_WORKSPACE_ID")

    if not all([tfc_token, tfc_workspace_id]):
        raise ValueError("TFC_TOKEN and TFC_WORKSPACE_ID environment variables are required")

    creator = GitHubAppCreator(args.org, args.token)
    result = creator.create_app_from_manifest(args.manifest)

    print(f"✅ Created app: {result['app_name']} (ID: {result['app_id']})")

    # Upload to Terraform Cloud
    tfc_client = TerraformCloudClient(tfc_token, tfc_workspace_id)
    upload_to_terraform_cloud(result, tfc_client)


if __name__ == "__main__":
    main()
