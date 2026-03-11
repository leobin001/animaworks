# Common Knowledge — 目次・クイックガイド

AnimaWorks の全 Anima が共有する日常ガイド。
困ったとき・手順が不明なときは、このファイルで該当ドキュメントを特定し、
`read_memory_file(path="common_knowledge/...")` で詳細を参照すること。

> 💡 詳細な技術リファレンス（構成ファイル仕様・モデル設定・認証設定・ユースケース等）は `reference/` に移動しました。
> 目次: `reference/00_index.md`

---

## 困ったときのクイックガイド

### コミュニケーション

| 困りごと | 参照先 |
|---------|--------|
| Board（共有チャネル）の使い方がわからない | `communication/board-guide.md` |
| 人間への通知方法がわからない | `communication/call-human-guide.md` |
| メッセージ送信が制限された | `communication/sending-limits.md` |
| メッセージの送り方がわからない | `reference/communication/messaging-guide.md` ※技術リファレンス |
| 指示の出し方・報告の仕方がわからない | `reference/communication/instruction-patterns.md` / `reference/communication/reporting-guide.md` ※技術リファレンス |
| Slack ボットトークンの設定がわからない | `reference/communication/slack-bot-token-guide.md` ※技術リファレンス |

### 組織・階層

| 困りごと | 参照先 |
|---------|--------|
| 階層間の通信ルールがわからない | `organization/hierarchy-rules.md` |
| 役割と責任範囲を確認したい | `reference/organization/roles.md` ※技術リファレンス |
| 組織構造・誰に連絡すべきかわからない | `reference/organization/structure.md` ※技術リファレンス |

### タスク・運用

| 困りごと | 参照先 |
|---------|--------|
| タスクボード（人間向けダッシュボード）を使いたい | `operations/task-board-guide.md` |
| 長時間ツールの実行方法がわからない | `operations/background-tasks.md` |
| タスク管理の方法がわからない | `reference/operations/task-management.md` ※技術リファレンス |
| ハートビートやcronの設定がわからない | `reference/operations/heartbeat-cron-guide.md` ※技術リファレンス |
| プロジェクト設定を変更したい | `reference/operations/project-setup.md` ※技術リファレンス |

### ツール・モデル・技術

| 困りごと | 参照先 |
|---------|--------|
| ツールの使い方・呼び出し方がわからない | `reference/operations/tool-usage-overview.md` ※技術リファレンス |
| モデルの選び方・変更方法がわからない | `reference/operations/model-guide.md` ※技術リファレンス |
| Mode S の認証方式を変えたい | `reference/operations/mode-s-auth-guide.md` ※技術リファレンス |
| 音声チャットの設定・使い方がわからない | `reference/operations/voice-chat-guide.md` ※技術リファレンス |

### 自分自身の理解

| 困りごと | 参照先 |
|---------|--------|
| Animaとは何か知りたい | `anatomy/what-is-anima.md` |
| 記憶の仕組み・種類を知りたい | `reference/anatomy/memory-system.md` ※技術リファレンス |
| 自分の構成ファイルの役割を知りたい | `reference/anatomy/anima-anatomy.md` ※技術リファレンス |

### トラブルシューティング

| 困りごと | 参照先 |
|---------|--------|
| ツールやコマンドが使えない / エラーが出る | `reference/troubleshooting/common-issues.md` ※技術リファレンス |
| タスクがブロックされた / 判断に迷う | `reference/troubleshooting/escalation-flowchart.md` ※技術リファレンス |
| Gmail ツールの認証設定がうまくいかない | `reference/troubleshooting/gmail-credential-setup.md` ※技術リファレンス |

### セキュリティ

| 困りごと | 参照先 |
|---------|--------|
| 外部データの信頼性が気になる | `security/prompt-injection-awareness.md` |

### 活用例

| 困りごと | 参照先 |
|---------|--------|
| AnimaWorksで何ができるか知りたい | `reference/usecases/usecase-overview.md` ※技術リファレンス |

**上記に該当しない場合** → `search_memory(query="キーワード", scope="common_knowledge")` で検索する

---

## ドキュメント一覧

### anatomy/ — Animaの構成要素

| ファイル | 概要 |
|---------|------|
| `what-is-anima.md` | Animaとは何か（概念・設計思想・ライフサイクル・実行パス） |

### organization/ — 組織・構造

| ファイル | 概要 |
|---------|------|
| `hierarchy-rules.md` | 階層間のルール（通信経路、スーパーバイザーツール、緊急時の例外） |

### communication/ — コミュニケーション

| ファイル | 概要 |
|---------|------|
| `board-guide.md` | Board（共有チャネル）ガイド（post_channel / read_channel の使い分け、投稿ルール） |
| `call-human-guide.md` | 人間への通知ガイド（call_human の使い方、返信の受け取り、通知チャネル設定） |
| `sending-limits.md` | 送信制限の詳細（3層レート制限、30/h・100/day 上限、カスケード検出、対処法） |

### operations/ — 運用・タスク管理

| ファイル | 概要 |
|---------|------|
| `task-board-guide.md` | タスクボード（人間向けダッシュボード）の仕組みと運用方法 |
| `background-tasks.md` | バックグラウンドタスク実行ガイド（submit の使い方、判断基準、結果の受け取り方） |

### security/ — セキュリティ

| ファイル | 概要 |
|---------|------|
| `prompt-injection-awareness.md` | プロンプトインジェクション防御ガイド（信頼レベル、境界タグ、untrusted データの処理ルール） |

---

## キーワード索引

| キーワード | 参照先 |
|-----------|--------|
| Board, チャネル, post_channel, read_channel | `communication/board-guide.md` |
| DM履歴, read_dm_history, 過去の会話 | `communication/board-guide.md` |
| call_human, 人間通知, 人間に連絡, 通知チャネル | `communication/call-human-guide.md` |
| レート制限, 送信制限, 30通, 100通, 1ラウンドルール | `communication/sending-limits.md` |
| メッセージ, send_message, 送信, 返信, スレッド, inbox | `reference/communication/messaging-guide.md` |
| 指示, 委任, タスク依頼, デリゲーション | `reference/communication/instruction-patterns.md` |
| 報告, 日報, サマリー, 完了報告, エスカレーション | `reference/communication/reporting-guide.md` |
| Slack, ボットトークン, SLACK_BOT_TOKEN, not_in_channel | `reference/communication/slack-bot-token-guide.md` |
| 階層, 通信経路, org_dashboard, ping_subordinate | `organization/hierarchy-rules.md` |
| delegate_task, タスク委譲, task_tracker | `organization/hierarchy-rules.md`, `reference/operations/task-management.md` |
| 役割, 責任, speciality, 専門 | `reference/organization/roles.md` |
| 組織, supervisor, 上司, 部下, 同僚 | `reference/organization/structure.md` |
| タスクボード, ダッシュボード, 人間向け | `operations/task-board-guide.md` |
| バックグラウンド, submit, 長時間ツール | `operations/background-tasks.md` |
| タスク, current_task, pending, 進捗, 優先順位 | `reference/operations/task-management.md` |
| add_task, タスクキュー, plan_tasks, TaskExec | `reference/operations/task-management.md` |
| ハートビート, heartbeat, 定期チェック | `reference/operations/heartbeat-cron-guide.md` |
| cron, スケジュール, 定時タスク | `reference/operations/heartbeat-cron-guide.md` |
| ツール, animaworks-tool, MCP, mcp__aw__, skill | `reference/operations/tool-usage-overview.md` |
| 実行モード, S-mode, A-mode, B-mode, C-mode | `reference/operations/tool-usage-overview.md` |
| 設定, config, status.json, SSoT, reload | `reference/operations/project-setup.md` |
| モデル, models.json, credential, set-model, コンテキストウィンドウ | `reference/operations/model-guide.md` |
| background_model, バックグラウンドモデル, コスト最適化 | `reference/operations/model-guide.md` |
| Mode S, 認証, API直接, Bedrock, Vertex AI, Max plan | `reference/operations/mode-s-auth-guide.md` |
| 音声, voice, STT, TTS, VOICEVOX, ElevenLabs | `reference/operations/voice-chat-guide.md` |
| WebSocket, /ws/voice, barge-in, VAD, PTT | `reference/operations/voice-chat-guide.md` |
| Anima, 自分, 構成, 設計, ライフサイクル | `anatomy/what-is-anima.md` |
| 記憶, memory, episodes, knowledge, procedures | `reference/anatomy/memory-system.md` |
| Priming, RAG, Consolidation, Forgetting, 忘却 | `reference/anatomy/memory-system.md` |
| search_memory, write_memory_file, 記憶検索 | `reference/anatomy/memory-system.md` |
| identity, injection, 人格, 行動指針, 不変, 可変 | `reference/anatomy/anima-anatomy.md` |
| permissions.md, bootstrap, heartbeat.md, cron.md | `reference/anatomy/anima-anatomy.md` |
| プロンプトインジェクション, trust, untrusted, 境界タグ | `security/prompt-injection-awareness.md` |
| エラー, 問題, 動かない, 権限, ブロックコマンド | `reference/troubleshooting/common-issues.md` |
| フローチャート, 判断, 迷い, 緊急, セキュリティ | `reference/troubleshooting/escalation-flowchart.md` |
| Gmail, token.json, OAuth, pickle | `reference/troubleshooting/gmail-credential-setup.md` |
| ティア, tiered, T1, T2, T3, T4 | `reference/troubleshooting/common-issues.md` |
| ユースケース, 活用例, 何ができる | `reference/usecases/usecase-overview.md` |

---

## 使い方

```
# キーワードで検索
search_memory(query="メッセージ 送信", scope="common_knowledge")

# パスを直接指定
read_memory_file(path="common_knowledge/communication/board-guide.md")

# 技術リファレンスを参照
read_memory_file(path="reference/anatomy/anima-anatomy.md")

# このファイル自体を参照
read_memory_file(path="common_knowledge/00_index.md")
```
