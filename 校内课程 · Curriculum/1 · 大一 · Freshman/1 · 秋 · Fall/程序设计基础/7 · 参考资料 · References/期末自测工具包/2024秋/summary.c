/*
 * summary.c - 汇总 A-K 各题得分并输出总分
 * 每题得分 = 最大通过测试点数 / 该题总测试点数 * 该题总分
 * A 题总分 10 分，B-K 每题 100 分，满分 1010 分
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *read_file(const char *path, long *out_len)
{
    FILE *fp;
    long len;
    size_t n;
    char *buf;

    fp = fopen(path, "rb");
    if (fp == NULL) return NULL;

    if (fseek(fp, 0, SEEK_END) != 0) {
        fclose(fp);
        return NULL;
    }
    len = ftell(fp);
    if (len < 0) {
        fclose(fp);
        return NULL;
    }
    if (fseek(fp, 0, SEEK_SET) != 0) {
        fclose(fp);
        return NULL;
    }

    buf = (char *)malloc((size_t)len + 1);
    if (buf == NULL) {
        fclose(fp);
        return NULL;
    }

    n = fread(buf, 1, (size_t)len, fp);
    fclose(fp);
    buf[n] = '\0';
    if (out_len != NULL) *out_len = (long)n;
    return buf;
}

/* 读取 cfg.txt 中的总测试点数与最大通过测试点数 */
static int read_cfg(const char *path, int *total, int *best)
{
    char *buf;
    long len;
    int r;
    int t, tl, ml, b;

    buf = read_file(path, &len);
    if (buf == NULL) return 0;

    t = 0;
    tl = 0;
    ml = 0;
    b = 0;
    r = sscanf(buf, "%d %d %d %d", &t, &tl, &ml, &b);
    free(buf);

    if (r < 1) return 0;
    if (r < 4) b = 0;

    *total = t;
    *best = b;
    return 1;
}

int main(void)
{
    char letter;
    char path[300];
    int total, best;
    int weight;
    double score, sum = 0.0;

    for (letter = 'A'; letter <= 'K'; letter++) {
        sprintf(path, "./data/%c/cfg.txt", letter);

        if (!read_cfg(path, &total, &best)) {
            printf("%c: missing config %s\n", letter, path);
            continue;
        }

        if (total <= 0) {
            printf("%c: invalid test count\n", letter);
            continue;
        }

        weight = (letter == 'A') ? 10 : 100;
        score = (double)best / (double)total * (double)weight;
        sum += score;

        printf("%c: %d / %d * %d = %.6f\n",
               letter, best, total, weight, score);
    }

    printf("Total: %.6f / 1010\n", sum);
    printf("Press Enter to close...");
    getchar();
    return 0;
}
