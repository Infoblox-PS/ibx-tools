"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from typing import Union

import requests
import urllib3
from requests import Response

from ibx_tools.nios.exceptions import WapiInvalidParameterException, WapiRequestException
from ibx_tools.nios.fileop import NiosFileopMixin
from ibx_tools.nios.service import NiosServiceMixin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WAPI(requests.sessions.Session, NiosServiceMixin, NiosFileopMixin):
    """Handles interactions with the Infoblox WAPI.

    This class provides a range of classes to interact with Infoblox WAPI,
    including session management, data retrieval, file operations, and service management.

    Attributes:
        grid_mgr (str): IP address or hostname of the Grid Manager.
        wapi_ver (str): Version of the Infoblox WAPI.
        ssl_verify (bool): Flag to determine SSL certificate verification.
        conn (requests.sessions.Session, optional): Active session to the WAPI grid. Default is
        None.
        grid_ref (str, optional): Reference ID of the connected grid. Default is None.

    Examples:

    Initialize the WAPI instance with a dictionary of properties:

    ```py

    wapi_properties = {
        'grid_mgr': 'gm.example.com',
        'wapi_ver': '2.11',
        'ssl_verify': False
    }
    wapi = WAPI(wapi_properties)

    wapi.connect(username='admin', password='infoblox')

    ```

    Build up the WAPI instance one property at a time:

    ```python

    wapi = WAPI()

    wapi.grid_mgr = 'gm.example.com'
    wapi.wapi_ver = '2.11'
    wapi.ssl_verify = False

    wapi.connect(username='admin', password='infoblox')

    ```
    """

    def __init__(
            self,
            grid_mgr: str = None,
            wapi_ver: str = '2.5',
            ssl_verify: Union[bool, str] = False) -> None:
        super().__init__()
        self.grid_mgr = grid_mgr
        self.wapi_ver = wapi_ver
        self.ssl_verify = ssl_verify
        self.conn = None
        self.grid_ref = None

    def __repr__(self):
        args = []
        for key, value in self.__dict__.items():
            args.append(f'{key}={value}')
        return f"{self.__class__.__qualname__}({', '.join(args)})"

    @property
    def url(self) -> str:
        """
        Constructs a property using `grid_mgr` and `wapi_ver` attributes for the WAPI class.

        Parameters:
        - grid_mgr (str): The IP address or hostname of the grid manager.
        - wapi_ver (str): The version of the WAPI.

        Returns:
        - url (str): The URL constructed using the grid manager and WAPI version.

        Raises:
        - None.

        Example:

        ```python

        wapi = WAPI()
        wapi.grid_mgr = '10.0.0.1'
        wapi.wapi_ver = '2.10'
        url = wapi.url

        print(url)

        ```
        The above code example will return output:

        ```
        'https://10.0.0.1/wapi/v2.10'
        ```

        """
        if self.grid_mgr and self.wapi_ver:
            return f'https://{self.grid_mgr}/wapi/v{self.wapi_ver}'
        return ''

    def connect(self, username: str = None, password: str = None, certificate: str = None) -> None:
        """
        Make a connection to the grid manager using the WAPI instance

        Args:
            username: A string representing the username for the connection. (default: None)
            password: A string representing the password for the connection. (default: None)
            certificate: A string representing the certificate for the connection. (default: None)

        Raises:
            WapiInvalidParameterException: If neither a username and password nor a certificate
            is provided.

        """
        if not self.url:
            logging.error('invalid url %s - unable to connect!', self.url)
            raise WapiInvalidParameterException

        if username and password:
            self.__basic_auth_request(username, password)
        elif certificate:
            self.__certificate_auth_request(certificate)
        else:
            raise WapiInvalidParameterException

    def __certificate_auth_request(self, certificate: str) -> Union[dict, None]:
        """
        This private method performs a certificate authentication request to the API. It uses the
        provided certificate to establish a connection with the API server using the requests
        library.

        Args:
            certificate (str): The certificate to be used for authentication with the API.

        Returns:
            grid _ref (dict): A dictionary

        Raises:
            WapiRequestException: If there is an error with the request to the API.

        """
        with requests.sessions.Session() as conn:
            try:
                res = conn.get(
                    f'{self.url}/grid',
                    cert=certificate,
                    verify=self.ssl_verify
                )
                res.raise_for_status()
            except requests.exceptions.RequestException as err:
                logging.error(err)
                raise WapiRequestException(err) from err
            else:
                grid = res.json()
                setattr(self, 'conn', conn)
                setattr(self, 'grid_ref', grid[0].get('_ref'))
                return grid[0].get('_ref', '')

    def __basic_auth_request(self, username: str, password: str) -> Union[dict, None]:
        """
        This private method makes a request to the specified URL with basic authentication using
        the provided username and password. It stores the session connection in the instance
        attribute 'conn*' and the grid reference in the instance attribute 'grid_ref'.

        Note:
            This method requires the 'requests' library to be installed.

        Args:
            username (str): The username for basic authentication.
            password (str): The password for basic authentication.

        Returns:
            grid _ref (dict): A dictionary

        Raises:
            WapiRequestException: If an error occurs during the request.
        """
        with requests.sessions.Session() as conn:
            try:
                res = conn.get(
                    f'{self.url}/grid',
                    auth=(username, password),
                    verify=self.ssl_verify
                )
                res.raise_for_status()
            except requests.exceptions.RequestException as err:
                logging.error(err)
                raise WapiRequestException(err) from err
            else:
                grid = res.json()
                setattr(self, 'conn', conn)
                setattr(self, 'grid_ref', grid[0].get('_ref'))
                return grid[0].get('_ref', '')

    def object_fields(self, wapi_object: str) -> Union[str, None]:
        """
        Retrieves the object fields for a specified WAPI object.

        Args:
            wapi_object (str): The name of the WAPI object for which to retrieve the fields.

        Returns:
            Union[str, None]: A string containing the fields separated by commas, or None if an
            error occurred.

        Raises:
            WapiRequestException: If there was an error connecting to the WAPI service.

        Example:

        ```py
        wapi = WAPI()
        fields = wapi.object_fields('record:host')
        if fields is not None:
            print(f"Fields: {fields}")
        ```
        """
        try:
            logging.debug('trying %s/%s?_schema', self.url, wapi_object)
            res = self.conn.get(f'{self.url}/{wapi_object}?_schema', verify=self.ssl_verify)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err) from err
        else:
            fields = ",".join(
                field["name"] for field in data.get('fields') if "r" in field.get('supports')
            )
        return fields

    def max_wapi_ver(self) -> None:
        """
        Retrieves the maximum supported version of the WAPI.

        Returns:
            None

        Raises:
            WapiRequestException: If there is an error making the GET request to retrieve the
            WAPI version.

        Example Usage:

        ```py
        session = WAPI()
        session.max_wapi_ver()
        print(session.wapi_ver)  # Prints the maximum supported WAPI version
        ```

        """
        url = f'https://{self.grid_mgr}/wapi/v1.0/?_schema'
        try:
            logging.debug('trying %s', url)
            res = self.conn.get(url, verify=False)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err) from err
        else:
            versions = data.get('supported_versions')
            versions.sort(key=lambda s: list(map(int, s.split('.'))))
            logging.debug(versions)
            max_wapi_ver = versions.pop()
            setattr(self, 'wapi_ver', max_wapi_ver)

    def get(self, wapi_object: str, params=None, **kwargs) -> Response:
        """
        Create a GET request to retrieve WAPI object data

        Args:
            wapi_object: A string representing the path or object to be accessed using the GET
            method.
            params: Optional. A dictionary of query parameters to be included in the request.
            **kwargs: Optional. Additional keyword arguments to be passed to the `request` method.

        Returns:
            A `Response` object representing the HTTP response returned by the server.

        """
        url = f'{self.url}/{wapi_object}'
        return self.conn.request('get', url, params=params, verify=self.ssl_verify, **kwargs)

    def getone(self, wapi_object: str, params=None, **kwargs) -> Response:
        """
        return the reference of a single WAPI object

        Args:
            wapi_object: A string representing the object to retrieve data from.
            params: Optional parameters to include in the request.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            Response: A Response object containing the data returned from the WAPI.

        Raises:
            WapiRequestException: If multiple data records were returned or no data was returned.

        """
        url = f'{self.url}/{wapi_object}'
        response = self.conn.request('get', url, params=params, verify=self.ssl_verify, **kwargs)
        data = response.json()
        if len(data) > 1:
            raise WapiRequestException('Multiple data records were returned')
        elif len(data) == 0:
            raise WapiRequestException('No data was returned')
        return data[0].get('_ref', '')

    def post(self, wapi_object, data=None, json=None, **kwargs) -> Response:
        """
        Create a POST request to create a WAPI object

        Args:
            wapi_object: The object to which the POST request is being made.
            data (optional): The data to be sent in the body of the request. Default is None.
            json (optional): The JSON data to be sent in the body of the request. Default is None.
            **kwargs (optional): Additional keyword arguments to be passed to the request.

        Returns:
            Response: The response object containing the server's response to the POST request.

        """
        url = f'{self.url}/{wapi_object}'
        return self.conn.request('post', url, data=data, json=json, verify=self.ssl_verify,
                                 **kwargs)

    def put(self, wapi_object_ref: str, data=None, **kwargs) -> Response:
        """
        Create a PUT request to update a WAPI object by its _ref

        Args:
            wapi_object_ref: The reference string for the WAPI object.
            data: Optional data to be sent with the request. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            Response: The response object for the PUT request.

        """
        url = f'{self.url}/{wapi_object_ref}'
        return self.conn.request('put', url, verify=self.ssl_verify, **kwargs)

    def delete(self, wapi_object_ref: str, **kwargs) -> Response:
        """
        Deletes a resource specified by the WAPI object reference.

        Args:
            wapi_object_ref (str): The WAPI object reference of the resource to delete.
            **kwargs: Additional arguments to be passed to the HTTP delete request.

        Returns:
            Response: The response object representing the HTTP response.

        """
        url = f'{self.url}/{wapi_object_ref}'
        return self.conn.request('delete', url, verify=self.ssl_verify, **kwargs)
