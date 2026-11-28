import os
from mylib.p3translate import Translator
from mylib.insertRom import Inserter

class dumpTable():
        
    def __init__(self, pathToTb, pathToModule, pathToQuery, pathToRom) -> None:
        self.tbPath = pathToTb
        self.modulePath = pathToModule
        self.queryPath = pathToQuery
        self.romPath = pathToRom
        print("tbpath：",self.tbPath)
        
    def dumpQuery(self):
        inserter = Inserter()
        inserter.doInsert(self.queryPath, self.romPath)
        out = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + self.queryPath)
        file = open("query_result.txt", "w")
        file.writelines(out)
        file.close()
        
    def compCirc(self, otherPath):
        inserter = Inserter()
        inserter.doInsert(self.queryPath, self.romPath)
        inserter.doInsert(otherPath, self.romPath)
        outMy = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + self.queryPath)
        outOther = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + otherPath)
        
        file1 = open("compare_result_my.txt", "w")
        file1.write(self.queryPath + "table:\n")
        file1.writelines(outMy)
        
        file2 = open("compare_result_your.txt", "w")
        file2.write(otherPath + "table:\n")
        file2.writelines(outOther)
        
        file1.close()
        file2.close()
        
        listMy = open("compare_result_my.txt", "r").readlines()[1:]
        listOther = open("compare_result_your.txt", "r").readlines()[1:]
        flag = 0
        for i in range(0,listMy.__len__()):
            if flag > 10:
                break
            if listMy[i] != listOther[i]:
                flag += 1
                print("可能的错误 在 line " + str(i) + " :\n")
                print("outMy:",listMy[i])
                print("outYour:",listOther[i])
                print("显示前10条错误，具体错误请具体分析")
                break
    
    def compCircP3(self, otherPath):
        inserter = Inserter()
        inserter.doInsert(self.queryPath, self.romPath)
        outMy = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + self.queryPath)
        outOther = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + otherPath)
        
        file1 = open("compare_result_my.txt", "w")
        file1.write(self.queryPath + "table:\n")
        file1.writelines(outMy)
        
        file2 = open("compare_result_your.txt", "w")
        file2.write(otherPath + "table:\n")
        file2.writelines(outOther)
        
        file1.close()
        file2.close()
        
        t = Translator()
        listMy = open("compare_result_my.txt", "r").readlines()[1:]
        listOther = open("compare_result_your.txt", "r").readlines()[1:]
        flag = 0
        for i in range(0,listMy.__len__()):
            if flag>10:
                break
            if t.bin2ins_P3(listMy[i]) != t.bin2ins_P3(listOther[i]):
                if int("".join(listMy[i].split()),2) == 0 and int("".join(listOther[i].split()),2) == 0:
                    continue
                print("可能的错误 在 line " + str(i) + " :")
                flag += 1
                print("outMy:",t.bin2ins_P3(listMy[i]))
                print("outYour:",t.bin2ins_P3(listOther[i]))
                print("")
        
        if flag == 0:
            print("恭喜你，一样")
        else:
            print("显示前10条错误，具体错误请具体分析")
        
        
    def compMars(self, Content):
        inserter = Inserter()
        inserter.doInsert(self.queryPath, "./mars_result_machinecode.txt")
        
        outMy = os.popen("java -jar ./logisim-generic-2.7.1.jar " + self.tbPath + " -tty table -sub "
                  + self.modulePath + " " + self.queryPath)
        
        file1 = open("compare_result_my.txt", "w")
        file1.write(self.queryPath + "table:\n")
        file1.writelines(outMy)
        
        file1.close()
        
        t = Translator()
        listMy = open("compare_result_my.txt", "r").readlines()[1:]
        print("lenmy:",listMy.__len__(),"lenco:",Content.__len__())
        flag = 0
        for i in range(0,Content.__len__()):
            if flag>10:
                break
            if t.bin2ins_P3(listMy[i]) != Content[i]:
                if t.bin2ins_P3(listMy[i])[8:16] == "00000000" and Content[i][8:16] == "00000000":
                    continue
                if t.bin2ins_P3(listMy[i])[0:27] == Content[i][0:27] and t.bin2ins_P3(listMy[i])[29:32] == "$0 ":
                    continue
                print("可能的错误 在 line " + str(i) + " :")
                flag += 1
                print("outMy:",t.bin2ins_P3(listMy[i]))
                print("outMars:",Content[i])
                print("")
        
        
        if flag == 0:
            print("恭喜你，和MARS一样")
        else:
            print("显示前10条错误，具体错误请具体分析")
        
        
        
        
            
        
        
        
        
    