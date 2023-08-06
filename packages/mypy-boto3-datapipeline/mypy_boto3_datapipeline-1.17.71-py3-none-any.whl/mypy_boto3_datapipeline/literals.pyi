"""
Type annotations for datapipeline service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_datapipeline.literals import DescribeObjectsPaginatorName

    data: DescribeObjectsPaginatorName = "describe_objects"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "DescribeObjectsPaginatorName",
    "ListPipelinesPaginatorName",
    "OperatorType",
    "QueryObjectsPaginatorName",
    "TaskStatus",
)

DescribeObjectsPaginatorName = Literal["describe_objects"]
ListPipelinesPaginatorName = Literal["list_pipelines"]
OperatorType = Literal["BETWEEN", "EQ", "GE", "LE", "REF_EQ"]
QueryObjectsPaginatorName = Literal["query_objects"]
TaskStatus = Literal["FAILED", "FALSE", "FINISHED"]
