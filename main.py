import requests
import json

app_id = None
invalid_token = "allyourbasearebelongtous"
base_address = "https://dummyapi.io/"
base_endpoint = "/data/v1/"


def set_creds(creds):
    global app_id
    app_id = creds


def connectivity_test():
    global app_id
    if not app_id:
        set_creds(invalid_token)
    endpoint = base_address + base_endpoint + 'user?limit=1'
    response = requests.get(endpoint, headers={'app-id': app_id})
    response_json = response.json()
    if 'error' in response_json:
        raise ConnectionError(f"Failed connection with error {response_json['error']}")
    else:
        print("Connected successfully!")

def get_item(item):


def main():

    connectivity_test()


if __name__ == '__main__':
    main()
