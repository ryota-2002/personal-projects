# EDINET Pipeline

EDINET API v2から日本時間の当日分の提出書類一覧を取得し、JSONをS3へ保存する1回実行型のバッチです。

## 必要環境

- Docker
- EDINET APIキー
- 保存先S3バケット

Pythonの依存関係は `pyproject.toml` で宣言し、`uv.lock` で固定しています。`requirements.txt` は使用しません。

## Dockerでの実行

```sh
docker build -t edinet-pipeline:local .
docker run --rm \
  -e EDINET_API_KEY="your-api-key" \
  -e S3_BUCKET="your-bucket-name" \
  edinet-pipeline:local
```

ローカルの `.env` を使う場合は、イメージにコピーせず実行時に渡します。

```sh
docker run --rm --env-file .env edinet-pipeline:local
```

`EDINET_API_KEY` または `S3_BUCKET` が未設定、API通信が失敗、レスポンスが不正、またはS3保存が失敗した場合は標準エラーへ理由を出力し、終了コード1で終了します。
S3保存の失敗時は、保存先バケット・キーに加え、原因となったAWS SDKの例外（エラーコード・メッセージなど）とトレースバックを標準エラーへ出力します。

## ローカル開発

```sh
uv sync --locked
uv run python app/main.py
```

`.env` はGitとDocker build contextの両方から除外されます。コミットしないでください。開発開始時は `.env.example` を `.env` へコピーし、APIキーを設定します。

## AWS運用

このコンテナは常駐Webサービスではなくバッチです。ECS Serviceではなく、EventBridge SchedulerからECS `RunTask` を実行する構成を想定しています。

ECSタスク定義では以下を設定します。

- Secrets ManagerのAPIキーをコンテナの `EDINET_API_KEY` へ注入
- 保存先バケット名をコンテナの環境変数 `S3_BUCKET` に設定
- `awslogs` ログドライバでCloudWatch Logsへ出力
- ECR pullとSecrets Manager参照権限をタスク実行ロールへ付与
- 保存先バケットへの `s3:PutObject` 権限をタスクロールへ付与
- EDINETのパブリックAPIへ接続できるアウトバウンド経路を用意
- 必要なCPU、メモリ、失敗通知、再試行ポリシーを設定

取得したJSONは `document_list/YYYY-MM-DD.json` というキーでS3へ保存されます。AWS認証にはECSタスクロールを使用します。

## ECR Push前の確認

```sh
docker build --pull -t edinet-pipeline:local .
docker run --rm edinet-pipeline:local
docker run --rm --env-file .env edinet-pipeline:local
```

2つ目のコマンドが設定不足として終了コード1になり、3つ目がS3への保存完了ログを出力して終了コード0になることを確認します。ローカル実行時は、S3へ書き込めるAWS認証情報が別途必要です。
