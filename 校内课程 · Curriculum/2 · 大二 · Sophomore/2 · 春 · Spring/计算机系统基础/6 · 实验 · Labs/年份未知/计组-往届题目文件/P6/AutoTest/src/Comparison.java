import java.io.*;

public class Comparison {
    public static void compare(int instr_max) throws FileNotFoundException, IOException {
        File cmp_ans_file = new File("Comparison Output.txt");
        FileOutputStream fop = new FileOutputStream(cmp_ans_file);
        OutputStreamWriter writer = new OutputStreamWriter(fop);
        String[] cmp_ans = new String[instr_max];
        int right = 0;
        for(int i = 0; i < instr_max; i ++ ){
            String[] ans = new String[10000];
            String[] out = new String[10000];
            int ans_max = 0;
            int out_max = 0;
            File f;
            FileInputStream fip;
            InputStreamReader reader;
            BufferedReader bufferedReader;
            String text;

            f = new File(String.format("test\\testcase%d\\ans.txt", i));
            fip = new FileInputStream(f);
            reader = new InputStreamReader(fip);
            bufferedReader = new BufferedReader(reader);
            while((text = bufferedReader.readLine()) != null){
                ans[ans_max ++ ] = text;
            }
            f = new File(String.format("test\\testcase%d\\out.txt", i));
            fip = new FileInputStream(f);
            reader = new InputStreamReader(fip);
            bufferedReader = new BufferedReader(reader);
            for(int j = 0; j < 10; j ++ ){
                text = bufferedReader.readLine();
            }
            while((text = bufferedReader.readLine()) != null){
                out[out_max ++ ] = text.substring(text.indexOf('@'));
            }
            while(ans[ans_max - 1].indexOf('@') == -1){
                ans_max -- ;
            }
            while(out[out_max - 1].indexOf('@') == -1){
                out_max -- ;
            }
            if(out_max < ans_max){
                cmp_ans[i] = String.format("Testcase%3d: Your output are less than the standard answer", i);
            }
            else if(out_max > ans_max){
                cmp_ans[i] = String.format("Testcase%3d: Your output are more than the standard answer", i);
            }
            else{
                boolean flag = true;
                for(int j = 0; j < ans_max; j ++ ){
                    if(out[j].compareTo(ans[j]) != 0){
                        cmp_ans[i] = String.format("Testcase%3d: We got ", i) + out[j] + ", while we expect " + ans[j];
                        flag = false;
                        break;
                    }
                }
                if(flag){
                    cmp_ans[i] = String.format("Testcase%3d: Accepted", i);
                    right ++ ;
                }
            }
        }
        writer.append(String.format("Total Cases: %d, Right Cases: %d", instr_max, right));
        writer.append('\n');
        for(int i = 0; i < instr_max; i ++ ){
            writer.append(cmp_ans[i]);
            writer.append('\n');
        }
        writer.close();
        fop.close();
    }

    public static void main(String[] args) throws FileNotFoundException, IOException{
        compare(50);
    }
}
