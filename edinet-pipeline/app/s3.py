"""JSONデータのS3保存を担当するモジュール。"""

import json
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class S3UploadError(Exception):
    """S3への保存に失敗した場合の例外。"""


def put_json(bucket: str, key: str, payload: dict[str, Any]) -> None:
    """Pythonの辞書をUTF-8のJSONとしてS3へ保存する。

    Args:
        bucket: 保存先S3バケット名。
        key: 保存先オブジェクトキー。
        payload: 保存するJSONオブジェクト。

    Raises:
        S3UploadError: S3への保存に失敗した場合。
    """
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    try:
        boto3.client("s3").put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            ContentType="application/json",
        )
    except (BotoCoreError, ClientError) as exc:
        raise S3UploadError(
            f"S3へのJSON保存に失敗しました (bucket={bucket}, key={key}): "
            f"{type(exc).__name__}: {exc}"
        ) from exc
