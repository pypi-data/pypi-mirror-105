"""
Type annotations for lakeformation service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_lakeformation.literals import ComparisonOperator

    data: ComparisonOperator = "BEGINS_WITH"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ComparisonOperator",
    "DataLakeResourceType",
    "FieldNameString",
    "Permission",
    "ResourceShareType",
    "ResourceType",
)


ComparisonOperator = Literal[
    "BEGINS_WITH", "BETWEEN", "CONTAINS", "EQ", "GE", "GT", "IN", "LE", "LT", "NE", "NOT_CONTAINS"
]
DataLakeResourceType = Literal[
    "CATALOG",
    "DATABASE",
    "DATA_LOCATION",
    "LF_TAG",
    "LF_TAG_POLICY",
    "LF_TAG_POLICY_DATABASE",
    "LF_TAG_POLICY_TABLE",
    "TABLE",
]
FieldNameString = Literal["LAST_MODIFIED", "RESOURCE_ARN", "ROLE_ARN"]
Permission = Literal[
    "ALL",
    "ALTER",
    "ALTER_TAG",
    "ASSOCIATE_TAG",
    "CREATE_DATABASE",
    "CREATE_TABLE",
    "CREATE_TAG",
    "DATA_LOCATION_ACCESS",
    "DELETE",
    "DELETE_TAG",
    "DESCRIBE",
    "DESCRIBE_TAG",
    "DROP",
    "INSERT",
    "SELECT",
]
ResourceShareType = Literal["ALL", "FOREIGN"]
ResourceType = Literal["DATABASE", "TABLE"]
