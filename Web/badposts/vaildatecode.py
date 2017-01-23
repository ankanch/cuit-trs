#该库用来生成奇葩验证码
import random

RANGE_LOWER = 0         #验证码生成下限
RANGE_UPPER = 1         #验证码生成上限

#c储存验证码以及答案
VAILDATEDATA = [

]



#验证码生成函数
#返回 [验证问题，答案]
def getVaildateCode():
    qi = random.randint(0,99)