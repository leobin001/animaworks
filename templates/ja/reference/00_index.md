# Reference — 技術リファレンス目次

AnimaWorks の詳細な技術仕様・管理者向け設定ガイドの一覧。
RAG 検索対象外。必要なときに `read_memory_file(path="reference/...")` で直接参照すること。

## 参照方法

```
read_memory_file(path="reference/00_index.md")          # この目次
read_memory_file(path="reference/anatomy/anima-anatomy.md")  # 例
```

## カテゴリ

### anatomy/ — 構成・アーキテクチャ

| ファイル | 内容 |
|---------|------|
| `anima-anatomy.md` | Anima構成ファイル完全ガイド（全ファイルの役割・変更ルール・カプセル化） |
| `memory-system.md` | 記憶システム詳細（記憶の種類・RAG・Priming・Consolidation・Forgetting） |

### communication/ — メッセージング・連携

| ファイル | 内容 |
|---------|------|
| `messaging-guide.md` | メッセージ送受信の完全リファレンス（send_message パラメータ、スレッド管理、1ラウンドルール） |
| `instruction-patterns.md` | 指示の出し方パターン集（明確な指示の書き方、委任パターン、進捗確認） |
| `reporting-guide.md` | 報告・エスカレーションの方法（報告タイミング、フォーマット、緊急 vs 定期） |
| `slack-bot-token-guide.md` | Slack ボットトークンの設定方法（Per-Anima vs 共有） |

### internals/ — フレームワーク内部仕様

| ファイル | 内容 |
|---------|------|
| `common-knowledge-access-paths.md` | common_knowledge の5つの参照経路とRAGインデックスの仕組み |

### operations/ — 管理・運用設定

| ファイル | 内容 |
|---------|------|
| `project-setup.md` | プロジェクト初期設定（`animaworks init`・ディレクトリ構成） |
| `task-management.md` | タスク管理リファレンス（add_task / update_task / plan_tasks / delegate_task の全パラメータ） |
| `heartbeat-cron-guide.md` | 定期実行の設定詳細（ハートビートの仕組み、cron構文、ホットリロード、自己更新） |
| `tool-usage-overview.md` | ツール使用リファレンス（S/A/B/Cモード別のツール体系、呼び出し方法） |
| `model-guide.md` | モデル選択・実行モード・コンテキストウィンドウの技術詳細 |
| `mode-s-auth-guide.md` | Mode S 認証モード設定（API/Bedrock/Vertex/Max） |
| `voice-chat-guide.md` | 音声チャットのアーキテクチャ・STT/TTS・インストール |

### organization/ — 組織構造

| ファイル | 内容 |
|---------|------|
| `structure.md` | 組織構造のデータソース・supervisor/speciality の解決方法 |
| `roles.md` | 役割と責任範囲（トップレベル / 中間管理 / 実行 Anima の責務） |

### troubleshooting/ — トラブルシューティング

| ファイル | 内容 |
|---------|------|
| `common-issues.md` | よくある問題と対処法（メッセージ不達、送信制限、権限、ツール、コンテキスト） |
| `escalation-flowchart.md` | 困ったときの判断フローチャート（問題分類、緊急度判定、エスカレーション先） |
| `gmail-credential-setup.md` | Gmail Tool OAuth認証設定の手順 |

### usecases/ — ユースケースガイド

| ファイル | 内容 |
|---------|------|
| `usecase-overview.md` | AnimaWorksで何ができるか・始め方・全テーマ一覧 |
| `usecase-communication.md` | コミュニケーション自動化（チャット・メール監視、エスカレーション、定期連絡） |
| `usecase-development.md` | ソフトウェア開発支援（コードレビュー、CI/CD監視、Issue実装、バグ調査） |
| `usecase-monitoring.md` | インフラ・サービス監視（死活監視、リソース監視、SSL証明書、ログ分析） |
| `usecase-secretary.md` | 秘書・事務サポート（スケジュール管理、連絡調整、日報作成、リマインダー） |
| `usecase-research.md` | 調査・リサーチ・分析（Web検索、競合分析、市場調査、レポート作成） |
| `usecase-knowledge.md` | ナレッジ管理・ドキュメント整備（手順書作成、FAQ構築、教訓の蓄積） |
| `usecase-customer-support.md` | カスタマーサポート（一次対応、FAQ自動回答、エスカレーション管理） |

## 関連

- 日常の実用ガイド → `common_knowledge/00_index.md`
- 共通スキル → `common_skills/`
