"""
Type annotations for meteringmarketplace service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_meteringmarketplace.literals import UsageRecordResultStatus

    data: UsageRecordResultStatus = "CustomerNotSubscribed"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("UsageRecordResultStatus",)


UsageRecordResultStatus = Literal["CustomerNotSubscribed", "DuplicateRecord", "Success"]
