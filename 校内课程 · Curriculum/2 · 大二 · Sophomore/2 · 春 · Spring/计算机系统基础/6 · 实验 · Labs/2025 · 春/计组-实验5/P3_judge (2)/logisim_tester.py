import sys
import mylib.dumpTable as dt
from mylib.marslib import Marsconnect

def sys_argv():
    print(sys.argv)  
    # arg explanation
    # 'dump': shows the table of the circuit
    # 'comp': compare the result with others
    # 'compp3': compare for p3
    # 'mars' : compare with mars
    test_type = sys.argv[1]
    print('test_type:',test_type)
    return sys.argv
    

class Tester():
    
    def __init__(self) -> None:
        pass
        
    def doTest(self, test_type, tbPath, modulePath, queryPath, otherPath, romPath, asmPath, classPath):
        
        if (test_type == "dump"):
            
            if (tbPath == "" or modulePath == "" or queryPath == "" or romPath == ""):
                print("缺少参数")
                return
            print("开始运行，请等待")
            dt1 = dt.dumpTable(tbPath, modulePath, queryPath, romPath)
            dt1.dumpQuery()
        
        elif (test_type == "comp"):
            
            if (tbPath == "" or modulePath == "" or queryPath == "" or romPath == "" or otherPath ==""):
                print("缺少参数")
                return
            print("开始运行，请等待")
            dt1 = dt.dumpTable(tbPath, modulePath, queryPath, romPath)
            dt1.compCirc(otherPath)
        
        elif (test_type == "compp3"):
            
            if (tbPath == "" or modulePath == "" or queryPath == "" or romPath == "" or otherPath == ""):
                print("缺少参数")
                return
            print("开始运行，请等待")
            dt1 = dt.dumpTable(tbPath, modulePath, queryPath, romPath)
            dt1.compCircP3(otherPath)
            
        elif (test_type == "mars"):

            if (tbPath == "" or modulePath == "" or queryPath == "" or asmPath == ""):
                print("缺少参数")
                return
            print("开始运行，请等待，如果asm指令运行步数超过了0x0fff的时候请修改testbench电路的counter的最大值")
            mars = Marsconnect()
            content = mars.marsDebugInfo(asmPath, "")
            dt1 = dt.dumpTable(tbPath, modulePath, queryPath, "")
            dt1.compMars(content)
        
        elif (test_type == "exercise"):

            if (tbPath == "" or modulePath == "" or queryPath == "" or asmPath == "" or classPath == ""):
                print("缺少参数")
                return
            print("开始运行，请等待，如果asm指令运行步数超过了0x0fff的时候请修改testbench电路的counter的最大值")
            mars = Marsconnect()
            content = mars.marsDebugInfo(asmPath, classPath)
            dt1 = dt.dumpTable(tbPath, modulePath, queryPath, "")
            dt1.compMars(content)
        
        
        print("全部完成辣！")
        return
        

if __name__ == '__main__':
    test_type = input()
    print('test_type:',test_type)
    
    lt = Tester()
    lt.doTest(test_type)
    
    
        
        
        
    
    
    
    

