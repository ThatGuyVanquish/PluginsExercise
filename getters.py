import globals
import requests
import exceptions
from helper_methods import create_json


def get_item(item, args=None):
    """
    Method to send a GET request for an item from the API
    :param item: item to request for
    :param args: additional arguments
    :return: the obtained item in a json format
    """
    # format args as arg=value such that it could be appended to the address as a1=v1&a2=v2&...&an=vn
    if args:
        formatted_args = [f'{key}={str(args[key])}' for key in args]
    else:
        formatted_args = []
    endpoint = globals.base_address + item + '?' + '&'.join([arg for arg in formatted_args])

    response = requests.get(endpoint, headers={'app-id': globals.app_id})
    response_json = response.json()

    retry = 0
    while 'error' in response_json:
        retry += exceptions.handle_error("GET", response_json['error'], endpoint, retry)
        response = requests.get(endpoint, headers={'app-id': globals.app_id})
        response_json = response.json()

    return response_json


def get_items(item, to_return=False, amount=None):
    """
    Method to get multiple items of type item from the API
    :param item: item to request for
    :param to_return: should the method return the result or dump to json, default False means dump to json
    :param amount: number of items to request for, default None means get all
    :return: if to_return=True, return the data collected as a list of json objects
    """
    data = []
    current_page = 0
    filename = item + 's'

    while True:
        args = {'page': current_page}

        # get_item fails with exception, dump collected data and re-raise
        # note that server_error should return here only if already retried server_retry times
        try:
            response = get_item(item, args)
        except exceptions.APIRequestError as e:
            msg = ""
            if len(data) > 0:
                create_json(data, item + 's')
            exceptions.handle_error("GET", e.err, "", exceptions.server_retry)

        # obtained data is empty, meaning there's no more data to collect

        if len(response['data']) == 0:
            break

        # append the obtained information and continue
        data.extend(response['data'])

        # limit the size of obtained data to given amount argument
        if amount:
            if len(data) >= amount:
                data = data[:amount]
                break
        current_page += 1

    # export the obtained data to a JSON file
    if not to_return:
        create_json(data, filename)
    else:
        return data
