/*
 * reset.c - 将 A-K 每题 cfg.txt 第四行的最大通过测试点数清零，
 * 前三行保持不变。
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

/* 将 cfg.txt 第四行改写为 0，其余内容原样保留 */
static int reset_cfg(const char *path)
{
    char *buf;
    long len;
    long p, line;
    long line4_start, after;
    long newlen, q;
    char *newbuf;
    FILE *fp;
    int need_nl;

    buf = read_file(path, &len);
    if (buf == NULL) return 0;

    p = 0;
    line = 1;
    while (p < len && line < 4) {
        if (buf[p] == '\n') line++;
        p++;
    }

    if (line < 4) {
        /* 没有第四行：在末尾追加一行 0 */
        need_nl = (len == 0 || buf[len - 1] != '\n') ? 1 : 0;
        newlen = len + (need_nl ? 1 : 0) + 2;
        newbuf = (char *)malloc((size_t)newlen + 1);
        if (newbuf == NULL) {
            free(buf);
            return 0;
        }

        memcpy(newbuf, buf, (size_t)len);
        q = len;
        if (need_nl) newbuf[q++] = '\n';
        newbuf[q++] = '0';
        newbuf[q++] = '\n';
        newbuf[q] = '\0';
    } else {
        /* 存在第四行：只替换第四行内容，前三行与第四行之后的内容原样保留 */
        line4_start = p;

        while (p < len && buf[p] != '\n') p++;
        after = p;
        if (after < len && buf[after] == '\n') after++;

        newlen = line4_start + 2 + (len - after);
        newbuf = (char *)malloc((size_t)newlen + 1);
        if (newbuf == NULL) {
            free(buf);
            return 0;
        }

        memcpy(newbuf, buf, (size_t)line4_start);
        q = line4_start;
        newbuf[q++] = '0';
        newbuf[q++] = '\n';
        memcpy(newbuf + q, buf + after, (size_t)(len - after));
        q += len - after;
        newbuf[q] = '\0';
    }

    fp = fopen(path, "wb");
    if (fp == NULL) {
        free(newbuf);
        free(buf);
        return 0;
    }

    fwrite(newbuf, 1, (size_t)q, fp);
    fclose(fp);

    free(newbuf);
    free(buf);
    return 1;
}

int main(void)
{
    char letter;
    char path[300];
    int done = 0;

    for (letter = 'A'; letter <= 'K'; letter++) {
        sprintf(path, "./data/%c/cfg.txt", letter);

        if (reset_cfg(path)) {
            printf("%c: best cleared to 0\n", letter);
            done++;
        } else {
            printf("%c: cannot read %s, skipped\n", letter, path);
        }
    }

    printf("Done. %d problem(s) reset.\n", done);
    printf("Press Enter to close...");
    getchar();
    return 0;
}
