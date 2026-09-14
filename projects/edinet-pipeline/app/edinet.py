"""EDINET APIとのHTTP通信を担当するモジュール。"""

from datetime import date
from typing import Any

import requests

from config import (
    DOCUMENT_LIST_TYPE,
    DOCUMENTS_ENDPOINT,
    EDINET_API_BASE_URL,
    REQUEST_TIMEOUT_SECONDS,
)

JsonObject = dict[str, Any]


class EdinetAPIError(Exception):
    """EDINET APIの呼び出しに失敗した場合の基底例外。"""


class EdinetTimeoutError(EdinetAPIError):
    """EDINET APIへの接続がタイムアウトした場合の例外。"""


class EdinetHTTPError(EdinetAPIError):
    """EDINET APIがHTTPエラーを返した場合の例外。"""


class EdinetConnectionError(EdinetAPIError):
    """EDINET APIとの通信に失敗した場合の例外。"""


class EdinetJSONDecodeError(EdinetAPIError):
    """EDINET APIのレスポンスをJSONとして解釈できない場合の例外。"""


def _get_json(url: str, params: dict[str, str | int]) -> JsonObject:
    """GETリクエストを送り、レスポンスをJSONオブジェクトとして返す。

    Args:
        url: リクエスト先の完全なURL。
        params: URLへ付与するクエリパラメータ。

    Returns:
        EDINET APIから返されたJSONオブジェクト。

    Raises:
        EdinetTimeoutError: リクエストがタイムアウトした場合。
        EdinetHTTPError: HTTPステータスがエラーを示す場合。
        EdinetConnectionError: その他の通信エラーが発生した場合。
        EdinetJSONDecodeError: レスポンスをJSONとして解析できない場合。
    """
    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.Timeout as exc:
        raise EdinetTimeoutError(
            "EDINET APIへのリクエストがタイムアウトしました。"
        ) from exc
    except requests.HTTPError as exc:
        status_code = (
            exc.response.status_code if exc.response is not None else "不明"
        )
        raise EdinetHTTPError(
            f"EDINET APIがHTTPエラーを返しました: {status_code}"
        ) from exc
    except requests.RequestException as exc:
        raise EdinetConnectionError(
            "EDINET APIとの通信に失敗しました。"
        ) from exc

    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise EdinetJSONDecodeError(
            "EDINET APIのレスポンスをJSONとして解析できませんでした。"
        ) from exc

    if not isinstance(payload, dict):
        raise EdinetJSONDecodeError(
            "EDINET APIのJSONレスポンスがオブジェクトではありません。"
        )
    return payload


def get_document_list(target_date: date, api_key: str) -> JsonObject:
    """指定日の提出書類一覧をEDINET APIから取得する。

    Args:
        target_date: 一覧を取得する日付。
        api_key: EDINETから発行されたAPIキー。

    Returns:
        提出書類一覧を含むJSONオブジェクト。
    """
    url = f"{EDINET_API_BASE_URL}{DOCUMENTS_ENDPOINT}"
    params: dict[str, str | int] = {
        "date": target_date.isoformat(),
        "type": DOCUMENT_LIST_TYPE,
        "Subscription-Key": api_key,
    }
    return _get_json(url, params)
