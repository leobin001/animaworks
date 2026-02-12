## 外部ツール

以下の外部ツールが `animaworks-tool` コマンド経由で使えます。
Bashツールから実行してください。出力はJSON形式（`-j` オプション）を推奨します。

### Web検索
```bash
animaworks-tool web_search "検索クエリ" -j
animaworks-tool web_search "検索クエリ" -n 5 -l ja -j
```

### X (Twitter) 検索
```bash
animaworks-tool x_search "検索クエリ" -j
animaworks-tool x_search --user ユーザー名 -j
animaworks-tool x_search "検索クエリ" --days 3 -n 10 -j
```

### Chatwork
```bash
animaworks-tool chatwork rooms -j
animaworks-tool chatwork messages <ルーム名またはID> -j
animaworks-tool chatwork send <ルーム名またはID> "メッセージ本文"
animaworks-tool chatwork search "キーワード" -j
animaworks-tool chatwork unreplied -j
```

### Slack
```bash
animaworks-tool slack channels -j
animaworks-tool slack messages <チャンネル名またはID> -j
animaworks-tool slack send <チャンネル名またはID> "メッセージ本文"
animaworks-tool slack search "キーワード" -j
animaworks-tool slack unreplied -j
```

### Gmail
```bash
animaworks-tool gmail unread -j
animaworks-tool gmail read <メッセージID>
animaworks-tool gmail draft --to "宛先" --subject "件名" --body "本文"
```

### ローカルLLM (Ollama)
```bash
animaworks-tool local_llm generate "プロンプト"
animaworks-tool local_llm chat '{"messages":[{"role":"user","content":"質問"}]}'
animaworks-tool local_llm list -j
animaworks-tool local_llm status -j
```

### 音声認識
```bash
animaworks-tool transcribe <音声ファイルパス> -j
animaworks-tool transcribe <音声ファイルパス> --raw -j
```

### AWS モニタリング
```bash
animaworks-tool aws_collector ecs-status --cluster <クラスタ> --service <サービス> -j
animaworks-tool aws_collector error-logs --log-group <ロググループ> --hours 2 -j
animaworks-tool aws_collector metrics --cluster <クラスタ> --service <サービス> --metric CPUUtilization -j
```

### GitHub
```bash
animaworks-tool github issues -j
animaworks-tool github issues --repo owner/repo -j
animaworks-tool github issue 123 -j
animaworks-tool github create-issue --title "タイトル" --body "本文"
animaworks-tool github prs -j
animaworks-tool github create-pr --title "タイトル" --body "本文" --head ブランチ名
```

### 注意事項
- 使えるツールは permissions.md の「外部ツール」セクションで許可されたもののみ
- APIキーが未設定のツールはエラーになる。エラー内容を確認して報告すること
- 検索結果やメッセージ一覧は記憶に保存すべきか判断すること
