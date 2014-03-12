import os
import requests
from exception import *


class HSRequest(object):
    """Object to handle HTTP requests

    Although we have greate requests package which can handle the HTTP request
    beautifully, we need this class to fit better our need like sending the
    requests with authentication information, download files, check HTTP
    errors...

    Attributes:
        DEFAULT_ENCODING (str): Default encoding for requests
        USER_AGENT (str): HTTP User agent used when sending requests
        parameters (dict): Some parameters for GET requests
        headers (dict): Custome headers for every requests
        http_status_code (int): HTTP status code returned of requests

    """

    DEFAULT_ENCODING = "UTF-8"
    USER_AGENT = "HelloSign Java SDK"
    parameters = {}
    headers = {'User-Agent': USER_AGENT}
    http_status_code = 0

    def __init__(self, auth):
        self.auth = auth

    def get(self, url, headers={}, parameters={}):
        """Send a GET request with custome headers and parameters

        Args:
            url (str): URL to send the request to
            headers (str, optional): custom headers
            parameters (str, optional): optional parameters

        Returns:
            A JSON object of the returned response

        """

        response = requests.get(
            url, headers=dict(self.headers.items() + headers.items()), params=dict(self.parameters.items() + parameters.items()), auth=self.auth)
        self.http_status_code = response.status_code
        self._check_error(response)
        return response.json()

    def get_file(self, url, filename, headers={}):
        """Get a file from a url and save it as `filename`

        Args:
            url (str): URL to send the request to
            filename (str): File name to save the file as, this can be either
                a full path or a relative path
            headers (str, optional): custom headers

        Returns:
            True if file is downloaded and written successfully, False
            otherwise.

        """

        response = requests.get(url, headers=dict(self.headers.items() + headers.items()), auth=self.auth)
        self.http_status_code = response.status_code
        try:
            self._check_error(response)
            fd = os.open(filename, os.O_CREAT | os.O_RDWR)
            with os.fdopen(fd, "w+b") as f:
                f.write(response.content)
        except:
            return False
        return True

    def post(self, url, data={}, files=None, headers={}):
        """Make POST request to a url

        Args:
            url (str): URL to send the request to
            data (dict, optional): Data to send
            files (dict, optional): Files to send with the request
            headers (str, optional): custom headers

        Returns:
            A JSON object of the returned response

        """

        response = requests.post(
            url, headers=dict(self.headers.items() + headers.items()), data=data, auth=self.auth, files=files)
        self.http_status_code = response.status_code
        self._check_error(response)
        return response.json()

    # TODO: use a expected key in returned json, if the returned key does not match, return false...
    def _check_error(self, response):
        """Check for HTTP error code from the response, raise exception if
        there's any

        Args:
            response (object): Object returned by requests' `get` and `post`
                methods

        Raises:
            HTTPError: If the status code of response is either 4xx or 5xx

        Returns:
            True if status code is not error code
        """

        # If status code is 4xx or 5xx, that should be an error
        if response.status_code >= 400:
            # I intended to return False here but raising a meaningful exception may make senses more.
            raise HTTPError(str(response.status_code) +
                            " error: " + response.json()["error"]["error_msg"])
        # Return True if everything looks OK
        return True
