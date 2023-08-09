import globals


def set_api(api):
    """
    Method to set the global base_address value to a specific API's address
    :param api: address of an API
    """
    globals.base_address = api


def set_creds(creds):
    """
    Method to set the global app_id value to a specific API token
    :param creds: token to set the global api_token holder as
    """
    globals.app_id = creds

