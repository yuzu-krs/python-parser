######################################
# 入力正数の平方根を求めるプログラム #
# Written by Yasuharu Mizutani #
######################################
var C;
C:=20;
var f := C; # 計算結果を格納する変数
repeat 20 f:=(f+C/f)/2.0;
var f;

print(C, "の平方根は "); print(f); println("です");
println(); #空行の挿入

print("ちなみに，");
print("sqrt(", C, ") の値は");
println(@sqrt(C), "です");
println(); #空行の挿入


println("誤差は ", f-@sqrt(C), "です");
