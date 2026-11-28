import java.util.Random;

public class Instruction {
    private int type;
    private int rs;
    private int rt;
    private int rd;
    private int imm;
    private int abs_imm;
    private int imm_4;
    private int s;
    private int nPC;

    public static final int MAX   = 51;
    public static final int MAX_IMM = 65536;
    public static final int NOP   = 0;
    public static final int LB    = 1;
    public static final int LBU   = 2;
    public static final int LH    = 3;
    public static final int LHU   = 4;
    public static final int LW    = 5;
    public static final int SB    = 6;
    public static final int SH    = 7;
    public static final int SW    = 8;
    public static final int ADD   = 9;
    public static final int ADDU  = 10;
    public static final int SUB   = 11;
    public static final int SUBU  = 12;
    public static final int MULT  = 13;
    public static final int MULTU = 14;
    public static final int DIV   = 15;
    public static final int DIVU  = 16;
    public static final int SLL   = 17;
    public static final int SRL   = 18;
    public static final int SRA   = 19;
    public static final int SLLV  = 20;
    public static final int SRLV  = 21;
    public static final int SRAV  = 22;
    public static final int AND   = 23;
    public static final int OR    = 24;
    public static final int XOR   = 25;
    public static final int NOR   = 26;
    public static final int ADDI  = 27;
    public static final int ADDIU = 28;
    public static final int ANDI  = 29;
    public static final int ORI   = 30;
    public static final int XORI  = 31;
    public static final int LUI   = 32;
    public static final int SLT   = 33;
    public static final int SLTI  = 34;
    public static final int SLTIU = 35;
    public static final int SLTU  = 36;
    public static final int BEQ   = 37;
    public static final int BNE   = 38;
    public static final int BLEZ  = 39;
    public static final int BGTZ  = 40;
    public static final int BLTZ  = 41;
    public static final int BGEZ  = 42;
    public static final int J     = 43;
    public static final int JAL   = 44;
    public static final int JALR  = 45;
    public static final int JR    = 46;
    public static final int MFHI  = 47;
    public static final int MFLO  = 48;
    public static final int MTHI  = 49;
    public static final int MTLO  = 50;

    public Instruction(){}

    public Instruction(int type){
        this.type = type;
    }

    public void setType(int type){
        this.type = type;
    }

    public void setRs(int rs){
        this.rs = rs;
    }

    public void setRt(int rt){
        this.rt = rt;
    }

    public void setRd(int rd){
        this.rd = rd;
    }

    public void setImm(int imm){
        this.imm = imm;
        this.abs_imm = Math.abs(imm);
        this.imm_4 = abs_imm / 4 * 4;
    }

    public void setnPC(int nPC) {
        this.nPC = nPC;
    }

    public void setS(int s){
        this.s = s;
    }

    public int getType(){
        return this.type;
    }

    public int getRs(){
        return this.rs;
    }

    public int getRt(){
        return this.rt;
    }

    public int getRd(){
        return this.rd;
    }

    public int getImm(){
        return this.imm;

    }

    public int getAbs_imm(){
        return abs_imm;
    }

    public int getnPC(){
        return nPC;
    }

    public int getS(){
        return this.s;
    }

    public void random(int INSTR_MAX){
        //setType
        int type = new Random().nextInt(MAX);
        while(type == 0){
            type = new Random().nextInt(MAX);
        }
        this.setType(type);

        //setRs
        this.setRs(new Random().nextInt(32));

        //setRt
        this.setRt(new Random().nextInt(32));

        //setRd
        this.setRd(new Random().nextInt(32));

        //setImm
        this.setImm(new Random().nextInt(2 * MAX_IMM) - MAX_IMM);

        //setnPC
        this.setnPC(new Random().nextInt(INSTR_MAX));

        //setS
        this.setS(new Random().nextInt(32));
    }

    public String output(){
        String output = "";
        switch (this.type){
            case LB     -> output = String.format("lb $%d, %d($%d)", this.rt, this.imm, this.rs);
            case LBU    -> output = String.format("lbu $%d, %d($%d)", this.rt, this.imm, this.rs);
            case LH     -> output = String.format("lh $%d, %d($%d)", this.rt, this.imm, this.rs);
            case LHU    -> output = String.format("lhu $%d, %d($%d)", this.rt, this.imm, this.rs);
            case LW     -> output = String.format("lw $%d, %d($%d)", this.rt, this.imm, this.rs);
            case SB     -> output = String.format("sb $%d, %d($%d)", this.rt, this.imm, this.rs);
            case SH     -> output = String.format("sh $%d, %d($%d)", this.rt, this.imm, this.rs);
            case SW     -> output = String.format("sw $%d, %d($%d)", this.rt, this.imm, this.rs);
            case ADD    -> output = String.format("add $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case ADDU   -> output = String.format("addu $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case SUB    -> output = String.format("sub $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case SUBU   -> output = String.format("subu $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case MULT   -> output = String.format("mult $%d, $%d", this.rs, this.rt);
            case MULTU  -> output = String.format("multu $%d, $%d", this.rs, this.rt);
            case DIV    -> output = String.format("div $%d, $%d", this.rs, this.rt);
            case DIVU   -> output = String.format("divu $%d, $%d", this.rs, this.rt);
            case SLL    -> output = String.format("sll $%d, $%d, $%d", this.rd, this.rt, this.s);
            case SRL    -> output = String.format("srl $%d, $%d, $%d", this.rd, this.rt, this.s);
            case SRA    -> output = String.format("sra $%d, $%d, $%d", this.rd, this.rt, this.s);
            case SLLV   -> output = String.format("sllv $%d, $%d, $%d", this.rd, this.rt, this.rs);
            case SRLV   -> output = String.format("srlv $%d, $%d, $%d", this.rd, this.rt, this.rs);
            case SRAV   -> output = String.format("srav $%d, $%d, $%d", this.rd, this.rt, this.rs);
            case AND    -> output = String.format("and $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case OR     -> output = String.format("or $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case XOR    -> output = String.format("xor $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case NOR    -> output = String.format("nor $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case ADDI    -> output = String.format("addi $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case ADDIU    -> output = String.format("addiu $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case ANDI    -> output = String.format("andi $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case ORI    -> output = String.format("ori $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case XORI    -> output = String.format("xori $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case LUI    -> output = String.format("lui $%d, %d", this.rt, this.abs_imm);
            case SLT    -> output = String.format("slt $%d, $%d, %d", this.rd, this.rs, this.rt);
            case SLTI    -> output = String.format("slti $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case SLTIU    -> output = String.format("sltiu $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case SLTU    -> output = String.format("sltu $%d, $%d, %d", this.rd, this.rs, this.rt);
            case BEQ    -> output = String.format("beq $%d, $%d, ", this.rs, this.rt);
            case BNE    -> output = String.format("bne $%d, $%d, ", this.rs, this.rt);
            case BLEZ    -> output = String.format("blez $%d, $%d, ", this.rs, this.rt);
            case BGTZ   -> output = String.format("bgtz $%d, $%d, ", this.rs, this.rt);
            case BLTZ    -> output = String.format("bltz $%d, $%d, ", this.rs, this.rt);
            case BGEZ    -> output = String.format("bgez $%d, $%d, ", this.rs, this.rt);
            case J      -> output = String.format("j ");
            case JAL    -> output = String.format("jal ");
            case JALR     -> output = String.format("jalr $%d, $%d", this.rs, this.rt);
            case JR     -> output = String.format("jr $%d", this.rs);
            case MFHI     -> output = String.format("mfhi $%d", this.rs);
            case MFLO     -> output = String.format("mflo $%d", this.rs);
            case MTHI     -> output = String.format("mthi $%d", this.rs);
            case MTLO     -> output = String.format("mtlo $%d", this.rs);
        }
        return output;
    }
}
