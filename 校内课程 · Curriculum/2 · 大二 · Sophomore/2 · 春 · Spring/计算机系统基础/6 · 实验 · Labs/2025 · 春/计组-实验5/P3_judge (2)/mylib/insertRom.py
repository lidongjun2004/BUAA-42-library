import re

class Inserter:
    
    def __init__(self) -> None:
        pass
    
    def doInsert(self, filePath, romPath):
        fp = open(filePath, "r+", encoding='utf-8')
        romfp = open(romPath, "r", encoding='utf-8')
        data = romfp.readlines()[1:]
        circfile = fp.readlines()
        
        finalCirc = ""
        for line in circfile:
            finalCirc += line[:-1]
            finalCirc += "\n"
        
        replace = "<a name=\"contents\">addr/data: 12 32\n"
        for i in data:
            replace += i[:-1]
            replace += ' '
        
        replace += "\n</a>"
        #print(replace)
        
        pattern = "<a name=\"contents\">([\s\S]*?)</a>"
        
        finalCirc = re.sub(pattern, replace, finalCirc)
        
        fp.close()
        
        wr = open(filePath, "w", encoding='utf-8')
        wr.write(finalCirc)
        wr.close()
        
        return finalCirc
    
    def doInsertStr(self, filePath, machinecode):
        fp = open(filePath, "r+", encoding='utf-8')
        circfile = fp.readlines()
        
        finalCirc = ""
        for line in circfile:
            finalCirc += line[:-1]
            finalCirc += "\n"
        
        replace = "<a name=\"contents\">addr/data: 12 32\n"
        for i in machinecode:
            replace += i[:-1]
            replace += ' '
        
        replace += "\n</a>\n"
        #print(replace)
        
        pattern = "<a name=\"contents\">addr/data:.*\n.*\n</a>"
        
        finalCirc = re.sub(pattern, replace, finalCirc)
        
        fp.close()
        
        wr = open(filePath, "w", encoding='utf-8')
        wr.write(finalCirc)
        wr.close()
        
        return finalCirc


if __name__ == '__main__':
    inserter = Inserter()
    strq = inserter.doInsert("../circ/CPU_P3.circ", "../mars_result_machinecode.txt")
        
        
        
            
        
        