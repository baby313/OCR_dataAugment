# coding=utf-8
# 检查测试字符集对姓名和地址样本的覆盖率
# 70万地址 50万姓名，GB2312对地址的覆盖率超过99.9%， 对姓名覆盖率超过99.8%

import os,sys
import glob
reload(sys) 
sys.setdefaultencoding("utf8")
print sys.getdefaultencoding()

encode_maps={}
decode_maps={}
def loadDict(dictPath):
    pos = len(encode_maps)
    with open(dictPath) as file:
        for line in file:
            char = line.decode("utf-8").strip()
            encode_maps[char]=pos
            decode_maps[pos]=char
            pos += 1

loadDict("../Dicts/Chars.txt")
loadDict("../Dicts/GB2312.txt")

print("Char set: ", len(encode_maps))

def test(caseName, filePath):
    file = open(filePath)
    total = 0
    hits = 0
    for line in file:
        address = line.decode("utf-8").strip()
        total += len(address)
        for i in range(len(address)):
            if address[i] in encode_maps:
                hits += 1
            else:
                print address[i]
    
    print ("========Cover Result of " + caseName + "============")
    print("Total:", total)
    print("Hits:", hits)
    print("Hit percentage:", hits * 1.0 / total)


test("Name", "../Dicts/Name.txt")
test("Address", "../Dicts/Address.txt")
