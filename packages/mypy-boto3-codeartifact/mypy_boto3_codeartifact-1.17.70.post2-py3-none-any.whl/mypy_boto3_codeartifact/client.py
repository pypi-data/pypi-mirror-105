"""
Type annotations for codeartifact service client.

[Open documentation](./client.md)

Usage::

    ```python
    import boto3
    from mypy_boto3_codeartifact import CodeArtifactClient

    client: CodeArtifactClient = boto3.client("codeartifact")
    ```
"""
import sys
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from mypy_boto3_codeartifact.paginator import (
    ListDomainsPaginator,
    ListPackagesPaginator,
    ListPackageVersionAssetsPaginator,
    ListPackageVersionsPaginator,
    ListRepositoriesInDomainPaginator,
    ListRepositoriesPaginator,
)

from .literals import PackageFormat, PackageVersionStatus
from .type_defs import (
    AssociateExternalConnectionResultTypeDef,
    CopyPackageVersionsResultTypeDef,
    CreateDomainResultTypeDef,
    CreateRepositoryResultTypeDef,
    DeleteDomainPermissionsPolicyResultTypeDef,
    DeleteDomainResultTypeDef,
    DeletePackageVersionsResultTypeDef,
    DeleteRepositoryPermissionsPolicyResultTypeDef,
    DeleteRepositoryResultTypeDef,
    DescribeDomainResultTypeDef,
    DescribePackageVersionResultTypeDef,
    DescribeRepositoryResultTypeDef,
    DisassociateExternalConnectionResultTypeDef,
    DisposePackageVersionsResultTypeDef,
    GetAuthorizationTokenResultTypeDef,
    GetDomainPermissionsPolicyResultTypeDef,
    GetPackageVersionAssetResultTypeDef,
    GetPackageVersionReadmeResultTypeDef,
    GetRepositoryEndpointResultTypeDef,
    GetRepositoryPermissionsPolicyResultTypeDef,
    ListDomainsResultTypeDef,
    ListPackagesResultTypeDef,
    ListPackageVersionAssetsResultTypeDef,
    ListPackageVersionDependenciesResultTypeDef,
    ListPackageVersionsResultTypeDef,
    ListRepositoriesInDomainResultTypeDef,
    ListRepositoriesResultTypeDef,
    ListTagsForResourceResultTypeDef,
    PutDomainPermissionsPolicyResultTypeDef,
    PutRepositoryPermissionsPolicyResultTypeDef,
    TagTypeDef,
    UpdatePackageVersionsStatusResultTypeDef,
    UpdateRepositoryResultTypeDef,
    UpstreamRepositoryTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeArtifactClient",)


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
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeArtifactClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client)
    [Show boto3-stubs documentation](./client.md)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def associate_external_connection(
        self, domain: str, repository: str, externalConnection: str, domainOwner: str = None
    ) -> AssociateExternalConnectionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.associate_external_connection)
        [Show boto3-stubs documentation](./client.md#associate-external-connection)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.can_paginate)
        [Show boto3-stubs documentation](./client.md#can-paginate)
        """

    def copy_package_versions(
        self,
        domain: str,
        sourceRepository: str,
        destinationRepository: str,
        format: PackageFormat,
        package: str,
        domainOwner: str = None,
        namespace: str = None,
        versions: List[str] = None,
        versionRevisions: Dict[str, str] = None,
        allowOverwrite: bool = None,
        includeFromUpstream: bool = None,
    ) -> CopyPackageVersionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.copy_package_versions)
        [Show boto3-stubs documentation](./client.md#copy-package-versions)
        """

    def create_domain(
        self, domain: str, encryptionKey: str = None, tags: List["TagTypeDef"] = None
    ) -> CreateDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.create_domain)
        [Show boto3-stubs documentation](./client.md#create-domain)
        """

    def create_repository(
        self,
        domain: str,
        repository: str,
        domainOwner: str = None,
        description: str = None,
        upstreams: List[UpstreamRepositoryTypeDef] = None,
        tags: List["TagTypeDef"] = None,
    ) -> CreateRepositoryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.create_repository)
        [Show boto3-stubs documentation](./client.md#create-repository)
        """

    def delete_domain(self, domain: str, domainOwner: str = None) -> DeleteDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain)
        [Show boto3-stubs documentation](./client.md#delete-domain)
        """

    def delete_domain_permissions_policy(
        self, domain: str, domainOwner: str = None, policyRevision: str = None
    ) -> DeleteDomainPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.delete_domain_permissions_policy)
        [Show boto3-stubs documentation](./client.md#delete-domain-permissions-policy)
        """

    def delete_package_versions(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        versions: List[str],
        domainOwner: str = None,
        namespace: str = None,
        expectedStatus: PackageVersionStatus = None,
    ) -> DeletePackageVersionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.delete_package_versions)
        [Show boto3-stubs documentation](./client.md#delete-package-versions)
        """

    def delete_repository(
        self, domain: str, repository: str, domainOwner: str = None
    ) -> DeleteRepositoryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository)
        [Show boto3-stubs documentation](./client.md#delete-repository)
        """

    def delete_repository_permissions_policy(
        self, domain: str, repository: str, domainOwner: str = None, policyRevision: str = None
    ) -> DeleteRepositoryPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.delete_repository_permissions_policy)
        [Show boto3-stubs documentation](./client.md#delete-repository-permissions-policy)
        """

    def describe_domain(self, domain: str, domainOwner: str = None) -> DescribeDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.describe_domain)
        [Show boto3-stubs documentation](./client.md#describe-domain)
        """

    def describe_package_version(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        packageVersion: str,
        domainOwner: str = None,
        namespace: str = None,
    ) -> DescribePackageVersionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.describe_package_version)
        [Show boto3-stubs documentation](./client.md#describe-package-version)
        """

    def describe_repository(
        self, domain: str, repository: str, domainOwner: str = None
    ) -> DescribeRepositoryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.describe_repository)
        [Show boto3-stubs documentation](./client.md#describe-repository)
        """

    def disassociate_external_connection(
        self, domain: str, repository: str, externalConnection: str, domainOwner: str = None
    ) -> DisassociateExternalConnectionResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.disassociate_external_connection)
        [Show boto3-stubs documentation](./client.md#disassociate-external-connection)
        """

    def dispose_package_versions(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        versions: List[str],
        domainOwner: str = None,
        namespace: str = None,
        versionRevisions: Dict[str, str] = None,
        expectedStatus: PackageVersionStatus = None,
    ) -> DisposePackageVersionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.dispose_package_versions)
        [Show boto3-stubs documentation](./client.md#dispose-package-versions)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.generate_presigned_url)
        [Show boto3-stubs documentation](./client.md#generate-presigned-url)
        """

    def get_authorization_token(
        self, domain: str, domainOwner: str = None, durationSeconds: int = None
    ) -> GetAuthorizationTokenResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_authorization_token)
        [Show boto3-stubs documentation](./client.md#get-authorization-token)
        """

    def get_domain_permissions_policy(
        self, domain: str, domainOwner: str = None
    ) -> GetDomainPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_domain_permissions_policy)
        [Show boto3-stubs documentation](./client.md#get-domain-permissions-policy)
        """

    def get_package_version_asset(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        packageVersion: str,
        asset: str,
        domainOwner: str = None,
        namespace: str = None,
        packageVersionRevision: str = None,
    ) -> GetPackageVersionAssetResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_asset)
        [Show boto3-stubs documentation](./client.md#get-package-version-asset)
        """

    def get_package_version_readme(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        packageVersion: str,
        domainOwner: str = None,
        namespace: str = None,
    ) -> GetPackageVersionReadmeResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_package_version_readme)
        [Show boto3-stubs documentation](./client.md#get-package-version-readme)
        """

    def get_repository_endpoint(
        self, domain: str, repository: str, format: PackageFormat, domainOwner: str = None
    ) -> GetRepositoryEndpointResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_endpoint)
        [Show boto3-stubs documentation](./client.md#get-repository-endpoint)
        """

    def get_repository_permissions_policy(
        self, domain: str, repository: str, domainOwner: str = None
    ) -> GetRepositoryPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.get_repository_permissions_policy)
        [Show boto3-stubs documentation](./client.md#get-repository-permissions-policy)
        """

    def list_domains(
        self, maxResults: int = None, nextToken: str = None
    ) -> ListDomainsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_domains)
        [Show boto3-stubs documentation](./client.md#list-domains)
        """

    def list_package_version_assets(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        packageVersion: str,
        domainOwner: str = None,
        namespace: str = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListPackageVersionAssetsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_assets)
        [Show boto3-stubs documentation](./client.md#list-package-version-assets)
        """

    def list_package_version_dependencies(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        packageVersion: str,
        domainOwner: str = None,
        namespace: str = None,
        nextToken: str = None,
    ) -> ListPackageVersionDependenciesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_package_version_dependencies)
        [Show boto3-stubs documentation](./client.md#list-package-version-dependencies)
        """

    def list_package_versions(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        domainOwner: str = None,
        namespace: str = None,
        status: PackageVersionStatus = None,
        sortBy: Literal["PUBLISHED_TIME"] = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListPackageVersionsResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_package_versions)
        [Show boto3-stubs documentation](./client.md#list-package-versions)
        """

    def list_packages(
        self,
        domain: str,
        repository: str,
        domainOwner: str = None,
        format: PackageFormat = None,
        namespace: str = None,
        packagePrefix: str = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListPackagesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_packages)
        [Show boto3-stubs documentation](./client.md#list-packages)
        """

    def list_repositories(
        self, repositoryPrefix: str = None, maxResults: int = None, nextToken: str = None
    ) -> ListRepositoriesResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories)
        [Show boto3-stubs documentation](./client.md#list-repositories)
        """

    def list_repositories_in_domain(
        self,
        domain: str,
        domainOwner: str = None,
        administratorAccount: str = None,
        repositoryPrefix: str = None,
        maxResults: int = None,
        nextToken: str = None,
    ) -> ListRepositoriesInDomainResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_repositories_in_domain)
        [Show boto3-stubs documentation](./client.md#list-repositories-in-domain)
        """

    def list_tags_for_resource(self, resourceArn: str) -> ListTagsForResourceResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](./client.md#list-tags-for-resource)
        """

    def put_domain_permissions_policy(
        self, domain: str, policyDocument: str, domainOwner: str = None, policyRevision: str = None
    ) -> PutDomainPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.put_domain_permissions_policy)
        [Show boto3-stubs documentation](./client.md#put-domain-permissions-policy)
        """

    def put_repository_permissions_policy(
        self,
        domain: str,
        repository: str,
        policyDocument: str,
        domainOwner: str = None,
        policyRevision: str = None,
    ) -> PutRepositoryPermissionsPolicyResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.put_repository_permissions_policy)
        [Show boto3-stubs documentation](./client.md#put-repository-permissions-policy)
        """

    def tag_resource(self, resourceArn: str, tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.tag_resource)
        [Show boto3-stubs documentation](./client.md#tag-resource)
        """

    def untag_resource(self, resourceArn: str, tagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.untag_resource)
        [Show boto3-stubs documentation](./client.md#untag-resource)
        """

    def update_package_versions_status(
        self,
        domain: str,
        repository: str,
        format: PackageFormat,
        package: str,
        versions: List[str],
        targetStatus: PackageVersionStatus,
        domainOwner: str = None,
        namespace: str = None,
        versionRevisions: Dict[str, str] = None,
        expectedStatus: PackageVersionStatus = None,
    ) -> UpdatePackageVersionsStatusResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.update_package_versions_status)
        [Show boto3-stubs documentation](./client.md#update-package-versions-status)
        """

    def update_repository(
        self,
        domain: str,
        repository: str,
        domainOwner: str = None,
        description: str = None,
        upstreams: List[UpstreamRepositoryTypeDef] = None,
    ) -> UpdateRepositoryResultTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Client.update_repository)
        [Show boto3-stubs documentation](./client.md#update-repository)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_domains"]) -> ListDomainsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListDomains)[Show boto3-stubs documentation](./paginators.md#listdomainspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_version_assets"]
    ) -> ListPackageVersionAssetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersionAssets)[Show boto3-stubs documentation](./paginators.md#listpackageversionassetspaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_package_versions"]
    ) -> ListPackageVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackageVersions)[Show boto3-stubs documentation](./paginators.md#listpackageversionspaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_packages"]) -> ListPackagesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListPackages)[Show boto3-stubs documentation](./paginators.md#listpackagespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositories)[Show boto3-stubs documentation](./paginators.md#listrepositoriespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories_in_domain"]
    ) -> ListRepositoriesInDomainPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.70/reference/services/codeartifact.html#CodeArtifact.Paginator.ListRepositoriesInDomain)[Show boto3-stubs documentation](./paginators.md#listrepositoriesindomainpaginator)
        """
