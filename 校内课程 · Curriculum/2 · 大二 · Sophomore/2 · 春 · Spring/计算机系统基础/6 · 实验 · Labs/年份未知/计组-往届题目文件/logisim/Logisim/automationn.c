#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(){
    int start_x = 150, start_y = 50;
    int step_x = 140, step_y = 140;
    freopen("output.txt", "w", stdout);

    char template[] = 
        "    <comp lib=\"4\" loc=\"(%d,%d)\" name=\"Register\">\n"
        "</comp>\n"
        "    <comp lib=\"0\" loc=\"(%d,%d)\" name=\"Tunnel\">\n"
        "    <a name=\"facing\" val=\"north\"/>\n"
        "    <a name=\"label\" val=\"clk\"/>\n"
        "</comp>\n"
        "    <comp lib=\"0\" loc=\"(%d,%d)\" name=\"Tunnel\">\n"
        "    <a name=\"facing\" val=\"north\"/>\n"
        "    <a name=\"label\" val=\"reset\"/>\n"
        "</comp>\n"
        "    <comp lib=\"0\" loc=\"(%d,%d)\" name=\"Tunnel\">\n"
        "    <a name=\"width\" val=\"8\"/>\n"
        "    <a name=\"label\" val=\"Out%d\"/>\n"
        "</comp>\n"
        "    <comp lib=\"0\" loc=\"(%d,%d)\" name=\"Tunnel\">\n"
        "    <a name=\"width\" val=\"8\"/>\n"
        "    <a name=\"facing\" val=\"east\"/>\n"
        "    <a name=\"label\" val=\"In%d\"/>\n"
        "</comp>\n";

    for (int i = 0; i < 8; i++){
        for (int j = 0; j < 4; j++){
            char buffer[2000];
            snprintf(buffer, sizeof(buffer), template, start_x + step_x * i, start_y + step_y * j, start_x + step_x * i - 20, start_y + step_y * j + 20, start_x + step_x * i - 10, start_y + step_y * j + 50, start_x + step_x * i, start_y + step_y * j, i * 4 + j, start_x + step_x * i - 30, start_y + step_y * j, i * 4 + j);
            printf("%s", buffer);
        }
    }
    return 0;
}