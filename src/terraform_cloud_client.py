#!/usr/bin/env python3
"""
A simple Terraform Cloud API client to create variables in a workspace.
"""
import requests

class TerraformCloudClient:
    def __init__(self, token: str, workspace_id: str):
        self.token = token
        self.workspace_id = workspace_id
        self.base_url = "https://app.terraform.io/api/v2"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json"
        }

    def get_workspace_vars(self):
        """Fetch workspace variables"""
        try:
            response = requests.get(
                f"{self.base_url}/workspaces/{self.workspace_id}/vars",
                headers=self.headers
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return {}

        return response.json()

    def create_variable(self, key: str, value: str, description: str = "", sensitive: bool = True):
        """Create a Terraform variable in the workspace if it doesn't exist"""
        current_vars = self.get_workspace_vars()
        for var in current_vars.get("data", []):
            if var["attributes"]["key"] == key:
                print(f"⚠️ Variable {key} already exists. Skipping creation.")
                return var

        data = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": key,
                    "value": value,
                    "description": description,
                    "category": "terraform",
                    "hcl": False,
                    "sensitive": sensitive
                }
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/workspaces/{self.workspace_id}/vars",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to create variable {key}: {e}")
            return {}

        if response.status_code == 201:
            print(f"✅ Created variable: {key}")
            return response.json()
        else:
            print(f"❌ Failed to create variable {key}: {response.status_code} - {response.text}")
            return {}
