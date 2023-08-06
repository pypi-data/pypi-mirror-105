"""DB-API implementation backed by HiveServer2 (Thrift API)
See http://www.python.org/dev/peps/pep-0249/
Many docstrings in this file are based on the PEP, which is in the public domain.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from urllib.parse import urlparse

import datetime
import json
import re
from decimal import Decimal
from ssl import CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED
import http.client as httplib
from urllib.parse import *

from uniphi import common
from uniphi.common import DBAPITypeObject
# Make all exceptions visible in this uniphi per DB-API
import logging
import sys
import uniphi.typeId
import uniphi.constants
from uniphi.aesCipher import AESCipher

apilevel = '2.0'
threadsafety = 2  # Threads may share the uniphi and connections.
paramstyle = 'pyformat'  # Python extended format codes, e.g. ...WHERE name=%(name)s
key = b"teamuniphi@cunninghamroadfrmbang"

_logger = logging.getLogger(__name__)

_TIMESTAMP_PATTERN = re.compile(r'(\d+-\d+-\d+ \d+:\d+:\d+(\.\d{,6})?)')

ssl_cert_parameter_map = {
    "none": CERT_NONE,
    "optional": CERT_OPTIONAL,
    "required": CERT_REQUIRED,
}


def _parse_timestamp(value):
    if value:
        match = _TIMESTAMP_PATTERN.match(value)
        if match:
            if match.group(2):
                format = '%Y-%m-%d %H:%M:%S.%f'
                # use the pattern to truncate the value
                value = match.group()
            else:
                format = '%Y-%m-%d %H:%M:%S'
            value = datetime.datetime.strptime(value, format)
        else:
            raise Exception(
                'Cannot convert "{}" into a datetime'.format(value))
    else:
        value = None
    return value


TYPES_CONVERTER = {"DECIMAL_TYPE": Decimal,
                   "TIMESTAMP_TYPE": _parse_timestamp}


class HiveParamEscaper(common.ParamEscaper):
    def escape_string(self, item):
        # backslashes and single quotes need to be escaped
        # TODO verify against parser
        # Need to decode UTF-8 because of old sqlalchemy.
        # Newer SQLAlchemy checks dialect.supports_unicode_binds before encoding Unicode strings
        # as byte strings. The old version always encodes Unicode as byte strings, which breaks
        # string formatting here.
        if isinstance(item, bytes):
            item = item.decode('utf-8')
        return "'{}'".format(
            item
                .replace('\\', '\\\\')
                .replace("'", "\\'")
                .replace('\r', '\\r')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
        )


_escaper = HiveParamEscaper()


def connect(*args, **kwargs):
    """Constructor for creating a connection to the database. See class :py:class:`Connection` for
    arguments.
    :returns: a :py:class:`Connection` object.
    """
    return Connection(*args, **kwargs)


class Connection(object):
    """Wraps a http uniphi session"""

    def __init__(
            self,
            connectStr=None
    ):
        print("got connect info {str}, with datatype {dt}".format(str=str, dt=type(str)))
        scheme = connectStr.drivername
        print("Using scheme {scheme}".format(scheme=scheme))
        uri = "{host}:{port}".format(host= connectStr.host, port=connectStr.port)
        print("Using uri {uri}".format(uri=uri))
        self._username = connectStr.username
        print("Using username {user}".format(user=self._username))
        password = connectStr.password
        print("Using password {password}".format(password=password))
        _auth_token = None

        if scheme in ("https", "http", "uniphi"):
            if scheme == "https" or scheme == "uniphi":
                if password is None:
                    raise ValueError("Password should be set")
                if self._username is None:
                    raise ValueError("Username should be set")
                # ssl_context = create_default_context()
                # ssl_context.check_hostname = "false"
                # ssl_cert = "none"
                # ssl_context.verify_mode = ssl_cert_parameter_map.get(ssl_cert, CERT_NONE)
                self.http_transport = httplib.HTTPConnection(uri, timeout=10)
                # Create a call to get a token here by first validating credentials
                self.signin(password)
                response = self.http_transport.getresponse()
                if response.status == 409:
                    _logger.info("**** got 409 from signin")
                    response.read()
                    self.signoutAndSignin(password)
                    response = self.http_transport.getresponse()
                    if response.status != 200:
                        _logger.info("**** signed in successfully")
                        raise Exception("Unable to sign back into uniphi")
                elif response.status == 200:
                    _logger.info("**** signed in successfully")
                    pass
                else:
                    _logger.info("**** Unknown issue while signing in : {error}".format(error=response))
                    raise Exception("Unknown issue while logging in")
                resp = response.read()
                _logger.info("Reponding to connect request with {response}".format(response=resp))
                responseDict = json.loads(resp)
                self._auth_token = responseDict['authtoken']
            else:
                raise ValueError(
                    "Use scheme HTTPS/UNIPHI"
                )
        # This is the part where other drivers point to a database. It is not necessary for Uniphi.

    def signoutAndSignin(self, password):
        body = {
            "username": self._username
        }
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*"}
        # self._set_headers(http_transport, None)
        jsonbody = json.dumps(body)
        print("using json {jsonbody}".format(jsonbody=jsonbody))
        self.http_transport.request("POST", "/signout", json.dumps(body), headers)
        response = self.http_transport.getresponse()
        if response.status == 200:
            _logger.info("**** signedout successfully")
            response.read()
            self.signin(password)
        else:
            raise Exception("User unable to logout")

    def signin(self, password):
        encodedtext = AESCipher().encrypt(password).hex()
        print(encodedtext)
        body = {
            "username": self._username,
            "password": encodedtext
        }
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*"}
        # self._set_headers(http_transport, None)
        jsonbody = json.dumps(body)
        print("Signin : using json {jsonbody}".format(jsonbody=jsonbody))
        self.http_transport.request("POST", "/signin", json.dumps(body), headers)

    @staticmethod
    def _set_headers(http_transport, auth_token):
        http_transport.putheader('Connection', 'keep-alive')
        http_transport.putheader('Accept-Encoding', 'gzip, deflate, br')
        http_transport.putheader('Accept', '*/*')
        if auth_token is not None:
            http_transport.putheader('Authorization', 'Bearer {token}'.format(token=auth_token))

    def __enter__(self):
        """Transport should already be opened by __init__"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Call close"""
        self.close()

    def close(self):
        """Uniphi doesn't need to close client connections """
        pass

    def commit(self):
        """Hive does not support transactions, so this does nothing."""
        pass

    def cursor(self, *args, **kwargs):
        """Return a new :py:class:`Cursor` object using the connection."""
        return Cursor(self, *args, **kwargs)

    @property
    def client(self):
        return self.http_transport

    @property
    def clientAuth(self):
        return self._auth_token

    @property
    def user(self):
        return self._username

    @property
    def sessionHandle(self):
        return self._sessionHandle

    def rollback(self):
        raise Exception("Uniphi does not support transactions")  # pragma: no cover


class Cursor(common.DBAPICursor):
    """These objects represent a database cursor, which is used to manage the context of a fetch
    operation.
    Cursors are not isolated, i.e., any changes done to the database by a cursor are immediately
    visible by other cursors or connections.
    """

    def __init__(self, connection, arraysize=1000):
        super(Cursor, self).__init__()
        self._arraysize = arraysize
        self._connection = connection
        self.planUUID = None

    def _reset_state(self):
        """Reset state about the previous query in preparation for running another query"""
        pass

    @property
    def arraysize(self):
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        """Array size cannot be None, and should be an integer"""
        default_arraysize = 1000
        try:
            self._arraysize = int(value) or default_arraysize
        except TypeError:
            self._arraysize = default_arraysize

    @property
    def description(self):
        """This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column:
        - name
        - type_code
        - display_size (None in current implementation)
        - internal_size (None in current implementation)
        - precision (None in current implementation)
        - scale (None in current implementation)
        - null_ok (always True in current implementation)
        This attribute will be ``None`` for operations that do not return rows or if the cursor has
        not had an operation invoked via the :py:meth:`execute` method yet.
        The ``type_code`` can be interpreted by comparing it to the Type Objects specified in the
        section below.
        """
        return []
        # if self._operationHandle is None or not self._operationHandle.hasResultSet:
        #     return None
        # if self._description is None:
        #     req = ttypes.TGetResultSetMetadataReq(self._operationHandle)
        #     response = self._connection.client.GetResultSetMetadata(req)
        #     _check_status(response)
        #     columns = response.schema.columns
        #     self._description = []
        #     for col in columns:
        #         primary_type_entry = col.typeDesc.types[0]
        #         if primary_type_entry.primitiveEntry is None:
        #             # All fancy stuff maps to string
        #             type_code = ttypes.TTypeId._VALUES_TO_NAMES[ttypes.TTypeId.STRING_TYPE]
        #         else:
        #             type_id = primary_type_entry.primitiveEntry.type
        #             type_code = ttypes.TTypeId._VALUES_TO_NAMES[type_id]
        #         self._description.append((
        #             col.columnName.decode('utf-8') if sys.version_info[0] == 2 else col.columnName,
        #             type_code.decode('utf-8') if sys.version_info[0] == 2 else type_code,
        #             None, None, None, None, True
        #         ))
        # return self._description

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the operation handle"""
        pass

    def execute(self, operation, parameters=None, **kwargs):
        """Prepare and execute a database operation (query or command).
        Return values are not defined.
        """
        print("got command {op}".format(op=operation))

        if operation == "NOOP":
            return [{"test": "test"}]

        # Prepare statement
        if parameters is None:
            sql = operation
        else:
            sql = operation % _escaper.escape_args(parameters)

        _logger.info('%s', sql)

        sqlJson = {"sqlQuery": sql, "isPlain": "true", "planUuid": self.planUUID}

        transport = self._connection.client
        bearer = "Bearer " + self._connection.clientAuth
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*", "Authorization": bearer}
        # self._set_headers(http_transport, None)
        transport.request("POST", "/query", json.dumps(sqlJson), headers)
        response = transport.getresponse().read()
        print("got response from server ".format(response))
        responseDict = json.loads(response)
        return responseDict

    def get_view_names(self):
        user = self._connection.user
        transport = self._connection.client
        bearer = "Bearer " + self._connection.clientAuth
        headers = {"Content-Type": "text/plain", "Connection": "keep-alive", "Accept-Encoding": "gzip, deflate, br",
                   "Accept": "*/*", "Authorization": bearer}
        body = {"username": user}
        transport.request("POST", "/extract/preferences/fetch", json.dumps(body), headers)
        response = transport.getresponse()
        responseDict = json.loads(response.read())
        listOfViews = []
        for item in responseDict:
            dict = {}
            dict['ViewId'] = item['planUUID']
            dict['ViewName'] = item['planName']
            listOfViews.append(item['planName'])
        return listOfViews

    def cancel(self):
        """Uniphi does not support cancelling of queries as yet"""
        pass

    def _fetch_more(self):
        """Send another TFetchResultsReq and update state"""
        pass

    def poll(self, get_progress_update=True):
        """Poll for and return the raw status data provided by the Hive Thrift REST API.
        :returns: ``ttypes.TGetOperationStatusResp``
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass

    def fetch_logs(self):
        """Retrieve the logs produced by the execution of the query.
        Can be called multiple times to fetch the logs produced after the previous call.
        :returns: list<str>
        :raises: ``ProgrammingError`` when no query has been started
        .. note::
            This is not a part of DB-API.
        """
        pass

    def setContextForQuery(self, planId):
        self.planUUID = planId


#
# Type Objects and Constructors
#


for type_id in uniphi.constants.PRIMITIVE_TYPES:
    name = uniphi.typeId.TypeId._VALUES_TO_NAMES[type_id]
    setattr(sys.modules[__name__], name, DBAPITypeObject([name]))
