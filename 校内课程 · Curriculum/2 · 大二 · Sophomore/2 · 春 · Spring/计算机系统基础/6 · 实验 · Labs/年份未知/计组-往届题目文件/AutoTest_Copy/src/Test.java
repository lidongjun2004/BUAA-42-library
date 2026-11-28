public class Test {
    public static void main(String[] args){
        Instruction[] instr = new Instruction[100];
        for(int i = 0; i < 100; i ++ ){
            instr[i] = new Instruction();
        }
        instr[0].setType(Instruction.LUI);
        instr[0].setRt(16);
        instr[0].setImm(41);
        instr[1].setType(Instruction.ADDU);
        instr[1].setRd(31);
        instr[1].setRs(8);
        instr[1].setRt(25);
        instr[2].setType(Instruction.LW);
        instr[2].setRt(16);
        instr[2].setImm(12);
        instr[2].setRs(12);
        instr[3].setType(Instruction.BEQ);
        instr[3].setRs(25);
        instr[3].setRt(15);
        instr[3].setnPC(52);
        instr[4].setType(Instruction.LUI);
        instr[4].setRt(9);
        instr[4].setImm(194);
        instr[52].setType(Instruction.SUBU);
        instr[52].setRd(1);
        instr[52].setRs(2);
        instr[52].setRt(28);
        instr[53].setType(Instruction.SUBU);
        instr[53].setRd(15);
        instr[53].setRs(26);
        instr[53].setRt(7);
        instr[54].setType(Instruction.ORI);
        instr[54].setRd(29);
        instr[54].setRs(25);
        instr[54].setImm(127);
        instr[55].setType(Instruction.SW);
        instr[55].setRt(4);
        instr[55].setImm(97);
        instr[55].setRs(10);
        String[] ans = new String[100];
        new Correction().correction(instr, ans);
    }
}
