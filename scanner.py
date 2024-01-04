import os
import sys

#行番号
line_number=1

#行番号を格納する配列
line_number_list=[-1]

#意味解析のための識別子と整数を確保する配列
semantic_analysis_list=[]
#意味解析用
token_value=None

# インタプリンタのための配列
interpreter_list=[]


internal_tokens = []
token=None


def add_internal_token(token):
    global line_number
    global line_number_list
    global token_value
    internal_tokens.append(token)
    # line_numberを記憶
    line_number_list.append(line_number)
    #意味解析に使用
    interpreter_list.append(token_value)


# 先読み関数
def get_token(lst):
    if not lst:
        return None

    next_element = lst[0]
    del lst[0]
    return next_element

# line_numberを取得
def get_line_number(lst):
    if not lst:
        return None
    
    next_element=lst[0]
    del lst[0]
    return next_element


# グローバル変数に格納する関数
def get_next_token():
    global token
    token = get_token(internal_tokens)
    global line_number
    line_number=get_line_number(line_number_list)



def get_current_token():
    return token
    

    


def process_file(file_path):
    global line_number 
    global token_value
    with open(file_path, "r", encoding="utf-8") as file:
        current_char = file.read(1)  # 最初の文字を読み込む

        while current_char:
            token_value=None #意味解析用
            if current_char.isspace():
                if current_char=='\n':
                    line_number+=1
                current_char = file.read(1)  # 空白文字の場合はスキップ
            elif current_char == '#':
                while current_char and current_char != '\n':
                    if current_char=='\n':
                        line_number+=1
                    current_char = file.read(1)
            elif current_char == '"':
                current_char = file.read(1)  # 次の文字を読み込む

                # ダブルクォートで囲まれた文字列を保存する変数
                string_value = ""

                # 次のダブルクォートが見つかるまでスキップ
                while current_char and current_char != '"':
                    string_value += current_char
                    current_char = file.read(1)

                if current_char == '"':
                    current_char = file.read(1)  # 次の文字を読み込む
                    add_internal_token(11)

                else:
                    print("エラー " + str(line_number) + "行目: 2つ目のダブルクォートが閉じられていません")
                    sys.exit(1)

            elif current_char == ':':
                current_char = file.read(1)  # 次の文字を読み込む

                if current_char == '=':
                    current_char = file.read(1)  # 次の文字を読み込む
                    add_internal_token(22)
                else:
                    print("エラー "+str(line_number)+"行目: ':' の後に '=' がありません")
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
                        print("エラー "+str(line_number)+"行目: 小数点が2つ以上か末尾に含まれています") 
                        sys.exit(1)
                    else:
                        print(token_value)
                        add_internal_token(10)  # token_valueに.を含む場合は10
                else:
                    print(token_value)
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
                    print(token_value)
                    add_internal_token(1)

            else:
                print("エラー "+str(line_number)+"行目:文法が間違っています")
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


# 非終端記号を呼ぶ前に先読み

# エラー回復が1回でも起こった場合は構文が正しいを表示しない
error_recovery_flag=False

# エラーリカバリ関数
def error_recovery(expected_tokens):
    global error_recovery_flag
    error_recovery_flag=True
    # 予測されるトークンセットに含まれている限りトークンを進める
    while get_current_token() not in expected_tokens and get_current_token() is not None:
        get_next_token()
    get_next_token()





# <プログラム> → {<解釈単位>“;”}
def program():
    # 最初のトークンを取得
    get_next_token()
    if first_program():
        while first_interpretation_unit():
            # 解釈単位
            interpretation_unit()
            # ';'
            if get_current_token() == 19 :
                get_next_token()
            else:
                print("line:"+str(line_number)+" SyntaxError:';'がありません")
                error_recovery([19])
        
        # エラー回復が1回でも起こった場合は表示しない
        if not error_recovery_flag:
            print("構文は正しいです")       
    elif get_current_token() is None:
            print("構文は正しいです")       
    else:
        print("line:"+str(line_number)+" SyntaxError:'<プログラム>'が間違っています")
        sys.exit(1)



# <解釈単位> → <変数代入> | <変数宣言> | <変数入力> | <出力指定> | <repeat 文>
def interpretation_unit():
    if first_variable_assignment():
        # 変数代入
        variable_assignment()
    elif first_variable_declaration():
        # 変数宣言 
        variable_declaration()
        
    elif first_input_statement():
        # 変数入力
        input_statement()

    elif first_output_specification():
        # 出力指定
        output_specification()
    
    elif first_repeat_statement():
        # repeat文
        repeat_statement()
    else:
        print("line:"+str(line_number)+" SyntaxError:'<解釈単位>'が間違っています")
        error_recovery([19])
        



# <変数代入> → <変数名> “:=” <式>
def variable_assignment():
    if first_parse_variable_name():
        # 変数名
        parse_variable_name()
        # ':='
        if get_current_token() == 22:
            get_next_token()
            if first_parse_expression():
                # 式
                parse_expression()
            else:
                print("line:"+str(line_number)+" SyntaxError:'=:'の後に'<式>'がありません")
                error_recovery([19])
                
        else:
            print("line:"+str(line_number)+" SyntaxError:':='がありません")
            error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'<変数名>'が間違っています")
        error_recovery([19])


# <変数名> → “識別子”
def parse_variable_name():
    # '識別子'
    if get_current_token() == 1:
        get_next_token()
        

# <式> → [“+” | “-”] <項> {“+” <項> | “-” <項> }
def parse_expression():
    # '+'
    if get_current_token() == 12:     
        get_next_token()
    # '-'
    elif get_current_token() == 13:
        get_next_token()
    if first_term():
        # 項
        term()
        # '+' or '-'
        while get_current_token()in(12,13):
            get_next_token()
            if first_term():
                # 項
                term()
            else:
                print("line:"+str(line_number)+" SyntaxError:'+'の後に'<項>'がありません")                                                
                error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'<項>'が間違っています")                                                        
        error_recovery([19])




# <項> → <因子> {“*” <因子> | “/” <因子> | “div” <因子> | “%” <因子>}
def term():
    if first_factor():
        # 因子
        factor()
        # '*' or '/' or 'div' or '%'
        while get_current_token() in (14,15,6,16):
            get_next_token()
            if first_factor():
                # 因子
                factor()
            else:
                print("line:"+str(line_number)+" SyntaxError:'演算子'の後に'<因子>'がありません")                                                        
                error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'<因子>'が間違っています")                                                                
        error_recovery([19])



#<因子> → “(” <式>“)” | “整数” | “実数” | <変数名> | <関数呼出>
def factor():
    # '('
    if get_current_token()==17:
        get_next_token()
        if first_parse_expression():
            # 式
            parse_expression()
            # ')'
            if get_current_token()==18:
                get_next_token()
            else:
                print("line:"+str(line_number)+" SyntaxError:')'がありません")     
                error_recovery([19])
        else:
            print("line:"+str(line_number)+" SyntaxError:'('の後に'<式>'がありません")     
            error_recovery([19])
    # '整数'
    elif get_current_token()==9:
        get_next_token()
    # '実数'
    elif get_current_token()==10:
        get_next_token()
    elif first_parse_variable_name():
        # 変数名
        parse_variable_name()
    elif first_function_call():
        # 関数呼出
        function_call()
    else:
        print("line:"+str(line_number)+" SyntaxError:'因子'が間違っています")     
        error_recovery([19])



# <変数宣言> → “var” <変数名> [“:=” <式>]
def variable_declaration():
    #'var'
    if get_current_token() == 2:
        get_next_token()
        if first_parse_variable_name():
            # 変数名
            parse_variable_name()
            # ':='
            if get_current_token()==22:
                get_next_token()
                if first_parse_expression():
                    # 式
                    parse_expression()
                else:
                    print("line:"+str(line_number)+" SyntaxError:':='の後に'式'がありません") 
                    error_recovery([19])
        else:
            print("line:"+str(line_number)+" SyntaxError:'変数名'がありません") 
            error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'var'がありません") 
        error_recovery([19])

# <変数入力> → “read” “(” <変数名> “)”
def input_statement():
    # 'read'
    if get_current_token()==3:
        get_next_token()
        # '('
        if get_current_token()==17:
            get_next_token()
            if first_parse_variable_name():
                # 変数名
                parse_variable_name()
                # ')'
                if get_current_token()==18:
                    get_next_token()
                else:
                    print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                    error_recovery([19])
                    
            else:
                print("line:"+str(line_number)+" SyntaxError:'変数名'がありません")                 
                error_recovery([19])
                
        else:
            print("line:"+str(line_number)+" SyntaxError:'('がありません") 
            error_recovery([19])
            
    else:
        print("line:"+str(line_number)+" SyntaxError:'read'がありません") 
        error_recovery([19])
        

# <出力指定> → “print” “(”<出力単位の並び> “)” | “println” “(”<出力単位の並び> “)”
def output_specification():
    # 'print'
    if get_current_token()==4:
        get_next_token()
        # '('
        if get_current_token() == 17:
            get_next_token()
            # 出力単位の並び
            output_sequence()
            # ')'
            if get_current_token() == 18:
                get_next_token()
            else:
                print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                error_recovery([19])
        else:
            print("line:"+str(line_number)+" SyntaxError:'('がありません") 
            error_recovery([19])
    # 'println'
    elif get_current_token()==5:
        get_next_token()
        # '('
        if get_current_token() == 17:
            get_next_token()
            # 出力単位の並び
            output_sequence()
            # ')'
            if get_current_token() == 18:
                get_next_token()
            else:
                print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                error_recovery([19])
        else:
            print("line:"+str(line_number)+" SyntaxError:')'がありません")             
            error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'出力指定'が間違っています") 
        error_recovery([19])


# <出力単位の並び> → ε | <出力単位> {“,” <出力単位>}
def output_sequence():
    if first_output_unit():
        # 出力単位
        output_unit()
        # ','
    while get_current_token()==20:
        get_next_token()
        if first_output_unit():
            # 出力単位
            output_unit()
        else:
            print("line:"+str(line_number)+" SyntaxError:'出力単位'が間違っています") 
            error_recovery([19])
    

# <出力単位> → <式> | “文字列”
def output_unit():
    if first_parse_expression():
        # 式        
        parse_expression()
        #'文字列'
    elif get_current_token() == 11:
        get_next_token()
    else:
        print("line:"+str(line_number)+" SyntaxError:'出力単位'が間違っています") 
        error_recovery([19])



# <repeat 文> → “repeat” <式> <変数代入>
def repeat_statement():
    # 'repeat'
    if get_current_token()==7:
        get_next_token()
        if first_parse_expression():
            # 式
            parse_expression()
            if first_variable_assignment():
                # 変数代入
                variable_assignment()
            else:
                print("line:"+str(line_number)+" SyntaxError:'変数代入'が間違っています") 
                error_recovery([19])
        else:            
            print("line:"+str(line_number)+" SyntaxError:'式'が間違っています")             
            error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'repeat'がありません") 
        error_recovery([19])
        

#<関数呼出> → “@” <関数名> “(” <式の並び> “)”
def function_call():
    # '@'
    if get_current_token() == 21:
        get_next_token()
        if first_function_name():
            # 関数名
            function_name()
            # '('
            if get_current_token()==17:
                get_next_token()
                # 式の並び
                expression_sequence()
                # ')'
                if get_current_token()==18:
                    get_next_token()
                else:
                    print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                    error_recovery([19])
            else:
                print("line:"+str(line_number)+" SyntaxError:'('がありません") 
                error_recovery([19])
        else:
            print("line:"+str(line_number)+" SyntaxError:'関数名'が間違っています") 
            error_recovery([19])
    else:
        print("line:"+str(line_number)+" SyntaxError:'@'がありません") 
        error_recovery([19])



#<関数名> → “識別子”
def function_name():
    # '識別子'
    if get_current_token() == 1:
        get_next_token()


# <式の並び> → ε | <式> {“,” <式>}
def expression_sequence():
    if first_parse_expression():
        # 式
        parse_expression()
        # ','
        while get_current_token()==20:
            get_next_token()
            if first_parse_expression():
                # 式
                parse_expression()
            else:
                print("line:"+str(line_number)+" SyntaxError:','の後に'式'がありません") 
                error_recovery([19])
        #式だけでも良い
    

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

    print(interpreter_list)

    #構文解析
    program()

