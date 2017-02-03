#该库用来生成奇葩验证码
import random

RANGE_LOWER = 0         #验证码生成下限
RANGE_UPPER = 9         #验证码生成上限

#c储存验证码以及答案
VAILDATEDATA = [
["a在abc中的位置（从0开始）","0"],
["a在bcca中的位置（从1开始）","4"],
["填空：成都信___工程大学","息"],
["填空：教（wu）___处","务"],
["100加上100等于多少？","200"],
["请输入：kanch","kanch"],
["我们学校有几个食堂？（1/2/3）","2"],
["填空：成都信息____大学","工程"],
["第二个 x 在12xyx中的位置（从0开始）","4"],
["50加上10等于多少？","60"]     
]



#验证码生成函数
#返回 [验证问题，答案]
def getVaildateCode():
    qi = random.randint(RANGE_LOWER,RANGE_UPPER)
    return VAILDATEDATA[qi]

#该函数用来检查验证吗
def check(q,a):
    for question in VAILDATEDATA:
        if question[0] == q:
            if a == question[1]:
                return True
    return False