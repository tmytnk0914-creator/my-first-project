# 業務改善キット(企画・マーケ・制作向け)

データ整理とレポート作成の時間を減らし、AI活用の型を身につけるためのツール一式。

## 何が入っているか

| 場所 | 内容 |
|---|---|
| `docs/00_業務マップ.md` | 業務の棚卸しと「人間 vs AI」の分担表 |
| `docs/01_自動化候補一覧.md` | 自動化候補15案と優先順位 |
| `docs/02_運用ルール.md` | ファイル命名・保存・AI活用の安全ルール |
| `docs/99_最終レポート.md` | 今回の改善プロジェクトの最終レポート |
| `scripts/clean_data.py` | Excel/CSV整形スクリプト(表記ゆれ・重複・空行を自動処理) |
| `prompts/` | コピペで使える定型プロンプト集(どのAIでも可) |
| `templates/提出前チェックリスト.md` | レポート・企画書の提出前チェック |
| `.claude/skills/` | Claude Code用Skill(`/data-clean` `/report-draft` `/weekly-review`) |
| `samples/` | 動作確認用のサンプルデータ |

## クイックスタート

### 1. データ整形を試す(30秒)
```bash
python3 scripts/clean_data.py samples/サンプル_汚れたデータ.csv --out /tmp
```
→ 整形済みファイルとサマリーが出力される。自分のExcel/CSVでも同じ。
※初回のみ: `pip3 install pandas openpyxl`

### 2. Claude Codeでの使い方
このフォルダでClaude Codeを開き、次のように呼び出す:
- `/data-clean` — データ整理を任せる
- `/report-draft` — レポート・企画書の初稿を作らせる
- `/weekly-review` — 週次ふりかえりを作る

### 3. どのAIでも使えるプロンプト
`prompts/` のファイルを開き、【 】を書き換えて貼るだけ。
プロンプトの書き方の型は `prompts/README.md` 参照。

## 明日からの運用手順
1. **朝**: 受領データは `01_受領データ/` に保存(命名ルール: `YYYYMMDD_種類_内容_v1`)
2. **データ作業の前**: まず `clean_data.py`(または `/data-clean`)に整形させる
3. **資料を書く前**: `/report-draft` か `prompts/企画書たたき台.md` でたたき台を作ってから直す
4. **提出前**: `templates/提出前チェックリスト.md` を必ず通す(AIの数値は検算)
5. **金曜15分**: `/weekly-review` でふりかえり、自動化候補を1つ追記する
