import json
from time import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        result["response_time"] = end - start
        return result

    return wrapper


class NetworkRequest:
    @staticmethod
    @measure_time
    def request(method, url, data=None, headers={}):
        req = Request(url=url, method=method)
        for key, value in headers.items():
            req.add_header(key, value)

        if data is not None:
            req.data = json.dumps(data).encode("utf-8")

        result = {}
        try:
            with urlopen(req) as res:
                body = res.read().decode("utf-8")
                result["body"] = json.loads(body)
                result["code"] = res.status
        except HTTPError as e:
            result["body"] = json.loads(e.read().decode("utf-8"))
            result["code"] = e.code

        return result

    @staticmethod
    @measure_time
    def get(url, headers={}):
        return NetworkRequest.request("GET", url, headers=headers)

    @staticmethod
    @measure_time
    def post(url, data, headers={}):
        return NetworkRequest.request("POST", url, data=data, headers=headers)

    @staticmethod
    @measure_time
    def put(url, data, headers={}):
        return NetworkRequest.request("PUT", url, data=data, headers=headers)

    @staticmethod
    @measure_time
    def delete(url, headers={}):
        return NetworkRequest.request("DELETE", url, headers=headers)


RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def colored_output(color):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(color, end="")
            func(*args, **kwargs)
            print(RESET, end="")

        return wrapper

    return decorator


@colored_output(CYAN)
def print_info(message):
    print(message)


@colored_output(YELLOW)
def print_warning(message):
    print(message)


@colored_output(GREEN)
def print_success(message):
    print(message)


@colored_output(RED)
def print_error(message):
    print(message)


@colored_output(MAGENTA)
def print_highlight(message):
    print(message)


@colored_output(BLUE)
def print_data(message):
    print(message)
