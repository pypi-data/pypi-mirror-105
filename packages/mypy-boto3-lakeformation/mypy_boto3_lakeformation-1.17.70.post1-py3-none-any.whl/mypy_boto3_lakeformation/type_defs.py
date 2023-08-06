"""
Type annotations for lakeformation service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_lakeformation/type_defs.html)

Usage::

    ```python
    from mypy_boto3_lakeformation.type_defs import AddLFTagsToResourceResponseTypeDef

    data: AddLFTagsToResourceResponseTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List

from mypy_boto3_lakeformation.literals import (
    ComparisonOperator,
    FieldNameString,
    Permission,
    ResourceType,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AddLFTagsToResourceResponseTypeDef",
    "BatchGrantPermissionsResponseTypeDef",
    "BatchPermissionsFailureEntryTypeDef",
    "BatchPermissionsRequestEntryTypeDef",
    "BatchRevokePermissionsResponseTypeDef",
    "ColumnLFTagTypeDef",
    "ColumnWildcardTypeDef",
    "DataLakePrincipalTypeDef",
    "DataLakeSettingsTypeDef",
    "DataLocationResourceTypeDef",
    "DatabaseResourceTypeDef",
    "DescribeResourceResponseTypeDef",
    "DetailsMapTypeDef",
    "ErrorDetailTypeDef",
    "FilterConditionTypeDef",
    "GetDataLakeSettingsResponseTypeDef",
    "GetEffectivePermissionsForPathResponseTypeDef",
    "GetLFTagResponseTypeDef",
    "GetResourceLFTagsResponseTypeDef",
    "LFTagErrorTypeDef",
    "LFTagKeyResourceTypeDef",
    "LFTagPairTypeDef",
    "LFTagPolicyResourceTypeDef",
    "LFTagTypeDef",
    "ListLFTagsResponseTypeDef",
    "ListPermissionsResponseTypeDef",
    "ListResourcesResponseTypeDef",
    "PrincipalPermissionsTypeDef",
    "PrincipalResourcePermissionsTypeDef",
    "RemoveLFTagsFromResourceResponseTypeDef",
    "ResourceInfoTypeDef",
    "ResourceTypeDef",
    "SearchDatabasesByLFTagsResponseTypeDef",
    "SearchTablesByLFTagsResponseTypeDef",
    "TableResourceTypeDef",
    "TableWithColumnsResourceTypeDef",
    "TaggedDatabaseTypeDef",
    "TaggedTableTypeDef",
)


class AddLFTagsToResourceResponseTypeDef(TypedDict, total=False):
    Failures: List["LFTagErrorTypeDef"]


class BatchGrantPermissionsResponseTypeDef(TypedDict, total=False):
    Failures: List["BatchPermissionsFailureEntryTypeDef"]


class BatchPermissionsFailureEntryTypeDef(TypedDict, total=False):
    RequestEntry: "BatchPermissionsRequestEntryTypeDef"
    Error: "ErrorDetailTypeDef"


class _RequiredBatchPermissionsRequestEntryTypeDef(TypedDict):
    Id: str


class BatchPermissionsRequestEntryTypeDef(
    _RequiredBatchPermissionsRequestEntryTypeDef, total=False
):
    Principal: "DataLakePrincipalTypeDef"
    Resource: "ResourceTypeDef"
    Permissions: List[Permission]
    PermissionsWithGrantOption: List[Permission]


class BatchRevokePermissionsResponseTypeDef(TypedDict, total=False):
    Failures: List["BatchPermissionsFailureEntryTypeDef"]


class ColumnLFTagTypeDef(TypedDict, total=False):
    Name: str
    LFTags: List["LFTagPairTypeDef"]


class ColumnWildcardTypeDef(TypedDict, total=False):
    ExcludedColumnNames: List[str]


class DataLakePrincipalTypeDef(TypedDict, total=False):
    DataLakePrincipalIdentifier: str


class DataLakeSettingsTypeDef(TypedDict, total=False):
    DataLakeAdmins: List["DataLakePrincipalTypeDef"]
    CreateDatabaseDefaultPermissions: List["PrincipalPermissionsTypeDef"]
    CreateTableDefaultPermissions: List["PrincipalPermissionsTypeDef"]
    TrustedResourceOwners: List[str]


class _RequiredDataLocationResourceTypeDef(TypedDict):
    ResourceArn: str


class DataLocationResourceTypeDef(_RequiredDataLocationResourceTypeDef, total=False):
    CatalogId: str


class _RequiredDatabaseResourceTypeDef(TypedDict):
    Name: str


class DatabaseResourceTypeDef(_RequiredDatabaseResourceTypeDef, total=False):
    CatalogId: str


class DescribeResourceResponseTypeDef(TypedDict, total=False):
    ResourceInfo: "ResourceInfoTypeDef"


class DetailsMapTypeDef(TypedDict, total=False):
    ResourceShare: List[str]


class ErrorDetailTypeDef(TypedDict, total=False):
    ErrorCode: str
    ErrorMessage: str


class FilterConditionTypeDef(TypedDict, total=False):
    Field: FieldNameString
    ComparisonOperator: ComparisonOperator
    StringValueList: List[str]


class GetDataLakeSettingsResponseTypeDef(TypedDict, total=False):
    DataLakeSettings: "DataLakeSettingsTypeDef"


class GetEffectivePermissionsForPathResponseTypeDef(TypedDict, total=False):
    Permissions: List["PrincipalResourcePermissionsTypeDef"]
    NextToken: str


class GetLFTagResponseTypeDef(TypedDict, total=False):
    CatalogId: str
    TagKey: str
    TagValues: List[str]


class GetResourceLFTagsResponseTypeDef(TypedDict, total=False):
    LFTagOnDatabase: List["LFTagPairTypeDef"]
    LFTagsOnTable: List["LFTagPairTypeDef"]
    LFTagsOnColumns: List["ColumnLFTagTypeDef"]


class LFTagErrorTypeDef(TypedDict, total=False):
    LFTag: "LFTagPairTypeDef"
    Error: "ErrorDetailTypeDef"


class _RequiredLFTagKeyResourceTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]


class LFTagKeyResourceTypeDef(_RequiredLFTagKeyResourceTypeDef, total=False):
    CatalogId: str


class _RequiredLFTagPairTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]


class LFTagPairTypeDef(_RequiredLFTagPairTypeDef, total=False):
    CatalogId: str


class _RequiredLFTagPolicyResourceTypeDef(TypedDict):
    ResourceType: ResourceType
    Expression: List["LFTagTypeDef"]


class LFTagPolicyResourceTypeDef(_RequiredLFTagPolicyResourceTypeDef, total=False):
    CatalogId: str


class LFTagTypeDef(TypedDict):
    TagKey: str
    TagValues: List[str]


class ListLFTagsResponseTypeDef(TypedDict, total=False):
    LFTags: List["LFTagPairTypeDef"]
    NextToken: str


class ListPermissionsResponseTypeDef(TypedDict, total=False):
    PrincipalResourcePermissions: List["PrincipalResourcePermissionsTypeDef"]
    NextToken: str


class ListResourcesResponseTypeDef(TypedDict, total=False):
    ResourceInfoList: List["ResourceInfoTypeDef"]
    NextToken: str


class PrincipalPermissionsTypeDef(TypedDict, total=False):
    Principal: "DataLakePrincipalTypeDef"
    Permissions: List[Permission]


class PrincipalResourcePermissionsTypeDef(TypedDict, total=False):
    Principal: "DataLakePrincipalTypeDef"
    Resource: "ResourceTypeDef"
    Permissions: List[Permission]
    PermissionsWithGrantOption: List[Permission]
    AdditionalDetails: "DetailsMapTypeDef"


class RemoveLFTagsFromResourceResponseTypeDef(TypedDict, total=False):
    Failures: List["LFTagErrorTypeDef"]


class ResourceInfoTypeDef(TypedDict, total=False):
    ResourceArn: str
    RoleArn: str
    LastModified: datetime


class ResourceTypeDef(TypedDict, total=False):
    Catalog: Dict[str, Any]
    Database: "DatabaseResourceTypeDef"
    Table: "TableResourceTypeDef"
    TableWithColumns: "TableWithColumnsResourceTypeDef"
    DataLocation: "DataLocationResourceTypeDef"
    LFTag: "LFTagKeyResourceTypeDef"
    LFTagPolicy: "LFTagPolicyResourceTypeDef"


class SearchDatabasesByLFTagsResponseTypeDef(TypedDict, total=False):
    NextToken: str
    DatabaseList: List["TaggedDatabaseTypeDef"]


class SearchTablesByLFTagsResponseTypeDef(TypedDict, total=False):
    NextToken: str
    TableList: List["TaggedTableTypeDef"]


class _RequiredTableResourceTypeDef(TypedDict):
    DatabaseName: str


class TableResourceTypeDef(_RequiredTableResourceTypeDef, total=False):
    CatalogId: str
    Name: str
    TableWildcard: Dict[str, Any]


class _RequiredTableWithColumnsResourceTypeDef(TypedDict):
    DatabaseName: str
    Name: str


class TableWithColumnsResourceTypeDef(_RequiredTableWithColumnsResourceTypeDef, total=False):
    CatalogId: str
    ColumnNames: List[str]
    ColumnWildcard: "ColumnWildcardTypeDef"


class TaggedDatabaseTypeDef(TypedDict, total=False):
    Database: "DatabaseResourceTypeDef"
    LFTags: List["LFTagPairTypeDef"]


class TaggedTableTypeDef(TypedDict, total=False):
    Table: "TableResourceTypeDef"
    LFTagOnDatabase: List["LFTagPairTypeDef"]
    LFTagsOnTable: List["LFTagPairTypeDef"]
    LFTagsOnColumns: List["ColumnLFTagTypeDef"]
