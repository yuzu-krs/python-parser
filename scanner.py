import os
import sys

internal_tokens = []

def add_internal_token(token):
    internal_tokens.append(token)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        current_char = file.read(1)  # 最初の文字を読み込む

        while current_char:
            if current_char.isspace():
                current_char = file.read(1)  # 空白文字の場合はスキップ
            elif current_char == '#':
                while current_char and current_char != '\n':
                    current_char = file.read(1)
            elif current_char == '"':
                current_char = file.read(1)  # 次の文字を読み込む

                # 次のダブルクォートが見つかるまでスキップ
                while current_char and current_char != '"':
                    current_char = file.read(1)

                if current_char == '"':
                    current_char = file.read(1)  # 次の文字を読み込む
                    add_internal_token(11)
                else:
                    print("エラー: 2つ目のダブルクォートが閉じられていません")
                    sys.exit(1)

            elif current_char == ':':
                current_char = file.read(1)  # 次の文字を読み込む

                if current_char == '=':
                    current_char = file.read(1)  # 次の文字を読み込む
                    add_internal_token(22)
                else:
                    print("エラー: ':' の後に '=' がありません")
                    sys.exit(1)

            elif current_char == '+':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(12)

            elif current_char == '-':
                current_char = file.read(1)  # 次の文字を読み込む                
                add_internal_token(13)

            elif current_char == '*':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(14)

            elif current_char == '/':
                current_char = file.read(1)  # 次の文字を読み込む                
                add_internal_token(15)

            elif current_char == '%':
                current_char = file.read(1)  # 次の文字を読み込む                
                add_internal_token(16)

            elif current_char == '(':
                current_char = file.read(1)  # 次の文字を読み込む                
                add_internal_token(17)

            elif current_char == ')':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(18)

            elif current_char == ';':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(19)

            elif current_char == ',':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(20)

            elif current_char == '@':
                current_char = file.read(1)  # 次の文字を読み込む
                add_internal_token(21)

            elif current_char.isdigit():  # 0~9の数字なら
                token_value = current_char
                dot_count = 0

                # 0~9の数字が来るか.が来るまで文字を消費
                while current_char := file.read(1):
                    if current_char.isdigit() or (current_char == '.' and dot_count < 2):
                        if current_char == '.':
                            dot_count += 1
                        token_value += current_char
                    else:
                        break

                if '.' in token_value:
                    if token_value.count('.') >= 2 or (token_value.count('.') == 1 and token_value.endswith('.')):
                        print("エラー: 小数点が2つ以上か末尾に含まれています")
                        sys.exit(1)
                    else:
                        add_internal_token(10)  # token_valueに.を含む場合は10
                else:
                    add_internal_token(9)  # token_valueに.を含まない場合は9

            elif current_char.isalpha() or current_char == '_':
                token_value = current_char

                # 2つ目以降はアルファベットorアンダーバーor数字が続く場合whileで文字列を保持
                while current_char := file.read(1):
                    if current_char.isalnum() or current_char == '_':
                        token_value += current_char
                    else:
                        break

                # 上記で保持した文字列が特定のキーワードの場合は対応する値を追加
                if token_value == 'var':
                    add_internal_token(2)
                elif token_value == 'read':
                    add_internal_token(3)
                elif token_value == 'print':
                    add_internal_token(4)
                elif token_value == 'println':
                    add_internal_token(5)
                elif token_value == 'div':
                    add_internal_token(6)
                elif token_value == 'repeat':
                    add_internal_token(7)
                else:
                    add_internal_token(1)

            else:
                print("エラー:文法が間違っています")
                sys.exit(1)

# 先読み関数
def lookahead(lst):
    if not lst:
        return None

    next_element = lst[0]
    del lst[0]
    return next_element







if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用法: python scanner.py <ファイル名>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_file(file_path)

    
    # 最後にinternal_tokensを表示
    print("Internal Tokens:", internal_tokens)