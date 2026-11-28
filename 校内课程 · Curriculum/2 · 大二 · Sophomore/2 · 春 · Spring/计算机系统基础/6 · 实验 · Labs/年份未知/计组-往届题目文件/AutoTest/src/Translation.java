import java.io.*;

public class Translation {
    public static void Translate(int max) throws FileNotFoundException, IOException, InterruptedException {
        String main_dir = "E:\\.main\\CO\\AutoTest";
        String fuse_dir = "D:\\ISE\\14.7\\ISE_DS\\ISE\\bin\\nt64";
        File to_compile;
        to_compile = new File("to_compile.bat");
        FileOutputStream fop = new FileOutputStream(to_compile);
        OutputStreamWriter writer = new OutputStreamWriter(fop);
        writer.append(fuse_dir + "\\fuse.exe " + "-nodebug -prj test.prj -o testmips.exe mips_tb");
        writer.append('\n');
        for(int i = 0; i < max; i ++ ) {
            String case_dir = String.format("test\\testcase%d\\", i);
            String target_dir = "code.txt";
            String code_command = "java -jar Mars.jar nc mc CompactDataAtZero a dump .text HexText" + " " + target_dir + " "  + String.format("test\\testpoint%d.asm", i);
            writer.append(code_command);
            writer.append('\n');
            String out_command = "testmips.exe -nolog -tclbatch test.tcl > " + case_dir + "out.txt";
            writer.append(out_command);
            writer.append('\n');
        }
        writer.close();
        fop.close();
        ProcessBuilder pb = new ProcessBuilder("to_compile.bat");
        pb.redirectError(new File("Compile_Error.txt"));
        Process p = pb.start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while((line = reader.readLine()) != null){
            System.out.println(line);
        }
        p.waitFor();
        p.destroy();
    }

    public static void main(String[] args) throws FileNotFoundException, IOException, InterruptedException{
        Translate(3);
    }
}