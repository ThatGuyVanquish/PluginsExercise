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


def get_item(item, args=None):
    if args:
        formatted_args = [f'{key}={str(args[key])}' for key in args]
    else:
        formatted_args = []
    endpoint = base_address + base_endpoint + item + '?' + '&'.join([arg for arg in formatted_args])
    response = requests.get(endpoint, headers={'app-id': app_id})
    response_json = response.json()
    if 'error' in response_json:
        return None
    return response_json


def get_items(item):
    data = []
    current_page = 0
    while True:
        args = {'page' : current_page}
        response = get_item(item, args)

        # get_item failed to return value, there's an error communicating with the API
        if not response:
            return data

        # obtained data is empty, meaning there's no more data to collect

        if len(response['data']) == 0:
            break

        # append the obtained information and continue
        data.extend(response['data'])
        current_page += 1

    # export the obtained data to a JSON file
    file_name = item + 's'
    data_json = json.dumps(data)

    with open(file_name + ".json", "w") as file:
        file.write(data_json)


def get_users():
    get_items('user')


def main():

    connectivity_test()
    get_users()


if __name__ == '__main__':
    main()
