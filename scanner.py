import os
import sys

internal_tokens = []
token=None

def add_internal_token(token):
    internal_tokens.append(token)


# 先読み関数
def get_token(lst):
    if not lst:
        return None

    next_element = lst[0]
    del lst[0]
    return next_element


# グローバル変数に格納する関数
def get_next_token():
    global token
    token = get_token(internal_tokens)


def get_current_token():
    return token


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


# "プログラム"=>“識別子”, “var”, “read”, “print”, “println”, “repeat”
def first_program():
    valid_numbers = {1, 2, 3, 4, 5, 7}
    return token in valid_numbers



# "解釈単位"=>“識別子”, “var”, “read”, “print”, “println”, “repeat”
def first_interpretation_unit():
    valid_numbers = {1, 2, 3, 4, 5, 7}
    return token in valid_numbers

# "変数代入"=>“識別子”
def first_variable_assignment():
    valid_numbers = {1}
    return token in valid_numbers

# "変数名"=>"識別子"
def first_parse_variable_name():
    valid_numbers = {1}
    return token in valid_numbers

# "式"=>“+”, “-”, “(”, “整数”, “実数”, “識別子”, “@”
def first_parse_expression():
    valid_numbers = {12,13,17,9,10,1,21}
    return token in valid_numbers

# "項"=>“(”, “整数”, “実数”, “識別子”, “@”
def first_term():
    valid_numbers = {17,9,10,1,21}
    return token in valid_numbers

# "因子"=>“(”, “整数”, “実数”, “識別子”, “@”
def first_factor():
    valid_numbers = {17,9,10,1,21}
    return token in valid_numbers

# "変数宣言"=>“var”
def first_variable_declaration():
    valid_numbers = {2}
    return token in valid_numbers
    
# "変数入力"=>“read”
def first_input_statement():
    valid_numbers = {3}
    return token in valid_numbers


# "出力指定"=>"print","println"
def first_output_specification():
    valid_numbers = {4,5}
    return token in valid_numbers


# "出力単位"=>“文字列”, “+”, “-”, “(”, “整数”, “実数”, “識別子”, “@”
def first_output_unit():
    valid_numbers = {11,12,13,17,9,10,1,21}
    return token in valid_numbers

# “repeat文”=>"repeat"
def first_repeat_statement():
    valid_numbers = {7}
    return token in valid_numbers


# "関数呼出"=>"@"
def first_function_call():
    valid_numbers = {21}
    return token in valid_numbers

# "関数名"=>"識別子"
def first_function_name():
    valid_numbers = {1}
    return token in valid_numbers





# <プログラム> → {<解釈単位>“;”}
def program():
    # 最初のトークンを取得
    get_next_token()
    if first_program():
        # First集合に含まれるならば
        while first_interpretation_unit():
            # <解釈単位>
            interpretation_unit()
            # ';'
            if get_current_token() == 19 :
                get_next_token()
            else:
                print("エラー:';'がありません")
                sys.exit(1)
        print("構文は正しいです")       
    else:
        print("エラー:'解釈単位'がありません")
        sys.exit(1)


# <解釈単位> → <変数代入> | <変数宣言> | <変数入力> | <出力指定> | <repeat 文>
def interpretation_unit():
    # 変数宣言
    if first_variable_declaration():
        variable_declaration()
    else:
        print("エラー:'var'がありません")
        sys.exit(1)

        

    # 変数入力

    # 出力指定

    # repeat文


# # <変数代入>
# def variable_assignment():

# <変数名>
def parse_variable_name():
    if token == 1:
        get_next_token()
        

# # <式>
# def parse_expression():

# # <項>
# def term():

# # <因子>
# def factor():


# <変数宣言> → “var” <変数名> [“:=” <式>]
def variable_declaration():
    if get_current_token() == 2:
        get_next_token()
        if first_parse_variable_name():
            parse_variable_name()
            # まだ未実装
        else:
            print("エラー:'変数名'がありません")
            sys.exit(1)



# # <変数入力>
# def input_statement():

# # <出力指定>
# def output_specification():

# # <出力単位の並び>
# def output_sequence():

# # <出力単位>
# def output_unit():

# # <repeat文>
# def repeat_statement():

# # <関数呼出>
# def function_call():

# # <関数名>
# def function_name():

# # <式の並び>
# def expression_sequence():







if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("使用法: python scanner.py <ファイル名>")
    #     sys.exit(1)

    # 現在のスクリプトのディレクトリを取得
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # ファイルのパスを作成
    file_path = os.path.join(current_directory, "test.m")


    # file_path = sys.argv[1]
    process_file(file_path)

    #構文解析
    program()

