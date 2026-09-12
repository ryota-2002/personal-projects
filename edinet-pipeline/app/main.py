"""EDINET提出書類一覧を取得し、S3へ保存するエントリーポイント。"""

import sys
import traceback
from datetime import datetime, timedelta, timezone

from config import get_api_key, get_s3_bucket
from edinet import EdinetAPIError, get_document_list
from s3 import S3UploadError, put_json

JST = timezone(timedelta(hours=9), name="JST")


def main() -> int:
    """当日分のEDINET提出書類一覧を取得してS3へ保存する。

    Returns:
        正常終了時は0、設定、API呼び出し、S3保存の失敗時は1。
    """
    try:
        target_date = datetime.now(JST).date()
        api_key = get_api_key()
        payload = get_document_list(target_date, api_key)
        bucket = get_s3_bucket()
        key = f"document_list/{target_date.isoformat()}.json"
        put_json(bucket, key, payload)
    except S3UploadError:
        traceback.print_exc(file=sys.stderr)
        return 1
    except (RuntimeError, EdinetAPIError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    print(
        f"EDINET提出書類一覧をS3へ保存しました: "
        f"target_date={target_date.isoformat()}, bucket={bucket}, key={key}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
