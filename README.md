# Research Git Practice

研究開発でGit・GitHubを使う流れを練習するためのRepositoryです。

## 実習ルール

- `main`では直接作業しない
- 最新の`main`から作業用Branchを作る
- 基本実習では自分の学籍番号をファイル名に使う
- Commit前に差分を確認する
- Pull Requestを作成し、Review後にMergeする
- パスワード、APIキー、個人情報、生の大容量データを追加しない

## 動作環境

- Git
- Python 3.9以降を推奨
- Visual Studio Codeを推奨

外部Pythonパッケージは使用しません。

## サンプル評価

```bash
python src/evaluate.py --config config/examples/default.json --data data/sample/measurements.csv
```

Windowsで`python`が利用できない場合は、`py`へ置き換えてください。

期待される結果：

```text
sample_count: 8
mean_error: 0.2375
max_error: 0.5000
threshold: 0.3000
within_threshold_rate: 0.7500
```

## 個人実習

1. `config/examples/default.json`を`config/users/<学籍番号>.json`へコピーする
2. `threshold`を変更する
3. 次を実行する

```bash
python src/evaluate.py --config config/users/<学籍番号>.json --data data/sample/measurements.csv --output experiments/<学籍番号>/run01.md
```

4. `members/<学籍番号>.md`を追加する
5. Commit・PushしてPull Requestを作る

## フォルダー構成

```text
.github/       Issue・Pull Requestテンプレート
config/        評価条件
  examples/    共有する設定例
  users/       実習参加者の個人設定
data/sample/   Gitに含められる小さなサンプルデータ
docs/          手順・方針・共同編集用文書
experiments/   実験条件・結果・考察
members/       参加者情報
src/           評価スクリプト
```

## 大容量データ

生データ、動画、モデル、巨大ログはこのRepositoryへ直接入れません。実際の研究では、保存場所・版・対応するCommitを実験記録へ記載します。
