import java.io.*;

public class Generator {

    public static void generate(int INSTR_MAX, int FILE_MAX) throws FileNotFoundException, IOException{
        int j = 0;
        while(j < FILE_MAX) {
            Instruction[] instr = new Instruction[INSTR_MAX];
            String[] ans = new String[INSTR_MAX * 100];
            int[] j_type = new int[INSTR_MAX];
            int ans_max;

            for (int i = 0; i < INSTR_MAX; i++) {
                instr[i] = new Instruction();
                instr[i].random(INSTR_MAX);
            }
            try {
                new Correction().correction(instr, ans);
                ans_max = new Correction().correction(instr, ans);
            } catch (IndexOutOfBoundsException e) {
                continue;
            }
            for (int i = 0; i < INSTR_MAX; i++) {
                if (instr[i].getType() == Instruction.BEQ || instr[i].getType() == Instruction.J || instr[i].getType() == Instruction.JAL) {
                    j_type[instr[i].getnPC()] = instr[i].getType();
                }
            }
            //text
            System.out.println(String.format("正在生成text%d.asm", j));
            File test_case_file = new File(String.format("test/testcase%d", j));
            if (!test_case_file.exists()) {
                test_case_file.mkdir();
            }
            File f = new File(String.format("test/testcase%d/text.asm", j));
            FileOutputStream fop = new FileOutputStream(f);
            OutputStreamWriter writer = new OutputStreamWriter(fop);
            for (int i = 0; i < INSTR_MAX; i++) {
                if (j_type[i] == Instruction.BEQ || j_type[i] == Instruction.J || j_type[i] == Instruction.JAL) {
                    writer.append(String.format("label%d:\n", i));
                }
                writer.append(instr[i].output());
                if (instr[i].getType() == Instruction.BEQ || instr[i].getType() == Instruction.J || instr[i].getType() == Instruction.JAL) {
                    writer.append(String.format("label%d", instr[i].getnPC()));
                }
                writer.append("\n");
            }
            writer.close();
            fop.close();
            System.out.println(String.format("生成text%d.asm成功", j));
            //ans
            System.out.println(String.format("正在生成ans%d.txt", j));
            f = new File(String.format("test/testcase%d/ans.txt", j));
            fop = new FileOutputStream(f);
            writer = new OutputStreamWriter(fop);
            for (int i = 0; i < ans_max; i++) {
                writer.append(ans[i]);
                writer.append("\n");
            }
            writer.close();
            fop.close();
            System.out.println(String.format("生成ans%d.txt成功", j));
            j++;
        }
    }

    public static void main(String[] args) throws IOException {
            final int INSTR_MAX = 50;
            final int FILE_MAX = 10;
            generate(INSTR_MAX, FILE_MAX);
        }
}
