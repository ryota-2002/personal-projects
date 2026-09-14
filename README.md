# personal-projects

個人プロジェクトを1つのGitリポジトリで管理するためのmonorepoです。

## ディレクトリ構成

各プロジェクトは `projects/<プロジェクト名>/` に配置します。

```text
personal-projects/
├── README.md
├── .gitignore
└── projects/
    └── edinet-pipeline/
```

## プロジェクトの追加

```bash
mkdir -p projects/<プロジェクト名>
```

作成したディレクトリには、目的や実行方法を記載した `README.md` を置きます。
このリポジトリ全体で履歴を管理するため、各プロジェクト内では `git init` を実行しません。

## プロジェクト一覧

- [edinet-pipeline](projects/edinet-pipeline/README.md)
