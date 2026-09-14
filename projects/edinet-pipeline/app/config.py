"""EDINET APIクライアントで使用する設定を管理するモジュール。"""
import os

from dotenv import load_dotenv

load_dotenv()


# 接続先やリクエスト条件はこのモジュールに集約し、変更を容易にします。
EDINET_API_BASE_URL = "https://api.edinet-fsa.go.jp"
DOCUMENTS_ENDPOINT = "/api/v2/documents.json"
REQUEST_TIMEOUT_SECONDS = 30.0
DOCUMENT_LIST_TYPE = 2
API_KEY_ENV_NAME = "EDINET_API_KEY"
S3_BUCKET_ENV_NAME = "S3_BUCKET"


def get_api_key() -> str:
    """環境変数からEDINET APIキーを取得する。

    Returns:
        前後の空白を除去したAPIキー。

    Raises:
        RuntimeError: APIキーが環境変数に設定されていない場合。
    """
    api_key = os.getenv(API_KEY_ENV_NAME, "").strip()
    if not api_key:
        raise RuntimeError(
            f"環境変数 {API_KEY_ENV_NAME} にEDINET APIキーを設定してください。"
        )
    return api_key


def get_s3_bucket() -> str:
    """環境変数から保存先S3バケット名を取得する。

    Returns:
        前後の空白を除去したS3バケット名。

    Raises:
        RuntimeError: バケット名が環境変数に設定されていない場合。
    """
    bucket = os.getenv(S3_BUCKET_ENV_NAME, "").strip()
    if not bucket:
        raise RuntimeError(
            f"環境変数 {S3_BUCKET_ENV_NAME} にS3バケット名を設定してください。"
        )
    return bucket
