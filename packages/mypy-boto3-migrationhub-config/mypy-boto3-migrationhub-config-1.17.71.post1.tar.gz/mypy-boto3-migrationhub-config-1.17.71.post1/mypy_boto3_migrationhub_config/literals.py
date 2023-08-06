"""
Type annotations for migrationhub-config service literal definitions.

[Open documentation](./literals.md)

Usage::

    ```python
    from mypy_boto3_migrationhub_config.literals import TargetType

    data: TargetType = "ACCOUNT"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TargetType",)


TargetType = Literal["ACCOUNT"]
