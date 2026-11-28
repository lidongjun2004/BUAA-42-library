import os
from time import sleep

class Marsconnect():
    
    def __init__(self) -> None:
        pass
    
    def marsDebugInfo(self, asmPath, classPath):
        file = open("mars_result_machinecode.txt", "w")
        file.close()
        
        if (classPath == ""):
            out = os.popen("java -jar ./Mars_CO_v0.5.0.1.jar " + asmPath + " ig nc coL2 mc CompactDataAtZero dump .text HexText mars_result_machinecode.txt")
        else:
            os.popen("java -jar ./fernflower.jar " + classPath + " ./class")
            os.popen("javac -cp ./Mars_CO_v0.5.0.1.jar " + classPath[:-5] + "java -d ./")
            sleep(2)
            out = os.popen("java -jar ./Mars_CO_v0.5.0.1.jar " + asmPath + " ig nc coL2 mc CompactDataAtZero cl ./" + str(classPath).split("/")[-1] + " dump .text HexText mars_result_machinecode.txt")
        file2 = open("mars_result_coL2.txt", "w")
        file2.writelines(out)
        file2.close()
        
        pro = open("mars_result_coL2.txt", "r")
        #code = []
        content = []
        pro_content = pro.readlines()
        
        file = open("mars_result_machinecode.txt", "r")
        ori_lines = file.readlines()
        ori_lines.insert(0, "v2.0 raw\n")
        file.close()
        
        file = open("mars_result_machinecode.txt", "w")
        file.writelines(ori_lines)
        file.close()
        
        for line in pro_content:
            if line[0] == '@':
                #code.append(line[-10:-2] + "\n")
                content.append("Instr:0x" + line[-10:-2] + "  @" + line[3:11])
            elif line[0] == '\t' and line[2] == '$':
                content[-1] += (": " + line[2] + str(int(line[3:5])) + line[5:9] + "0x" + line[9:-1])
            elif line[0] == '\t' and line[2] == '*':
                content[-1] += (": " + line[2] + line[3:15] + "0x" + line[-9:-1])
        
        return content

if __name__ == '__main__':
    mars = Marsconnect()
    (a,b) = mars.marsDebugInfo("C:/Users/Messix/Desktop/P3/CPU_P3/test.asm")
    print(a)
    print(b)