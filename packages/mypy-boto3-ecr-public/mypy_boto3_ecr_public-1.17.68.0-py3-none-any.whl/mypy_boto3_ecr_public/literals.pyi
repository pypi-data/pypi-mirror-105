"""
Type annotations for ecr-public service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ecr_public/literals.html)

Usage::

    ```python
    from mypy_boto3_ecr_public.literals import DescribeImageTagsPaginatorName

    data: DescribeImageTagsPaginatorName = "describe_image_tags"
    ```
"""
import sys

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "DescribeImageTagsPaginatorName",
    "DescribeImagesPaginatorName",
    "DescribeRegistriesPaginatorName",
    "DescribeRepositoriesPaginatorName",
    "ImageFailureCode",
    "LayerAvailability",
    "LayerFailureCode",
    "RegistryAliasStatus",
)

DescribeImageTagsPaginatorName = Literal["describe_image_tags"]
DescribeImagesPaginatorName = Literal["describe_images"]
DescribeRegistriesPaginatorName = Literal["describe_registries"]
DescribeRepositoriesPaginatorName = Literal["describe_repositories"]
ImageFailureCode = Literal[
    "ImageNotFound",
    "ImageReferencedByManifestList",
    "ImageTagDoesNotMatchDigest",
    "InvalidImageDigest",
    "InvalidImageTag",
    "KmsError",
    "MissingDigestAndTag",
]
LayerAvailability = Literal["AVAILABLE", "UNAVAILABLE"]
LayerFailureCode = Literal["InvalidLayerDigest", "MissingLayerDigest"]
RegistryAliasStatus = Literal["ACTIVE", "PENDING", "REJECTED"]
