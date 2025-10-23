#!/usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""

import argparse
import os

from github_app_creator import GitHubAppCreator
from terraform_cloud_client import TerraformCloudClient


def validate_args(args):
    """Validate required arguments"""
    errors = []

    if not args.enterprise or not args.enterprise.strip():
        errors.append("--enterprise is required and cannot be empty")

    if not args.org or not args.org.strip():
        errors.append("--org is required and cannot be empty")

    if not args.token or not args.token.strip():
        errors.append("--token is required and cannot be empty")

    if not args.code or not args.code.strip():
        errors.append("--code is required and cannot be empty")

    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Complete Github App creation and upload to Terraform Cloud"
    )
    parser.add_argument("--enterprise", required=True, help="GitHub Enterprise name")
    parser.add_argument("--org", required=True, help="GitHub Organization name")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument(
        "--code", required=True, help="GitHub App manifest code from redirect"
    )

    args = parser.parse_args()

    # Validate arguments
    if not validate_args(args):
        return 1

    # Get Terraform Cloud credentials from environment
    tfc_token = os.getenv("TFC_TOKEN")
    tfc_workspace_id = os.getenv("TFC_WORKSPACE_ID")

    if not all([tfc_token, tfc_workspace_id]):
        print(
            "❌ Error: TFC_TOKEN and TFC_WORKSPACE_ID environment variables are required"
        )
        return 1

    try:
        tfc_client = TerraformCloudClient(tfc_token, tfc_workspace_id)
    except Exception as e:
        print(f"❌ Error: Failed to initialize Terraform Cloud client: {e}")
        return 1

    creator = GitHubAppCreator(args.enterprise, args.org, args.token)
    app_data = creator.complete_app_creation(args.code)
    if not app_data:
        print("❌ App creation failed. Exiting.")
        return 1

    # Log app creation success
    # TODO: remove once complete flow is working
    print(
        f"✅ GitHub App '{app_data['name']}' created successfully."
        f"\n📋 Application Slug: {app_data['slug']}"
        f"\n🆔 Application ID: {app_data['id']}"
    )

    installation_data = creator.install_app(app_data["client_id"])
    if not installation_data:
        print("❌ App installation failed. Exiting.")
        return 1

    # Upload to Terraform Cloud
    upload_data = {
        **app_data,
        "installation_id": str(installation_data["id"]),
        "tfc_client": tfc_client,
    }
    upload_result = creator.upload_to_terraform_cloud(**upload_data)

    # Check upload results
    if upload_result and upload_result.get("failed"):
        print(f"⚠️  Warning: Some variables failed to upload: {upload_result['failed']}")
        return 1
    elif upload_result and upload_result.get("successful"):
        print("🎉 All GitHub App variables uploaded successfully!")
        return 0
    else:
        print("❌ Upload to Terraform Cloud failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
