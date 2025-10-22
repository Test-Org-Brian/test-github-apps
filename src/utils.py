def get_app_name(name: str) -> str:
    """Convert app name to uppercase with underscores"""
    if name == "dte-cloud-platform":
        return "CLOUD_PLATFORM"

    if name.startswith("dte-cloud-platform-"):
        return name.replace("dte-cloud-platform-", "").replace("-", "_").replace(" ","_").upper()

    if name.startswith("dte-cloud-application-"):
        return name.replace("dte-cloud-application-", "").replace("-", "_").replace(" ","_").upper()

    return name.replace("-", "_").replace(" ","_").upper()
