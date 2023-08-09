import requests
import exceptions
from getters import get_items
from helper_methods import create_json
import globals
from setters import set_api, set_creds

invalid_token = "all_your_base_are_belong_to_us"
server_retry = 5


def connectivity_test(endpoint):
    """
    Method to test connectivity to some API
    :param endpoint: endpoint for the specific API
    """
    address = globals.base_address + endpoint
    response = requests.get(address, headers={'app-id': globals.app_id})
    response_json = response.json()

    """
        handle_error handles SERVER_ERROR up to server_retry times
        therefore if handle_error returns to retry, the method will retry connecting
        up to the server_retry limit
    """

    retry = 0
    while 'error' in response_json:
        retry += exceptions.handle_error("GET", response_json['error'], address, retry)
        response = requests.get(address, headers={'app-id': globals.app_id})
        response_json = response.json()
    else:
        print("Connected successfully!")


def get_users():
    """
    Create a json file called users.json which holds the entire user database of dummyapi.io
    """
    get_items('user')


def get_posts():
    """
    Create a json file called posts.json which holds some amount of posts and their relevant comments from
    dummyapi.io
    """
    posts = get_items('post', to_return=True, amount=50)
    for post in posts:
        post_id = post['id']
        endpoint = f'post/{post_id}/comment'
        comments = get_items(endpoint, to_return=True)
        post['comments'] = comments

    create_json(posts, 'posts')


def main():
    set_api("https://dummyapi.io/data/v1/")
    # set_creds('INSERT CREDENTIALS HERE')
    connectivity_test('user?limit=1')
    get_users()
    get_posts()


if __name__ == '__main__':
    main()
