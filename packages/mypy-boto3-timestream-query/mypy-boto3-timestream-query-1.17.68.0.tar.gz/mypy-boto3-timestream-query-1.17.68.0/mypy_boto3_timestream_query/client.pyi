"""
Type annotations for timestream-query service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_timestream_query import TimestreamQueryClient

    client: TimestreamQueryClient = boto3.client("timestream-query")
    ```
"""
import sys
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from mypy_boto3_timestream_query.paginator import QueryPaginator
from mypy_boto3_timestream_query.type_defs import (
    CancelQueryResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    QueryResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("TimestreamQueryClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEndpointException: Type[BotocoreClientError]
    QueryExecutionException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class TimestreamQueryClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html#can-paginate)
        """
    def cancel_query(self, QueryId: str) -> CancelQueryResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client.cancel_query)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html#cancel-query)
        """
    def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client.describe_endpoints)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html#describe-endpoints)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html#generate-presigned-url)
        """
    def query(
        self, QueryString: str, ClientToken: str = None, NextToken: str = None, MaxRows: int = None
    ) -> QueryResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Client.query)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client.html#query)
        """
    def get_paginator(self, operation_name: Literal["query"]) -> QueryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/timestream-query.html#TimestreamQuery.Paginator.Query)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators.html#querypaginator)
        """
