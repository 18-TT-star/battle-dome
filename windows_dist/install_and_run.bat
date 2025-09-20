@echo off
REM ==============================================
REM Battle Dome セットアップ & 実行スクリプト (Windows)
REM 1) 仮想環境 .venv_win を作成
REM 2) requirements.txt をインストール
REM 3) ゲームを起動
REM ==============================================

setlocal ENABLEDELAYEDEXPANSION

REM スクリプトのあるディレクトリへ移動
cd /d "%~dp0.."

IF NOT EXIST requirements.txt (
  echo requirements.txt が見つかりません。中断します。
  pause
  exit /b 1
)

REM Python 存在チェック
python --version >NUL 2>&1
IF ERRORLEVEL 1 (
  echo Python が見つかりません。https://www.python.org/ からインストールしてください。
  pause
  exit /b 1
)

IF NOT EXIST .venv_win (
  echo [1/3] 仮想環境を作成中...
  python -m venv .venv_win
)

CALL .venv_win\Scripts\activate.bat

python -m pip install --upgrade pip >NUL

echo [2/3] 依存関係をインストール中...
pip install -r requirements.txt
IF ERRORLEVEL 1 (
  echo インストールに失敗しました。
  pause
  exit /b 1
)

echo [3/3] ゲームを起動します...
python battle_dome.py

echo.
echo 終了しました。もう一度遊ぶ場合は本ウィンドウを閉じずに python battle_dome.py と入力してもOKです。
pause
