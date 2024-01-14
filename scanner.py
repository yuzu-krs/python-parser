import os
import sys
import math

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

#インタプリンタの際，文字列の行を決める配列
interpreter_line_number=[]

#インタプリンタの際，文字列の行を決める配列
def add_interpreter_line_number():
    global interpreter_line_number
    interpreter_line_number.append(line_number)

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

# 意味解析用リスト
def get_interpreter(lst):
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
    global token_value
    token_value=get_interpreter(interpreter_list)




def get_current_token():
    return token
    

    


def process_file(file_path):
    global line_number 
    global token_value
    with open(file_path, "r", encoding="utf-8") as file:
        current_char = file.read(1)  # 最初の文字を読み込む

        while current_char:
            token_value="" #意味解析用
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
                token_value = ""

                # 次のダブルクォートが見つかるまでスキップ
                while current_char and current_char != '"':
                    token_value += current_char
                    current_char = file.read(1)

                if current_char == '"':
                    current_char = file.read(1)  # 次の文字を読み込む
                    add_internal_token(11)
                    add_interpreter_line_number()

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
                    token_value=""
                    add_internal_token(2)
                elif token_value == 'read':
                    token_value=""
                    add_internal_token(3)
                elif token_value == 'print':
                    token_value=""
                    add_internal_token(4)
                elif token_value == 'println':
                    token_value=""
                    add_internal_token(5)
                elif token_value == 'div':
                    token_value=""
                    add_internal_token(6)
                elif token_value == 'repeat':
                    token_value=""
                    add_internal_token(7)
                else:
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


#####

#記号表

symbol_table = {}

# 登録
def add_variable_to_symbol_table(name, value):
    symbol_table[name] = value

# 探索
def find_variable_in_symbol_table(name):
    return symbol_table.get(name)

# 値の変更
def update_variable_in_symbol_table(name, new_value):
    if name in symbol_table:
        symbol_table[name] = new_value
        return True
    else:
        return False

#keyに対して値を返す
def get_value_from_symbol_table(key):
    return symbol_table.get(key)

# # 例として変数 x を登録
# add_variable_to_symbol_table('x', 10)

# シンボルテーブルの内容を表示
# print("初期のシンボルテーブル:", symbol_table)

# # 変数 y の値を探索
# found_value = find_variable_in_symbol_table('y')
# print("変数 y の値:", found_value)

# # 変数 x の値を更新
# success = update_variable_in_symbol_table('x', 30)
# if success:
#     print("変数 x の値を更新しました:", symbol_table)
# else:
#     print("変数 x が見つかりませんでした")

# # 存在しない変数 z の値を探索
# not_found_value = find_variable_in_symbol_table('z')
# print("変数 z の値:", not_found_value)

#####


# インタプリンタ計算を行う関数
# 平方根を求める関数
def sqrt(x):
    return math.sqrt(x)

# 二つの数のうち大きい方を求める関数(標準である)


# 二つの数のうち小さい方を求める関数(標準である)


# 正弦を求める関数
def sin(x):
    return math.sin(x)

# 余弦を求める関数
def cos(x):
    return math.cos(x)

# 正接を求める関数
def tan(x):
    return math.tan(x)





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
                sys.exit(1)
        
        # エラー回復が1回でも起こった場合は表示しない
        if not error_recovery_flag:
            print("\n---------------------------")
            print("意味的&構文的は正しいです")       
    elif get_current_token() is None:
        print("\n---------------------------")
        print("構文的&意味的は正しいです")       
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
        sys.exit(1)
        



# <変数代入> → <変数名> “:=” <式>
def variable_assignment():
    if first_parse_variable_name():
        tmp_token=token_value
        # 変数名
        parse_variable_name()
        # ':='
        if get_current_token() == 22:
            get_next_token()
            if first_parse_expression():
                # 式
                tmp_number=parse_expression()
                update_variable_in_symbol_table(tmp_token,tmp_number)
            else:
                print("line:"+str(line_number)+" SyntaxError:'=:'の後に'<式>'がありません")
                sys.exit(1)
                
        else:
            print("line:"+str(line_number)+" SyntaxError:':='がありません")
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" SyntaxError:'<変数名>'が間違っています")
        sys.exit(1)


# <変数名> → “識別子”
def parse_variable_name():
    # '識別子'
    if get_current_token() == 1: 
        
        # "識別子が記号表に登録済みでない"
        # "未定義の変数の参照によるエラー"
        if token_value not in symbol_table:
            print("line:"+str(line_number_list[1])+" NameError:'"+token_value+ "' は未定義の変数です") 
            sys.exit(1)

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
        result1=term() 
        # '+' or '-'
        while get_current_token()in(12,13):
            operator_type=0
            if get_current_token()==12:
                operator_type=1
            
            elif get_current_token()==13:
                operator_type=2

            

            get_next_token()
            if first_term():
                # 項
                result2=term()
            else:
                print("line:"+str(line_number)+" SyntaxError:'+'の後に'<項>'がありません")                                                
                sys.exit(1)
            
            if operator_type==1:
                
                result1 = round(float(result1),6) + round(float(result2),6)
            elif operator_type==2:
                result1 = round(float(result1),6) - round(float(result2),6)
        
        return result1
    else:
        print("line:"+str(line_number)+" SyntaxError:'<項>'が間違っています")                                                        
        sys.exit(1)



# <項> → <因子> {“*” <因子> | “/” <因子> | “div” <因子> | “%” <因子>}
def term():
    if first_factor():
        # 因子
        result1=factor() #因子の構文解析結果を保持
        # '*' or '/' or 'div' or '%'
        while get_current_token() in (14,15,6,16):
            operator_type=0
            # '*'
            if get_current_token()==14:
                operator_type=1
            # '/'
            elif get_current_token()==15:
                operator_type=2
            # 'div'
            elif get_current_token()==6:
                operator_type=3
            # '%'
            elif get_current_token()==16:
                operator_type=4
            
            get_next_token()
            if first_factor():
                # 因子
                result2=factor()
            else:
                print("line:"+str(line_number)+" SyntaxError:'演算子'の後に'<因子>'がありません")                                                        
                sys.exit(1)
            
            #演算を行う
            #'*'
            if operator_type==1:
                result1 = round(float(result1),6) * round(float(result2),6)
            #'/'
            elif operator_type==2:
                result1 = round(float(result1),6) / round(float(result2),6)                                
            #整数除算 'div'
            elif operator_type==3:
                result1 = round(float(result1),6) // round(float(result2),6)                                
            #'%'
            elif operator_type==4:
                result1 = round(float(result1),6) % round(float(result2),6)                                
            
        return result1
    else:
        print("line:"+str(line_number)+" SyntaxError:'<因子>'が間違っています")                                                                
        sys.exit(1)





#<因子> → “(” <式>“)” | “整数” | “実数” | <変数名> | <関数呼出>
def factor():
    # '('
    if get_current_token()==17:
        get_next_token()
        if first_parse_expression():
            # 式
            result1=parse_expression()
            # ')'
            if get_current_token()==18:
                get_next_token()
                return result1
            else:
                print("line:"+str(line_number)+" SyntaxError:')'がありません")     
                sys.exit(1)
        else:
            print("line:"+str(line_number)+" SyntaxError:'('の後に'<式>'がありません")     
            sys.exit(1)
    # '整数'
    elif get_current_token()==9:
        result1=token_value
        get_next_token()
        return float(result1)
    # '実数'
    elif get_current_token()==10:
        result1=token_value
        get_next_token()
        return float(result1)
    elif first_parse_variable_name():
        # 変数名
        result1=token_value
        parse_variable_name()
        #keyに対して値を更新(記号表)
        return get_value_from_symbol_table(result1)
    elif first_function_call():
        # 関数呼出
        result1=function_call()
        return result1
    else:
        print("line:"+str(line_number)+" SyntaxError:'因子'が間違っています")     
        sys.exit(1)


# <変数宣言> → “var” <変数名> [“:=” <式>]
def variable_declaration():
    #'var'
    if get_current_token() == 2:
        get_next_token()
        if first_parse_variable_name():
            # "識別子が記号表に登録済みか"
            if token_value in symbol_table:
                #登録済みである 変数が二重に定義されています
                print("line:"+str(line_number)+" DuplicateError: '"+token_value+"' は二重に定義されています") 
                sys.exit(1)
            else:
                # 識別子がまだ登録されていない
                symbol_table[token_value]=None 
            # 変数名
            tmp_token=token_value
            parse_variable_name()
            # ':='
            if get_current_token()==22:
                get_next_token()
                if first_parse_expression():
                    # 式
                    tmp_number=parse_expression()
                    update_variable_in_symbol_table(tmp_token,tmp_number)
                    
                else:
                    print("line:"+str(line_number)+" SyntaxError:':='の後に'式'がありません") 
                    sys.exit(1)
        else:
            print("line:"+str(line_number)+" SyntaxError:'変数名'がありません") 
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" SyntaxError:'var'がありません") 
        sys.exit(1)

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
                tmp_token=token_value 
                parse_variable_name()
                # ')'
                if get_current_token()==18:
                    tmp_input=input()
                    update_variable_in_symbol_table(tmp_token,tmp_input)
                    get_next_token()
                    
                else:
                    print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                    sys.exit(1)
                    
            else:
                print("line:"+str(line_number)+" SyntaxError:'変数名'がありません")                 
                sys.exit(1)
                
        else:
            print("line:"+str(line_number)+" SyntaxError:'('がありません") 
            sys.exit(1)
            
    else:
        print("line:"+str(line_number)+" SyntaxError:'read'がありません") 
        sys.exit(1)
        

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
                sys.exit(1)
        else:
            print("line:"+str(line_number)+" SyntaxError:'('がありません") 
            sys.exit(1)
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
                # printlnの場合改行
                print()
            else:
                print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                sys.exit(1)
        else:
            print("line:"+str(line_number)+" SyntaxError:')'がありません")             
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" SyntaxError:'出力指定'が間違っています") 
        sys.exit(1)


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
            sys.exit(1)
    




# <出力単位> → <式> | “文字列”
def output_unit():
    global tmp_line_number
    if first_parse_expression():
        # 式        
        #小数点以下6桁
        print(f"{float(parse_expression()):.6f}", end='')
        #'文字列'
    elif get_current_token() == 11:
        # 文字列を表示する際に，同じ行のprintは同じ行に表示するため
        # 現在の行と次の行が同じだった場合は改行なし，もしくは配列の最後ではない場合改行あり
        
        print(token_value,end='')
        
        get_line_number(interpreter_line_number)
        get_next_token()
    else:
        print("line:"+str(line_number)+" SyntaxError:'出力単位'が間違っています") 
        sys.exit(1)



# repeat回数が整数かどうか判定する
def is_repeat_integer(value):
    try:
        # floatに変換してから整数に変換し、元の値と比較することで小数点以下がないかを確認
        return int(float(value)) == float(value)
    except ValueError:
        # 浮動小数点数に変換できない場合は False を返す
        return False


# <repeat 文> → “repeat” <式> <変数代入>
def repeat_statement():
    # 'repeat'
    if get_current_token()==7:
        get_next_token()
        if first_parse_expression():
            # internal_tokensの;になるまでtmp_tokensに格納する
            tmp_tokens=[] #初期化
            # 記号表の更新のためにさらに配列を保持
            tmp_interpreter_list=[] # 初期化
            global interpreter_list

            # parse_expression()を通すと0番目のトークンを消費してコピーできなくなるためここでコピーしておく
            tmp_interpreter_list.append(interpreter_list[0])



            # 式
            repeat_count=parse_expression()  #リピート回数

            # リピート回数が整数か？
            if is_repeat_integer(repeat_count):
                repeat_count=int(repeat_count)
            else:
                print("line:"+str(line_number)+" RepeatError:'repeat'の後は整数です") 
                sys.exit(1)

            # internal_tokensの;になるまでtmp_tokensに格納する
            #';'
            while not get_current_token()==19:
                tmp_tokens.append(get_current_token())
                tmp_interpreter_list.append(interpreter_list[0])
                get_next_token()
            
            #上で;が消費しているため，C:=C+1この状態となっている,;を末尾に追加
            if get_current_token()==19:
                tmp_tokens.append(get_current_token())

            # リピートの回数に応じてトークンを増加させる
            for _ in range(repeat_count):
                global internal_tokens  # globalキーワードを追加
                internal_tokens = tmp_tokens + internal_tokens
                interpreter_list=tmp_interpreter_list+interpreter_list

            get_next_token()

            if first_variable_assignment():
                # 変数代入
                variable_assignment()
            else:
                print("line:"+str(line_number)+" SyntaxError:'変数代入'が間違っています") 
                sys.exit(1)
        else:            
            print("line:"+str(line_number)+" SyntaxError:'式'が間違っています")             
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" SyntaxError:'repeat'がありません") 
        sys.exit(1)
        


#<関数呼出> → “@” <関数名> “(” <式の並び> “)”
def function_call():
    # '@'
    if get_current_token() == 21:
        get_next_token()
        if first_function_name():

            # 関数名
            tmp=function_name()
            
            # '('
            if get_current_token()==17:
                get_next_token()
                # 式の並び argsに引数の個数を格納する(意味解析で使用)
                function_length,function_number1,function_number2=expression_sequence()
                # 関数の引数をチェック
                result=check_args(tmp,function_length,function_number1,function_number2)
                # ')'
                if get_current_token()==18:
                    get_next_token()
                    return result
                else:
                    print("line:"+str(line_number)+" SyntaxError:')'がありません") 
                    sys.exit(1)
            else:
                print("line:"+str(line_number)+" SyntaxError:'('がありません") 
                sys.exit(1)
        else:
            print("line:"+str(line_number)+" SyntaxError:'関数名'が間違っています") 
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" SyntaxError:'@'がありません") 
        sys.exit(1)


# 意味解析での関数名の引数チェック
# 関数名と関数の引数
def check_args(function_string,function_length,function_number1,function_number2):
    if function_string=="sqrt" :
        if function_length==1:
            function_number1=float(function_number1)
            return sqrt(function_number1)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[sqrt]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    elif function_string=="max" :
        if function_length==2:
            function_number1=float(function_number1)                
            function_number2=float(function_number2)
            return max(function_number1,function_number2)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[max]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    elif function_string=="min" :
        if function_length==2:
            function_number1=float(function_number1)                
            function_number2=float(function_number2)
            return min(function_number1,function_number2)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[min]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    elif function_string=="sin" :
        if function_length==1:
            function_number1=float(function_number1)
            return sin(function_number1)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[sin]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    elif function_string=="cos" :
        if function_length==1:
            function_number1=float(function_number1)
            return cos(function_number1)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[cos]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    elif function_string=="tan" :
        if function_length==1:
            function_number1=float(function_number1)
            return tan(function_number1)
        else:
            print("line:"+str(line_number)+" FunctionError:関数[tan]の引数の個数 '"+str(function_length)+"' が不適です") 
            sys.exit(1)
    else:
        print("line:"+str(line_number)+" FunctionError: "+str(function_string)+" そのような関数はありません") 
        sys.exit(1)




#<関数名> → “識別子”
def function_name():
    # '識別子'
    if get_current_token() == 1:
        tmp_function_name=token_value
        get_next_token()
        return tmp_function_name
        


# <式の並び> → ε | <式> {“,” <式>}
def expression_sequence():
    # 今回は引数
    #関数の第一引数
    function_number1=None
    #関数の第二引数
    function_number2=None
    
    # 引数の個数を返す
    arguments_count=0
    if first_parse_expression():
        # 式
        arguments_count+=1
        function_number1=parse_expression()
        # ','
        while get_current_token()==20:
            get_next_token()
            if first_parse_expression():
                # 式
                arguments_count+=1
                function_number2=parse_expression()
            else:
                print("line:"+str(line_number)+" SyntaxError:','の後に'式'がありません") 
                sys.exit(1)
        #式だけでも良い
        return arguments_count,function_number1,function_number2

if __name__ == "__main__":
    print("---------------------------\n")
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
        