from main import server_retry


class APIRequestError(Exception):
    """
    Exception raised for errors generated by API calls

    Attributes:
        req -- request which generated the error
        msg -- error string
        err -- error name
    """
    def __init__(self, err, req, message):
        self.req = req
        self.msg = message
        self.err = err
        super().__init__(f"Failed {req} request, {message}")


class AppIDNotExistError(APIRequestError):
    """
    Exception raised for errors generated because app-id is invalid
    Attributes:
        req -- request which generated the error
        err -- error name
    """
    def __init__(self, req):
        self.req = req
        self.err = 'APP_ID_NOT_EXIST'
        super().__init__(self.err, req, "app-id is invalid.")


class AppIDMissingError(APIRequestError):
    """
    Exception raised for errors generated because app-id header is missing
    Attributes:
        req -- request which generated the error
        err -- error name
    """
    def __init__(self, req):
        self.req = req
        self.err = 'APP_ID_MISSING'
        super().__init__(self.err, req, "app-id header is missing in the request.")


class ParamsNotValidError(APIRequestError):
    """
    Exception raised for errors generated because of invalid parameters
    Attributes:
        req -- request which generated the error
        addr -- address which generated the error
        err -- error name
    """
    def __init__(self, req, addr):
        self.req = req
        self.addr = addr
        self.err = 'PARAMS_NOT_VALID'
        super().__init__(self.err, req, f"invalid parameters for address {addr}.")


class ResourceNotFoundError(APIRequestError):
    """
    Exception raised for errors generated because the requested item was not found
    Attributes:
        req -- request which generated the error
        addr -- address which generated the error
        err -- error name
    """
    def __init__(self, req, addr):
        self.req = req
        self.addr = addr
        self.err = 'RESOURCE_NOT_FOUND'
        super().__init__(self.err, req, f"missing resource for address {addr}.")


class PathNotFoundError(APIRequestError):
    """
    Exception raised for errors generated because of invalid path
    Attributes:
        req -- request which generated the error
        path -- request path
        err -- error number
    """
    def __init__(self, req, path):
        self.req = req
        self.path = path
        self.err = 'PATH_NOT_FOUND'
        super().__init__(self.err, req, f"couldn't find the path: {path}, check controller documentation to validate the URL.")


class ServerError(APIRequestError):
    """
    Exception raised for errors generated because of a server error
    Attributes:
        req -- request which generated the error
        err -- error name
    """
    def __init__(self, req):
        self.req = req
        self.err = 'SERVER_ERROR'
        super().__init__(self.err, req, f"Server error for the {req} request, try again later.")


def handle_error(req, err, addr, server_counter):
    """
    Method to handle errors generated by the plugin

    :param req: request which caused the error
    :param err: error name
    :param addr: address which caused the error
    :param server_counter: if the error is a 'SERVER_ERROR', number of times already attempted to call the request
    :return: if the error is a 'SERVER_ERROR' return 1 to add to the counter of the times attempted requesting data
    """
    if err == 'APP_ID_NOT_EXIST':
        raise AppIDNotExistError(req)
    if err == 'APP_ID_MISSING':
        raise AppIDMissingError(req)
    if err == 'PARAMS_NOT_VALID':
        raise ParamsNotValidError(req, addr)
    if err == 'RESOURCE_NOT_FOUND':
        raise ResourceNotFoundError(req, addr)
    if err == 'PATH_NOT_FOUND':
        raise PathNotFoundError(req, addr)
    if err == 'SERVER_ERROR' and server_counter >= server_retry:
        raise ServerError(req)
    return 1
