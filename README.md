# オリエンタルスパーク AI組織システム

Claude Codeを使った、オリエンタルスパーク向けのAIエージェント組織です。

## AI組織の構成

```
CEO Agent（戦略・意思決定）
├── Marketing Agent（マーケティング・コンテンツ）
├── Sales Agent（営業サポート・顧客管理）
├── Operations Agent（業務効率化・社内フロー）
└── Research Agent（情報収集・市場調査）
```

## 使えるコマンド（Skills）

| コマンド | 説明 |
|---------|------|
| `/task-assign [タスク内容]` | タスクを分析して担当エージェントに割り当て |
| `/daily-report` | 今日の作業をまとめた日次レポートを作成 |
| `/meeting-notes [メモ]` | 会議メモを構造化した議事録に変換 |
| `/research [テーマ]` | 指定テーマの調査レポートを作成 |
| `/proposal [顧客・課題]` | 顧客向け提案書のドラフトを作成 |

## フォルダ構成

```
.
├── CLAUDE.md                    # 長期記憶・プロジェクト知識ベース
├── README.md                    # このファイル
├── agents/                      # エージェント定義
│   ├── ceo-agent.md
│   ├── marketing-agent.md
│   ├── sales-agent.md
│   ├── operations-agent.md
│   └── research-agent.md
├── .claude/
│   └── commands/                # Skillsコマンド定義
│       ├── task-assign.md
│       ├── daily-report.md
│       ├── meeting-notes.md
│       ├── research.md
│       └── proposal.md
├── docs/
│   ├── tasks/                   # タスク管理ファイル
│   └── decisions/               # 重要な意思決定の記録
└── outputs/                     # 成果物の保存場所
```

## はじめ方

1. `CLAUDE.md` の「会社情報」セクションをオリエンタルスパークの実際の情報に更新する
2. タスクが来たら `/task-assign [タスク内容]` で開始する
3. 成果物は `outputs/` に自動保存される

## Claude Codeの基礎知識

### 知識の蓄積方法
- **CLAUDE.md** に書いた内容は、スレッドが変わっても毎回読み込まれる
- `~/.claude/CLAUDE.md` はすべてのプロジェクトで共通して読まれる
- このファイル（`/my-first-project/CLAUDE.md`）はこのプロジェクト専用

### Skillsの仕組み
- `.claude/commands/` フォルダに `.md` ファイルを置く
- `/ファイル名` でコマンドとして呼び出せる
- `$ARGUMENTS` で引数を受け取れる

### できること・できないこと
| できること | できないこと（直接は） |
|---|---|
| ローカルファイルの読み書き | Google Sheets直接編集 |
| Git操作 | ブラウザ操作 |
| APIリクエスト | 他スレッドの会話記憶 |
| コード実行 | リアルタイムWeb閲覧 |
