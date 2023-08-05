"""
Type annotations for dataexchange service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_dataexchange import DataExchangeClient

    client: DataExchangeClient = boto3.client("dataexchange")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_dataexchange.literals import TypeType
from mypy_boto3_dataexchange.paginator import (
    ListDataSetRevisionsPaginator,
    ListDataSetsPaginator,
    ListJobsPaginator,
    ListRevisionAssetsPaginator,
)
from mypy_boto3_dataexchange.type_defs import (
    CreateDataSetResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateRevisionResponseTypeDef,
    GetAssetResponseTypeDef,
    GetDataSetResponseTypeDef,
    GetJobResponseTypeDef,
    GetRevisionResponseTypeDef,
    ListDataSetRevisionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListJobsResponseTypeDef,
    ListRevisionAssetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RequestDetailsTypeDef,
    UpdateAssetResponseTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateRevisionResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DataExchangeClient",)

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
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class DataExchangeClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#can-paginate)
        """
    def cancel_job(self, JobId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.cancel_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#cancel-job)
        """
    def create_data_set(
        self,
        AssetType: Literal["S3_SNAPSHOT"],
        Description: str,
        Name: str,
        Tags: Dict[str, str] = None,
    ) -> CreateDataSetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.create_data_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#create-data-set)
        """
    def create_job(
        self, Details: RequestDetailsTypeDef, Type: TypeType
    ) -> CreateJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.create_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#create-job)
        """
    def create_revision(
        self, DataSetId: str, Comment: str = None, Tags: Dict[str, str] = None
    ) -> CreateRevisionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.create_revision)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#create-revision)
        """
    def delete_asset(self, AssetId: str, DataSetId: str, RevisionId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.delete_asset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#delete-asset)
        """
    def delete_data_set(self, DataSetId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.delete_data_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#delete-data-set)
        """
    def delete_revision(self, DataSetId: str, RevisionId: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.delete_revision)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#delete-revision)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#generate-presigned-url)
        """
    def get_asset(self, AssetId: str, DataSetId: str, RevisionId: str) -> GetAssetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.get_asset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#get-asset)
        """
    def get_data_set(self, DataSetId: str) -> GetDataSetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.get_data_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#get-data-set)
        """
    def get_job(self, JobId: str) -> GetJobResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.get_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#get-job)
        """
    def get_revision(self, DataSetId: str, RevisionId: str) -> GetRevisionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.get_revision)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#get-revision)
        """
    def list_data_set_revisions(
        self, DataSetId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListDataSetRevisionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.list_data_set_revisions)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#list-data-set-revisions)
        """
    def list_data_sets(
        self, MaxResults: int = None, NextToken: str = None, Origin: str = None
    ) -> ListDataSetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.list_data_sets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#list-data-sets)
        """
    def list_jobs(
        self,
        DataSetId: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        RevisionId: str = None,
    ) -> ListJobsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.list_jobs)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#list-jobs)
        """
    def list_revision_assets(
        self, DataSetId: str, RevisionId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListRevisionAssetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.list_revision_assets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#list-revision-assets)
        """
    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#list-tags-for-resource)
        """
    def start_job(self, JobId: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.start_job)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#start-job)
        """
    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#tag-resource)
        """
    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#untag-resource)
        """
    def update_asset(
        self, AssetId: str, DataSetId: str, Name: str, RevisionId: str
    ) -> UpdateAssetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.update_asset)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#update-asset)
        """
    def update_data_set(
        self, DataSetId: str, Description: str = None, Name: str = None
    ) -> UpdateDataSetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.update_data_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#update-data-set)
        """
    def update_revision(
        self, DataSetId: str, RevisionId: str, Comment: str = None, Finalized: bool = None
    ) -> UpdateRevisionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Client.update_revision)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/client.html#update-revision)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_set_revisions"]
    ) -> ListDataSetRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSetRevisions)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetrevisionspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_data_sets"]) -> ListDataSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Paginator.ListDataSets)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listdatasetspaginator)
        """
    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Paginator.ListJobs)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listjobspaginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_revision_assets"]
    ) -> ListRevisionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.68/reference/services/dataexchange.html#DataExchange.Paginator.ListRevisionAssets)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dataexchange/paginators.html#listrevisionassetspaginator)
        """
