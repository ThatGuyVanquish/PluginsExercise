import requests
import json

app_id = None
invalid_token = "allyourbasearebelongtous"
base_address = "https://dummyapi.io/"
base_endpoint = "/data/v1/"


class GetRequestError(Exception):
    """
    Exception raised for errors obtained by get request

    Attributes:
        err -- error string obtained by the GET method
    """
    def __init__(self, err):
        self.err = err
        super().__init__(f"Failed GET request because of {err}")


def create_json(data, filename):
    # export the obtained data to a JSON file
    data_json = json.dumps(data)

    with open(filename + ".json", "w") as file:
        file.write(data_json)

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

    # Should raise an exception
    if 'error' in response_json:
        raise GetRequestError(response_json['error'])

    return response_json


def get_items(item):
    data = []
    current_page = 0
    filename = item + 's'

    while True:
        args = {'page': current_page}

        # get_item fails with exception, dump collected data and re-raise
        try:
            response = get_item(item, args)
        except GetRequestError as e:
            msg = ""
            if len(data) > 0:
                create_json(data, item + 's')
                msg = f"Dumped collected data onto {filename}.json\n"
            raise GetRequestError(f"{msg}{e}")

        # obtained data is empty, meaning there's no more data to collect

        if len(response['data']) == 0:
            break

        # append the obtained information and continue
        data.extend(response['data'])
        current_page += 1

    # export the obtained data to a JSON file
    create_json(data, filename)


def get_users():
    get_items('user')


def main():

    connectivity_test()
    get_users()


if __name__ == '__main__':
    main()
