import random
import time
import os
from colorama import init, Fore, Style

# colorama 初期化
init()

# === ヘルパー関数 ===
def clear():
    os.system("clear")

def draw_bar(current, max_value, bar_length=10):
    filled = int((current / max_value) * bar_length)
    empty = bar_length - filled
    return "[" + "■" * filled + " " * empty + "]"

def draw_bar_with_blink(old_hp, new_hp, max_value, bar_length=10):
    """HPが減った部分だけ点滅"""
    old_filled = int((old_hp / max_value) * bar_length)
    new_filled = int((new_hp / max_value) * bar_length)
    blink_length = old_filled - new_filled
    for _ in range(2):
        bar = "[" + "■" * new_filled + Fore.RED + "■" * blink_length + Style.RESET_ALL + " " * (bar_length - old_filled) + "]"
        print(bar, end="\r")
        time.sleep(0.2)
        bar = "[" + "■" * new_filled + " " * blink_length + " " * (bar_length - old_filled) + "]"
        print(bar, end="\r")
        time.sleep(0.2)
    print(draw_bar(new_hp, max_value))  # 最終バー表示

def gauge_display(gauge, max_gauge=3):
    return f"{'★' * gauge}{' ' * (max_gauge - gauge)} ({gauge}/{max_gauge})"


# === メインループ・リトライ・メニュー機能 ===
def start_menu():
    print(Fore.CYAN + "=== 三すくみバトル！ ===" + Style.RESET_ALL)
    print("モードを選んでください：")
    print("1: CPU対戦")
    print("2: 二人対戦")
    while True:
        mode = input("番号で入力 > ")
        if mode in ["1", "2"]:
            break
        print("1か2で入力してください")
    is_two_player = (mode == "2")
    # 名前入力
    if is_two_player:
        player1_name = input("プレイヤー1の名前（赤）を入力してください > ").strip() or "プレイヤー1"
        player2_name = input("プレイヤー2の名前（青）を入力してください > ").strip() or "プレイヤー2"
        level = None
    else:
        player1_name = input("あなたの名前を入力してください > ").strip() or "あなた"
        player2_name = "CPU"
        print("\n難易度を選んでください：")
        print("1: かんたん（敵HP 5）")
        print("2: ふつう（敵HP 10）")
        print("3: むずかしい（敵HP 15）")
        while True:
            level = input("番号で入力 > ")
            if level in ["1", "2", "3"]:
                break
            print("1〜3で入力してください")
    return is_two_player, player1_name, player2_name, level

def get_enemy_hp_max_and_chance(is_two_player, level):
    if not is_two_player:
        enemy_hp_max = 5 if level == "1" else 15 if level == "3" else 10
        cpu_special_chance = 0.2 if level == "1" else 0.7 if level == "3" else 0.4
    else:
        enemy_hp_max = 10
        cpu_special_chance = 0.0
    return enemy_hp_max, cpu_special_chance

def battle(is_two_player, player1_name, player2_name, level):
    enemy_hp_max, cpu_special_chance = get_enemy_hp_max_and_chance(is_two_player, level)
    player_hp = 10
    enemy_hp = enemy_hp_max
    player_gauge = 0
    enemy_gauge = 0
    commands = ["攻撃", "防御", "溜め", "必殺(必要ゲージ: 2★)"]

    while player_hp > 0 and enemy_hp > 0:
        print(Fore.YELLOW + f"\n--- 現在のステータス ---" + Style.RESET_ALL)
        print(f"{Fore.RED}{player1_name}{Style.RESET_ALL} HP: {Fore.GREEN}{draw_bar(player_hp, 10)} {player_hp}/10{Style.RESET_ALL}  ゲージ: {gauge_display(player_gauge)}")
        print(f"{Fore.BLUE}{player2_name}{Style.RESET_ALL} HP: {Fore.RED}{draw_bar(enemy_hp, enemy_hp_max)} {enemy_hp}/{enemy_hp_max}{Style.RESET_ALL}  ゲージ: {gauge_display(enemy_gauge)}")

        # === プレイヤー1の入力 ===
        print(f"\n{Fore.RED}{player1_name}{Style.RESET_ALL} の番です。コマンドを選んでください:")
        for i, cmd in enumerate(commands):
            print(f"{i}: {cmd}")

        while True:
            try:
                player_input = int(input("> "))
                if player_input not in [0, 1, 2, 3]:
                    print("※0〜3の番号で入力してください！")
                elif player_input == 3 and player_gauge < 2:
                    print("※ゲージが足りません！")
                else:
                    break
            except:
                print("無効な入力です")

        clear()

        # === プレイヤー2またはCPUの入力 ===
        if is_two_player:
            while True:
                try:
                    print(f"{Fore.BLUE}{player2_name}{Style.RESET_ALL} の番 （他の人は見ないで）")
                    for i, cmd in enumerate(commands):
                        print(f"{i}: {cmd}")
                    enemy_input = int(input("> "))
                    if enemy_input not in [0, 1, 2, 3]:
                        print("※0〜3で入力してください！")
                    elif enemy_input == 3 and enemy_gauge < 2:
                        print("※ゲージが足りません！")
                    else:
                        break
                except:
                    print("無効な入力です")
            clear()
            print("\n選択完了。3秒後に発表！")
            time.sleep(3)
        else:
            if enemy_gauge >= 2 and random.random() < cpu_special_chance:
                enemy_input = 3
            else:
                enemy_input = random.randint(0, 2)

        # === 行動結果表示 ===
        print(Fore.MAGENTA + f"{player1_name} の行動: {commands[player_input]}" + Style.RESET_ALL)
        print(Fore.CYAN + f"{player2_name} の行動: {commands[enemy_input]}" + Style.RESET_ALL)

        old_player_hp = player_hp
        old_enemy_hp = enemy_hp

        # === 行動処理 ===
        if player_input == 3 and enemy_input == 3:
            player_gauge -= 2
            enemy_gauge -= 2
            print(Fore.YELLOW + "必殺技同士がぶつかって相殺された！" + Style.RESET_ALL)
        elif player_input == 3:
            player_gauge -= 2
            if enemy_input == 1:
                print(f"{player2_name} が防御！必殺は無効化された！")
            else:
                enemy_hp -= 10
                # 派手な必殺技エフェクト
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT)
                print("\n" + "="*40)
                print(Fore.RED + "★ 必殺技発動！！ ★" + Style.RESET_ALL)
                print(Fore.RED + Style.BRIGHT)
                for i in range(3):
                    print("    " + Fore.YELLOW + "BOOM!! " * 3 + Fore.RED + "BOOM!! " * 2 + Style.RESET_ALL)
                print(Fore.YELLOW + Style.BRIGHT + "\n         B O O M !!\n" + Style.RESET_ALL)
                for i in range(2):
                    print(Fore.RED + "    BOOM!! " * 4 + Style.RESET_ALL)
                print(Fore.YELLOW + Style.BRIGHT + "\n         B O O M !!\n" + Style.RESET_ALL)
                print(Fore.LIGHTYELLOW_EX + """
  ド派手なエネルギーが炸裂！！
  {0} に10ダメージ！！
                """.format(player2_name) + Style.RESET_ALL)
                print("="*40 + "\n")
                print(Fore.RED + f"必殺技ヒット！！{player2_name} に10ダメージ！！" + Style.RESET_ALL)
        elif enemy_input == 3:
            enemy_gauge -= 2
            if player_input == 1:
                print(f"{player1_name} が防御！必殺を無効化！")
            else:
                player_hp -= 10
                # 派手な必殺技エフェクト（敵バージョン）
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT)
                print("\n" + "="*40)
                print(Fore.RED + f"★ {player2_name} の必殺技発動！！ ★" + Style.RESET_ALL)
                print(Fore.RED + Style.BRIGHT)
                for i in range(3):
                    print("    " + Fore.YELLOW + "BOOM!! " * 3 + Fore.RED + "BOOM!! " * 2 + Style.RESET_ALL)
                print(Fore.YELLOW + Style.BRIGHT + "\n         B O O M !!\n" + Style.RESET_ALL)
                for i in range(2):
                    print(Fore.RED + "    BOOM!! " * 4 + Style.RESET_ALL)
                print(Fore.YELLOW + Style.BRIGHT + "\n         B O O M !!\n" + Style.RESET_ALL)
                print(Fore.LIGHTYELLOW_EX + f"""
  ド派手なエネルギーが炸裂！！
  {player1_name} に10ダメージ！！
                """ + Style.RESET_ALL)
                print("="*40 + "\n")
                print(Fore.RED + f"{player2_name} の必殺技が命中！！10ダメージ！！" + Style.RESET_ALL)
        else:
            if player_input == 0 and enemy_input == 2:
                enemy_hp -= 1
                print(f"{player1_name} の攻撃がヒット！{player2_name} に1ダメージ！")
            elif player_input == 2 and enemy_input == 0:
                player_hp -= 1
                print(f"{player2_name} の攻撃がヒット！{player1_name} は1ダメージ！")
            elif player_input == 1 and enemy_input == 0:
                print(f"{player1_name} が攻撃を防いだ！")
            elif player_input == 0 and enemy_input == 1:
                print(f"{player2_name} が攻撃を防いだ！")
            elif player_input == 2 and enemy_input == 1:
                player_gauge += 1
                print(f"{player1_name} は溜め成功！ゲージ+1！")
            elif player_input == 1 and enemy_input == 2:
                enemy_gauge += 1
                print(f"{player2_name} は溜め成功！ゲージ+1！")
            elif player_input == 2 and enemy_input == 2:
                player_gauge += 1
                enemy_gauge += 1
                print("両者溜めた！ゲージ+1ずつ！")
            elif player_input == 0 and enemy_input == 0:
                player_hp -= 1
                enemy_hp -= 1
                print("両者攻撃！お互いに1ダメージ！")
            elif player_input == 1 and enemy_input == 1:
                print("両者防御…静寂のターン。")

        # HPバー点滅（結果は消さない）
        if player_hp < old_player_hp:
            print(f"{Fore.RED}{player1_name}{Style.RESET_ALL} HPバー:")
            draw_bar_with_blink(old_player_hp, player_hp, 10)
        if enemy_hp < old_enemy_hp:
            print(f"{Fore.BLUE}{player2_name}{Style.RESET_ALL} HPバー:")
            draw_bar_with_blink(old_enemy_hp, enemy_hp, enemy_hp_max)

        time.sleep(1.5)

    # === 結果発表 ===
    print("\n" + Fore.CYAN + "=== バトル終了！ ===" + Style.RESET_ALL)
    if player_hp <= 0 and enemy_hp <= 0:
        print("相打ち！お互いに倒れた！")
    elif player_hp <= 0:
        print(f"{player1_name} の敗北……")
    else:
        print(f"{player1_name} の勝利だ！！")

def main():
    while True:
        is_two_player, player1_name, player2_name, level = start_menu()
        while True:
            battle(is_two_player, player1_name, player2_name, level)
            print("\nリトライ(r)、メニュー(m)、終了(q) > ", end="")
            choice = input().strip().lower()
            if choice == "r":
                # 名前や難易度を保持してリトライ
                continue
            elif choice == "m":
                clear()
                break
            elif choice == "q":
                print("また遊んでね！")
                return
            else:
                print("r/m/q で入力してください")

if __name__ == "__main__":
    main()
