"""
Utility functions for GitHub App automation.
"""


def get_app_name(name: str) -> str:
    """
    Convert app name to uppercase with underscores for use as Terraform variable prefix.

    This function standardizes GitHub App names to create consistent Terraform variable
    naming conventions by converting names to uppercase and replacing hyphens/spaces
    with underscores.

    Args:
        name (str): The GitHub App name to convert

    Returns:
        str: Standardized uppercase name with underscores

    Examples:
        >>> get_app_name("dte-cloud-platform")
        'CLOUD_PLATFORM'
        >>> get_app_name("dte-cloud-platform-actions")
        'ACTIONS'
        >>> get_app_name("dte-cloud-application-sos")
        'SOS'
        >>> get_app_name("my-custom-app")
        'MY_CUSTOM_APP'
    """
    if name == "dte-cloud-platform":
        return "CLOUD_PLATFORM"

    if name.startswith("dte-cloud-platform-"):
        return (
            name.replace("dte-cloud-platform-", "")
            .replace("-", "_")
            .replace(" ", "_")
            .upper()
        )

    if name.startswith("dte-cloud-application-"):
        return (
            name.replace("dte-cloud-application-", "")
            .replace("-", "_")
            .replace(" ", "_")
            .upper()
        )

    # Default case: convert any name to uppercase with underscores
    return name.replace("-", "_").replace(" ", "_").upper()
