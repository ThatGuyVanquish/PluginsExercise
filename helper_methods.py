import json


def create_json(data, filename):
    """
    Given data and a filename, create a file and dump the data onto it in a json format

    :param data: given data
    :param filename: requested filename
    """
    # export the obtained data to a JSON file
    data_json = json.dumps(data)

    with open(filename + ".json", "w") as file:
        file.write(data_json)
