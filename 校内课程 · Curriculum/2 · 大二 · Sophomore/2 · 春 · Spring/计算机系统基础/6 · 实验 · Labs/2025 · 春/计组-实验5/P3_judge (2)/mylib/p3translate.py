
class Translator:
    
    def __init__(self) -> None:
        pass
    
    def bin2ins_P3(self, binstr:str) -> str:
        Instr = (int("".join(binstr.split()[0:8]),2))
        pc = (int("".join(binstr.split()[8:16]),2))
        regWrite = int("".join(binstr.split()[16:17]),2)
        regAddr = (int("".join(binstr.split()[17:19]),2))
        regData = (int("".join(binstr.split()[19:27]),2))
        memWrite = int("".join(binstr.split()[27:28]),2)
        memAddr = (int("".join(binstr.split()[28:36]),2))
        memData = (int("".join(binstr.split()[36:44]),2))
        
        if regWrite == 1:
            return "Instr:0x{:08x}  @{:08x}: ${:d} <= 0x{:08x}".format(Instr, pc, regAddr, regData)
        elif memWrite == 1:
            return "Instr:0x{:08x}  @{:08x}: *{:08x} <= 0x{:08x}".format(Instr, pc, memAddr, memData)
        else:
            return "Instr:0x{:08x}  @{:08x}".format(Instr, pc)