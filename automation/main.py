#!/usr/bin/env python3
"""
GitHub App Creation Automation Tool
"""

import argparse

from github_app_creator import GitHubAppCreator


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

    # # Get Terraform Cloud credentials from environment
    # tfc_token = os.getenv("TFC_TOKEN")
    # tfc_workspace_id = os.getenv("TFC_WORKSPACE_ID")
    # tfc_client = TerraformCloudClient(tfc_token, tfc_workspace_id)

    # if not all([tfc_token, tfc_workspace_id]):
    #     raise ValueError(
    #         "TFC_TOKEN and TFC_WORKSPACE_ID environment variables are required"
    #     )

    creator = GitHubAppCreator(args.enterprise, args.org, args.token)
    app_data = creator.complete_app_creation(args.code)
    if not app_data:
        print("App creation failed. Exiting.")
        return

    print(
        f"GitHub App '{app_data['name']}' created successfully."
        f"\nApplication Slug: {app_data['slug']}"
        f"\nApplication ID: {app_data['id']}"
    )

    # installation_data = creator.install_app(app_data["client_id"])
    # if not installation_data:
    #     print("App installation failed. Exiting.")
    #     return

    # # Upload to Terraform Cloud using a single dictionary
    # upload_data = {
    #     **app_data,
    #     "installation_id": str(installation_data["id"]),
    #     "tfc_client": tfc_client,
    # }
    # creator.upload_to_terraform_cloud(**upload_data)


if __name__ == "__main__":
    main()
