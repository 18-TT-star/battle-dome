# Battle Dome (Windows 向け配布ガイド)

## 1. 同梱ファイル
- battle_dome.py
- requirements.txt (現在: colorama==0.4.6)
- windows_dist/install_and_run.bat (セットアップ & 実行)

## 2. 遊び方 (最短)
1. ZIP を解凍
2. `windows_dist` フォルダ内の `install_and_run.bat` をダブルクリック
3. 黒いウィンドウに従って待つとゲームが起動

## 3. うまく動かない時
| 症状 | 対処 |
|------|------|
| Python がないと怒られる | https://www.python.org/ から最新版 (3.10+ 推奨) をインストール。インストール時に "Add to PATH" をチェック |
| 画面が一瞬で閉じる | `cmd.exe` を手で開いてフォルダへ cd、`windows_dist\install_and_run.bat` 実行してエラー表示を確認 |
| 文字化け | Windows Terminal や PowerShell を使用 / フォントを等幅日本語対応へ |
| colorama が無いと言われる | `pip install -r requirements.txt` を手動で実行 |

## 4. 手動セットアップ手順 (バッチを使わない場合)
```
python -m venv .venv_win
.venv_win\Scripts\activate
pip install -r requirements.txt
python battle_dome.py
```

## 5. PyInstaller で単一 exe にしたい場合 (開発者向け)
```
pip install pyinstaller
pyinstaller --onefile --name BattleDome --icon icon.ico battle_dome.py
```
`dist/BattleDome.exe` が生成されます。colorama はバンドルされるので配布先へ Python 不要になります。

## 6. ライセンス / 注意
- 本フォルダ内スクリプトは学習用サンプルです。
- colorama ライセンスは MIT: https://github.com/tartley/colorama

楽しんでください！
