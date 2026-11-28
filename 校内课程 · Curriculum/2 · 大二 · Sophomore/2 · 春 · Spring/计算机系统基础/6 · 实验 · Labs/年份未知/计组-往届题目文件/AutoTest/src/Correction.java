import java.util.Random;

public class Correction {
    public static final int DM_length = 1024;
    public int correction(Instruction[] instr, String[] ans) {
        int time;
        int imm;
        int ans_max = 0;
        boolean[] reset = new boolean[1];
        int[] GRF = new int[32];
        int[] DM = new int[DM_length];
        int Instr_length = instr.length;
        int[] count_loop = new int[Instr_length];
        int[] count_mem = new int[Instr_length];
        boolean last_j = false;
        int i = 0;

        reset(GRF, DM, count_loop, count_mem, ans);
        while(i < Instr_length){
            GRF[0] = 0;
            time = 0;
            int data;
            int addr;
            switch(instr[i].getType()){
                case Instruction.LB:
                    last_j = false;
                    int [] get = load_memory(1, GRF, DM, count_loop, count_mem, instr, ans, i, Instr_length, reset);
                    if(reset[0]){
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    else{
                        addr = get[0];
                        if(get[0] > 7){
                            data = get[0] % 8 - 8;
                        }
                        else{
                            data = get[0];
                        }
                        GRF[addr] = data;
                        ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    }
                    break;
                case Instruction.LBU:
                    last_j = false;
                    int [] get = load_memory(1, GRF, DM, count_loop, count_mem, instr, ans, i, Instr_length, reset);
                    if(reset[0]){
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    else{
                        addr = get[0];
                        data = get[0];
                        GRF[addr] = data;
                        ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    }
                    break;
                case Instruction.LH:
                    last_j = false;
                    int [] get = load_memory(2, GRF, DM, count_loop, count_mem, instr, ans, i, Instr_length, reset);
                    if(reset[0]){
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    else{
                        addr = get[0];
                        if(get[0] > 128){
                            data = get[0] % 128 - 128;
                        }
                        else{
                            data = get[0];
                        }
                        GRF[addr] = data;
                        ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    }
                    break;
                case Instruction.LHU:
                    last_j = false;
                    int [] get = load_memory(2, GRF, DM, count_loop, count_mem, instr, ans, i, Instr_length, reset);
                    if(reset[0]){
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    else{
                        addr = get[0];
                        data = get[0];
                        GRF[addr] = data;
                        ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    }
                    break;
                case Instruction.LW:
                    count_mem[i] ++ ;
                    imm = instr[i].getImm();
                    if(count_mem[i] > 1 && (GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % 4 > 0)){
                        instr[i].random(Instr_length);
                        reset(GRF, DM, count_loop, count_mem, ans);
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    while(GRF[instr[i].getRs()] + imm < 0 && time < 10){
                        imm = new Random().nextInt(Instruction.MAX_IMM * 2) - Instruction.MAX_IMM;
                        time ++ ;
                    }
                    imm = ((GRF[instr[i].getRs()] + imm) % DM_length ) / 4 * 4 - GRF[instr[i].getRs()];
                    imm %= Instruction.MAX_IMM;
                    if(GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % 4 > 0)
                    {
                        instr[i].random(Instr_length);
                        continue;
                    }
                    addr = instr[i].getRt();
                    data = DM[(GRF[instr[i].getRs()] + imm) / 4];
                    GRF[addr] = data;
                    ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    instr[i].setImm(imm);
                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.SW:
                    count_mem[i] ++ ;
                    imm = instr[i].getImm();
                    if(count_mem[i] > 1 && (GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % 4 > 0)){
                        instr[i].random(Instr_length);
                        reset(GRF, DM, count_loop, count_mem, ans);
                        ans_max = 0;
                        i = 0;
                        continue;
                    }
                    while(GRF[instr[i].getRs()] + imm < 0 && time < 10){
                        imm = new Random().nextInt(Instruction.MAX_IMM * 2) - Instruction.MAX_IMM;
                        time ++ ;
                    }
                    imm = ((GRF[instr[i].getRs()] + imm) % DM_length ) / 4 * 4 - GRF[instr[i].getRs()];
                    imm %= Instruction.MAX_IMM;
                    if(GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % 4 > 0)
                    {
                        instr[i].random(Instr_length);
                        continue;
                    }
                    else{
                        instr[i].setImm(imm);
                        //System.out.println(String.format("%d ", GRF[instr[i].getRs()] + imm) + instr[i].output());
                    }
                    addr = GRF[instr[i].getRs()] + imm;
                    data = GRF[instr[i].getRt()];
                    DM[addr / 4] = data;
                    ans[ans_max ++ ] = String.format("@%08x: *%08x <= %08x", 0x3000 + i * 4, addr ,data);

                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.ADDU:
                    addr = instr[i].getRd();
                    data = GRF[instr[i].getRs()] + GRF[instr[i].getRt()];
                    GRF[addr] = data;
                    ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.SUBU:
                    addr = instr[i].getRd();
                    data = GRF[instr[i].getRs()] - GRF[instr[i].getRt()];
                    GRF[addr] = data;
                    ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.ORI:
                    addr = instr[i].getRd();
                    data = GRF[instr[i].getRs()] | instr[i].getAbs_imm();
                    GRF[addr] = data;
                    ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.LUI:
                    addr = instr[i].getRt();
                    data = instr[i].getAbs_imm() * 65536;
                    GRF[addr] = data;
                    ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                    last_j = false;
                    i ++ ;
                    break;
                case Instruction.BEQ:
                    if(count_loop[i] > 3 || last_j){
                        instr[i].random(Instr_length);
                        reset(GRF, DM, count_loop, count_mem, ans);
                        ans_max = 0;
                        i = 0;
                        last_j = false;
                    }
                    else if(GRF[instr[i].getRs()] == GRF[instr[i].getRt()]){
                        count_loop[i] ++ ;
                        last_j = true;
                        if(i + 1 < Instr_length) {
                            ans_max = delay(GRF, DM, count_mem, instr[i + 1], ans, ans_max, i + 1, 0x3000 + i * 4 + 4, Instr_length, reset);
                            if(reset[0]){
                                reset(GRF, DM, count_loop, count_mem, ans);
                                i = 0;
                                ans_max = 0;
                                continue;
                            }
                        }
                        i = instr[i].getnPC();
                    }
                    else{
                        i ++ ;
                    }
                    break;
                case Instruction.J:
                    if(count_loop[i] > 3 || last_j){
                        instr[i].random(Instr_length);
                        last_j = false;
                        i = 0;
                        reset(GRF, DM, count_loop, count_mem, ans);
                    }
                    else{
                        last_j = true;
                        count_loop[i] ++ ;
                        if(i + 1 < Instr_length) {
                            ans_max = delay(GRF, DM, count_mem, instr[i + 1], ans, ans_max, i + 1, 0x3000 + i * 4 + 4, Instr_length, reset);
                            if(reset[0]){
                                reset(GRF, DM, count_loop, count_mem, ans);
                                i = 0;
                                ans_max = 0;
                                continue;
                            }
                        }
                        i = instr[i].getnPC();
                    }
                    break;
                case Instruction.JAL:
                    if(count_loop[i] > 3 || last_j){
                        instr[i].random(Instr_length);
                        last_j = false;
                        i = 0;
                        reset(GRF, DM, count_loop, count_mem, ans);
                        ans_max = 0;
                    }
                    else{
                        last_j = true;
                        count_loop[i] ++ ;
                        addr = 31;
                        data = 0x3000 + i * 4 + 8;
                        GRF[addr] = data;
                        ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", 0x3000 + i * 4, addr ,data);
                        if(i + 1 < Instr_length) {
                            ans_max = delay(GRF, DM, count_mem, instr[i + 1], ans, ans_max, i + 1, 0x3000 + i * 4 + 4, Instr_length, reset);
                            if(reset[0]){
                                reset(GRF, DM, count_loop, count_mem, ans);
                                i = 0;
                                ans_max = 0;
                                continue;
                            }
                        }
                        i = instr[i].getnPC();
                    }
                    break;
                case Instruction.JR:
                    if(count_loop[i] > 3 || last_j){
                        instr[i].random(Instr_length);
                        last_j = false;
                        i = 0;
                        reset(GRF, DM, count_loop, count_mem, ans);
                        ans_max = 0;
                    }
                    else{
                        last_j = true;
                        count_loop[i] ++ ;
                        int rs = instr[i].getRs();
                        while((GRF[rs] - 0x3000 < 0 || (GRF[rs] - 0x3000) % 4 > 0 || (GRF[rs] - 0x3000) / 4 > Instr_length) && time < 10){
                            time ++;
                            rs = new Random().nextInt(32);
                        }
                        if(time == 10)
                        {
                            instr[i].random(Instr_length);
                            continue;
                        }
                        instr[i].setRs(rs);
                        int nPC = (GRF[rs] - 0x3000) / 4;
                        if(i + 1 < Instr_length) {
                            ans_max = delay(GRF, DM, count_mem, instr[i + 1], ans, ans_max, i + 1, 0x3000 + i * 4 + 4, Instr_length, reset);
                            if(reset[0]){
                                reset(GRF, DM, count_loop, count_mem, ans);
                                ans_max = 0;
                                i = 0;
                                continue;
                            }
                        }
                        i = nPC;
                    }
                    break;
            }
        }
        return ans_max;
    }

    public int delay(int[] GRF, int[] DM, int[] count_mem, Instruction instr, String[] ans, int ans_max, int i, int PC, int instr_length, boolean[] reset){
        int addr;
        int data;
        int time = 0;
        int imm;
        GRF[0] = 0;
        reset[0] = false;
        switch(instr.getType()){
            case Instruction.ADDU:
                addr = instr.getRd();
                data = GRF[instr.getRs()] + GRF[instr.getRt()];
                GRF[addr] = data;
                ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", PC, addr, data);
                break;
            case Instruction.SUBU:
                addr = instr.getRd();
                data = GRF[instr.getRs()] - GRF[instr.getRt()];
                GRF[addr] = data;
                ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", PC, addr, data);
                break;
            case Instruction.ORI:
                addr = instr.getRd();
                data = GRF[instr.getRs()] | instr.getAbs_imm();
                GRF[addr] = data;
                ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", PC, addr, data);
                break;
            case Instruction.LW:
                count_mem[i] ++ ;
                imm = instr.getImm();
                if(count_mem[i] > 1 && (GRF[instr.getRs()] + imm < 0 || GRF[instr.getRs()] + imm >= DM_length || (GRF[instr.getRs()] + imm) % 4 > 0)){
                    instr.random(instr_length);
                    reset[0] = true;
                    return 0;
                }
                while(GRF[instr.getRs()] + imm < 0 && time < 10){
                    imm = new Random().nextInt(Instruction.MAX_IMM * 2) - Instruction.MAX_IMM;
                    time ++ ;
                }
                imm = ((GRF[instr.getRs()] + imm) % DM_length ) / 4 * 4 - GRF[instr.getRs()];
                imm %= Instruction.MAX_IMM;
                if(GRF[instr.getRs()] + imm < 0 || GRF[instr.getRs()] + imm >= DM_length || (GRF[instr.getRs()] + imm) % 4 > 0)
                {
                    instr.random(instr_length);
                    return delay(GRF, DM, count_mem, instr, ans, ans_max, i, PC, instr_length, reset);
                }
                addr = instr.getRt();
                data = DM[(GRF[instr.getRs()] + imm) / 4];
                GRF[addr] = data;
                ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", PC, addr, data);
                instr.setImm(imm);
                break;
            case Instruction.SW:
                count_mem[i] ++ ;
                imm = instr.getImm();
                if(count_mem[i] > 1 && (GRF[instr.getRs()] + imm < 0 || GRF[instr.getRs()] + imm >= DM_length || (GRF[instr.getRs()] + imm) % 4 > 0)){
                    instr.random(instr_length);
                    reset[0] = true;
                    return 0;
                }
                while(GRF[instr.getRs()] + imm < 0 && time < 10){
                    imm = new Random().nextInt(Instruction.MAX_IMM * 2) - Instruction.MAX_IMM;
                    time ++ ;
                }
                imm = ((GRF[instr.getRs()] + imm) % DM_length ) / 4 * 4 - GRF[instr.getRs()];
                imm %= Instruction.MAX_IMM;
                if(GRF[instr.getRs()] + imm < 0 || GRF[instr.getRs()] + imm >= DM_length || (GRF[instr.getRs()] + imm) % 4 > 0) {
                    instr.random(instr_length);
                    return delay(GRF, DM, count_mem, instr, ans, ans_max, i, PC, instr_length, reset);
                }
                else{
                    instr.setImm(imm);
                    //System.out.println(String.format("%d ", GRF[instr.getRs()] + imm) + instr.output());
                }
                addr = GRF[instr.getRs()] + imm;
                data = GRF[instr.getRt()];
                DM[addr / 4] = data;
                ans[ans_max ++ ] = String.format("@%08x: *%08x <= %08x", PC, addr, data);
                break;
            case Instruction.LUI:
                addr = instr.getRt();
                data = instr.getAbs_imm() * 65536;
                GRF[addr] = data;
                ans[ans_max ++ ] = String.format("@%08x: $%2d <= %08x", PC, addr, data);
                break;
            case Instruction.BEQ:
            case Instruction.J:
            case Instruction.JR:
            case Instruction.JAL:
                instr.random(instr_length);
                return delay(GRF, DM, count_mem, instr, ans, ans_max, i, PC, instr_length, reset);
        }
        return ans_max;
    }

    public void reset(int[] GRF, int[] DM, int[] count_loop, int[] count_mem, String [] ans){
        for(int i = 0; i < 32; i ++)
        {
            GRF[i] = 0;
        }
        GRF[28] = 0x1800;
        GRF[29] = 0x2ffc;
        for(int i = 0; i < DM_length; i ++ ){
            DM[i] = 0;
        }
        for(int i = 0; i < count_loop.length; i ++ ){
            count_loop[i] = 0;
        }
        for(int i = 0; i < count_mem.length; i ++ ){
            count_mem[i] = 0;
        }
        for(int i = 0; i < ans.length; i ++ ){
            ans[i] = "";
        }
    }

    public int[] load_memory(int size, int[] GRF, int[] DM, int[] count_loop, int[] count_mem, Instruction[] instr, String[] ans,  int i,  int instr_length, boolean[] reset){
        count_mem[i] ++ ;
        int imm = instr[i].getImm();
        int time = 0;
        if(count_mem[i] > 1 && (GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % size > 0)){
            instr[i].random(instr_length);
            reset(GRF, DM, count_loop, count_mem, ans);
            reset[0] = true;
        }
        while(GRF[instr[i].getRs()] + imm < 0 && time < 10){
            imm = new Random().nextInt(Instruction.MAX_IMM * 2) - Instruction.MAX_IMM;
            time ++ ;
        }
        imm = ((GRF[instr[i].getRs()] + imm) % DM_length ) / size * size - GRF[instr[i].getRs()];
        imm %= Instruction.MAX_IMM;
        if(GRF[instr[i].getRs()] + imm < 0 || GRF[instr[i].getRs()] + imm >= DM_length || (GRF[instr[i].getRs()] + imm) % size > 0)
        {
            instr[i].random(instr_length);
            reset[0] = true;
        }
        int addr = instr[i].getRt();
        int memaddr = (GRF[instr[i].getRs()] + imm);
        int memdata = DM[memaddr / 4];
        int [] toreturn = new int[2];
        int data = 0;
        if
        toreturn[0] = addr;
        toreturn[1] = data;
        instr[i].setImm(imm);
        return toreturn;
    }
}
