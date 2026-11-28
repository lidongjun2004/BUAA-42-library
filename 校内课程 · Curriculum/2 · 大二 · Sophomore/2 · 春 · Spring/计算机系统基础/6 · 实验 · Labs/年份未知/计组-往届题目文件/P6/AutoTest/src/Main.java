import java.io.FileNotFoundException;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws FileNotFoundException, IOException, InterruptedException {
        int instr_max = 300;
        int file_max = 20;

        new Generator().generate(instr_max, file_max);
        new Translation().Translate(file_max);
        new Comparison().compare(file_max);
    }
}
