import os


dict = {"bird" : "鳥", "cat" : "貓",
"dog" : "狗", "fish" : "魚",
"mouse" : "老鼠", "rabbit" : "兔子",
"cow" : "母牛", "horse" : "馬",
"pig" : "豬", "sheep" : "綿羊"}

def funcSelect():
    print("請輸入指令: 1.英翻中 2.中翻英 3.離開 ")
    
    input01 = input()
    if(input01 == "1"):
        print("")
        ENtoCH()
        print("")
    elif(input01 == "2"):
        print("")
        CHToEN()
        print("")
    elif(input01 == "3"):
        print("")
        os._exit(0)
    else:
        print("請輸入正確的指令!")
        print("")
        return 0

def CHToEN():
    print("請輸入中文單字: ")
    input01 = input()
    if(input01 in list(dict.values())):
        print(input01 + " => " + list(dict.keys())[list(dict.values()).index(input01)])
    else:
        print("查無此單字")
        
def ENtoCH():
    print("請輸入英文單字: ")
    input01 = input()
    if(input01 in dict):
        print(input01 + " => " + dict[input01])
    else:
        print("查無此單字")

while(True):
    funcSelect()