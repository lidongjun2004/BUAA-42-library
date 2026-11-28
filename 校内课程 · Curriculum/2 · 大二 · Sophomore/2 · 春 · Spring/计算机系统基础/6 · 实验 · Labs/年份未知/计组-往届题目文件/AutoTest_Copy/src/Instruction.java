import java.util.Random;

public class Instruction {
    private int type;
    private int rs;
    private int rt;
    private int rd;
    private int imm;
    private int abs_imm;
    private int imm_4;
    private int nPC;

    public static int MAX   = 10;
    public static int NOP   = 0;
    public static final int ADDU  = 1;
    public static final int SUBU  = 2;
    public static final int ORI   = 3;
    public static final int LW    = 4;
    public static final int SW    = 5;
    public static final int LUI   = 6;
    public static final int BEQ   = 7;
    public static final int JAL   = 8;
    public static final int JR    = 9;
    public static final int J     = 10;
    public static final int MAX_IMM = 256;

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
    }

    public String output(){
        String output = "";
        switch (this.type){
            case ADDU   -> output = String.format("addu $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case SUBU   -> output = String.format("subu $%d, $%d, $%d", this.rd, this.rs, this.rt);
            case ORI    -> output = String.format("ori $%d, $%d, %d", this.rd, this.rs, this.abs_imm);
            case LW     -> output = String.format("lw $%d, %d($%d)", this.rt, this.imm, this.rs);
            case SW     -> output = String.format("sw $%d, %d($%d)", this.rt, this.imm, this.rs);
            case LUI    -> output = String.format("lui $%d, %d", this.rt, this.abs_imm);
            case BEQ    -> output = String.format("beq $%d, $%d, ", this.rs, this.rt);
            case J      -> output = String.format("j ");
            case JAL    -> output = String.format("jal ");
            case JR     -> output = String.format("jr $%d", this.rs);
        }
        return output;
    }
}
