/*
 * 简易 C89 跨平台评测器
 * 数据目录：./data/A/ ... ./data/K/
 * 数据文件：data1.in / data1.out ...
 * 配置：cfg.txt
 *   第 1 行：测试点数量
 *   第 2 行：时间限制，毫秒
 *   第 3 行：空间限制，KB
 *   第 4 行：历史最多通过测试点数
 * 学生文件：student.c
 */

/*
 * 在 POSIX 平台下启用 BSD/POSIX 扩展函数声明（wait4、gettimeofday 等），
 * 同时仍然保持 C89 的语言语法。
 */
#ifndef _WIN32
#ifndef _DEFAULT_SOURCE
#define _DEFAULT_SOURCE
#endif
#ifndef _POSIX_C_SOURCE
#define _POSIX_C_SOURCE 200809L
#endif
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#ifdef _WIN32

#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0500
#endif

#include <windows.h>
#define EXE_NAME "student.exe"

#ifndef JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION
#define JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION 0x00000400
#endif

#else

#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/select.h>
#include <signal.h>
#include <fcntl.h>
#include <errno.h>
#define EXE_NAME "student"

#endif

/* 评测结果 */
#define R_AC      0
#define R_PE      1
#define R_WA      2
#define R_OK      3
#define R_TLE     4
#define R_MLE     5
#define R_SEGV    6
#define R_FPE     7
#define R_ABRT    8
#define R_OTHER   9

static const char *result_name(int r)
{
    switch (r) {
    case R_AC:    return "Accepted";
    case R_PE:    return "Presentation Error";
    case R_WA:    return "Wrong Answer";
    case R_TLE:   return "Time Limit Exceed";
    case R_MLE:   return "Memory Limit Exceed";
    case R_SEGV:  return "Runtime Error (SIGSEGV)";
    case R_FPE:   return "Runtime Error (SIGFPE)";
    case R_ABRT:  return "Runtime Error (SIGABRT)";
    default:      return "Other Error";
    }
}

static int file_exists(const char *path)
{
    FILE *fp;
    fp = fopen(path, "rb");
    if (fp != NULL) {
        fclose(fp);
        return 1;
    }
    return 0;
}

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

/*
 * 规范化：
 * 1. 删除每行行尾空格、制表符、\r
 * 2. 删除文件末尾空行
 */
static char *normalize_text(const char *s, long len)
{
    char *d;
    long i, j, start, end, k;

    d = (char *)malloc((size_t)len + 2);
    if (d == NULL) return NULL;

    i = 0;
    j = 0;

    while (i < len) {
        start = i;
        while (i < len && s[i] != '\n') i++;
        end = i;

        while (end > start &&
               (s[end - 1] == ' ' || s[end - 1] == '\t' || s[end - 1] == '\r')) {
            end--;
        }

        for (k = start; k < end; k++) d[j++] = s[k];

        if (i < len && s[i] == '\n') {
            d[j++] = '\n';
            i++;
        }
    }

    while (j > 0 &&
           (d[j - 1] == '\n' || d[j - 1] == ' ' ||
            d[j - 1] == '\t' || d[j - 1] == '\r')) {
        j--;
    }

    d[j] = '\0';
    return d;
}

/* 删除所有空白字符，用于判断 Presentation Error */
static char *strip_all_space(const char *s, long len)
{
    char *d;
    long i, j;

    d = (char *)malloc((size_t)len + 1);
    if (d == NULL) return NULL;

    j = 0;
    for (i = 0; i < len; i++) {
        if (!isspace((unsigned char)s[i])) {
            d[j++] = s[i];
        }
    }
    d[j] = '\0';
    return d;
}

static int compare_files(const char *output_path, const char *answer_path)
{
    long olen, alen;
    char *outbuf, *ansbuf;
    char *outnorm, *ansnorm;
    char *outsp, *anssp;
    int result;

    outbuf = read_file(output_path, &olen);
    if (outbuf == NULL) return R_WA;

    ansbuf = read_file(answer_path, &alen);
    if (ansbuf == NULL) {
        free(outbuf);
        return R_WA;
    }

    outnorm = normalize_text(outbuf, olen);
    ansnorm = normalize_text(ansbuf, alen);

    if (outnorm == NULL || ansnorm == NULL) {
        free(outbuf);
        free(ansbuf);
        free(outnorm);
        free(ansnorm);
        return R_OTHER;
    }

    if (strcmp(outnorm, ansnorm) == 0) {
        result = R_AC;
    } else {
        outsp = strip_all_space(outbuf, olen);
        anssp = strip_all_space(ansbuf, alen);

        for ( char *tmp = outsp; tmp != NULL && *tmp != '\0'; tmp++ )
            *tmp = tolower(*tmp);
        for ( char *tmp = anssp; tmp != NULL && *tmp != '\0'; tmp++ )
            *tmp = tolower(*tmp);
        

        if (outsp != NULL && anssp != NULL && strcmp(outsp, anssp) == 0)
            result = R_PE;
        else
            result = R_WA;

        free(outsp);
        free(anssp);
    }

    free(outbuf);
    free(ansbuf);
    free(outnorm);
    free(ansnorm);

    return result;
}

static int read_cfg(const char *path, int *n, int *time_limit,
                    int *mem_limit, int *best)
{
    char *buf;
    long len;
    int r;

    buf = read_file(path, &len);
    if (buf == NULL) return 0;

    r = sscanf(buf, "%d %d %d %d", n, time_limit, mem_limit, best);
    free(buf);

    if (r < 3) return 0;
    if (r < 4) *best = 0;
    return 1;
}

/*
 * 更新 cfg.txt 第四行。
 * 前三行原样保留。
 */
static int update_cfg(const char *path, int new_best)
{
    char *buf;
    long len;
    long p;
    int line;
    long line4_start;
    long after;
    char num[32];
    long num_len;
    char *newbuf;
    long newlen;
    long q;
    FILE *fp;

    buf = read_file(path, &len);
    if (buf == NULL) return 0;

    p = 0;
    line = 1;

    /* 定位第四行行首 */
    while (p < len && line < 4) {
        if (buf[p] == '\n') line++;
        p++;
    }
    line4_start = p;

    /* 定位第四行行尾 */
    while (p < len && buf[p] != '\n') p++;
    after = p;
    if (after < len && buf[after] == '\n') after++;

    sprintf(num, "%d", new_best);
    num_len = (long)strlen(num);

    newlen = line4_start + num_len + 1 + (len - after);
    newbuf = (char *)malloc((size_t)newlen + 1);
    if (newbuf == NULL) {
        free(buf);
        return 0;
    }

    memcpy(newbuf, buf, (size_t)line4_start);

    q = line4_start;
    memcpy(newbuf + q, num, (size_t)num_len);
    q += num_len;
    newbuf[q++] = '\n';

    memcpy(newbuf + q, buf + after, (size_t)(len - after));
    q += len - after;
    newbuf[q] = '\0';

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

/* 判断编译器是否可用 */
static int command_exists(const char *cmd)
{
    char probe[512];

#ifdef _WIN32
    sprintf(probe, "where %s >nul 2>nul", cmd);
#else
    sprintf(probe, "command -v %s >/dev/null 2>&1", cmd);
#endif

    return system(probe) == 0;
}

static int compile_student(char **log_out, long *log_len)
{
    const char *compilers[4];
    char cmd[512];
    int i;

    *log_out = NULL;
    *log_len = 0;

    remove(EXE_NAME);
    remove("compile.log");

#ifdef _WIN32
    compilers[0] = "gcc";
    compilers[1] = "clang";
    compilers[2] = "cl";
    compilers[3] = "tcc";
#else
    compilers[0] = "cc";
    compilers[1] = "gcc";
    compilers[2] = "clang";
    compilers[3] = "tcc";
#endif

    for (i = 0; i < 4; i++) {
        if (!command_exists(compilers[i])) {
            /* 编译器不存在时不要覆盖有用的编译错误信息 */
            continue;
        }

#ifdef _WIN32
        if (strcmp(compilers[i], "cl") == 0) {
            sprintf(cmd, "%s student.c /Fe:%s /O2 > compile.log 2>&1",
                    compilers[i], EXE_NAME);
        } else {
            sprintf(cmd, "%s student.c -o %s -O2 -std=c99 > compile.log 2>&1",
                    compilers[i], EXE_NAME);
        }
#else
        sprintf(cmd, "%s student.c -o %s -O2 -std=c99 > compile.log 2>&1",
                compilers[i], EXE_NAME);
#endif

        system(cmd);

        if (file_exists(EXE_NAME)) {
            remove("compile.log");
            return 1;
        }

        if (*log_out == NULL) {
            /* 保留第一个真实编译器的报错信息 */
            *log_out = read_file("compile.log", log_len);
        }
    }

    return 0;
}

#ifdef _WIN32

static int run_program(const char *input_path, const char *output_path,
                       int time_limit, int mem_limit,
                       long *time_ms, long *mem_kb)
{
    HANDLE hIn, hOut, hNul, hJob;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    DWORD wait_result, start, end, exit_code;
    char cmd[256];
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION jeli;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION qjeli;
    SECURITY_ATTRIBUTES sa;
    int result;

    *time_ms = 0;
    *mem_kb = 0;

    /*
     * 注意：lpSecurityAttributes 为 NULL 时，CreateFileA 返回的句柄
     * 不可被子进程继承，导致子进程的 stdin/stdout/stderr 失效，
     * 程序会卡在读取输入上而被误判为 TLE。
     * 必须显式设置 bInheritHandle = TRUE。
     */
    sa.nLength = sizeof(sa);
    sa.lpSecurityDescriptor = NULL;
    sa.bInheritHandle = TRUE;

    hIn = CreateFileA(input_path, GENERIC_READ, FILE_SHARE_READ, &sa,
                      OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hIn == INVALID_HANDLE_VALUE) return R_OTHER;

    hOut = CreateFileA(output_path, GENERIC_WRITE, FILE_SHARE_READ, &sa,
                       CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hOut == INVALID_HANDLE_VALUE) {
        CloseHandle(hIn);
        return R_OTHER;
    }

    hNul = CreateFileA("NUL", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE,
                       &sa, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hNul == INVALID_HANDLE_VALUE) {
        CloseHandle(hIn);
        CloseHandle(hOut);
        return R_OTHER;
    }

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = hIn;
    si.hStdOutput = hOut;
    si.hStdError = hNul;

    ZeroMemory(&pi, sizeof(pi));
    strcpy(cmd, EXE_NAME);

    if (!CreateProcessA(NULL, cmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(hIn);
        CloseHandle(hOut);
        CloseHandle(hNul);
        return R_OTHER;
    }

    /*
     * 总是创建 Job Object：通过 JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION
     * 让子进程发生未处理异常时立即终止，避免 Windows Error Reporting
     * 弹窗/收集信息导致进程迟迟不退出而被误判为 TLE。
     * 这里不设置工作集硬限制，否则会干扰峰值内存测量并可能造成页面抖动，
     * 内存超限改为在进程结束后通过峰值工作集判断。
     */
    hJob = CreateJobObjectA(NULL, NULL);
    if (hJob != NULL) {
        ZeroMemory(&jeli, sizeof(jeli));
        jeli.BasicLimitInformation.LimitFlags =
            JOB_OBJECT_LIMIT_DIE_ON_UNHANDLED_EXCEPTION;

        SetInformationJobObject(hJob, JobObjectExtendedLimitInformation,
                                &jeli, sizeof(jeli));
        AssignProcessToJobObject(hJob, pi.hProcess);
    }

    start = GetTickCount();
    wait_result = WaitForSingleObject(pi.hProcess, (DWORD)time_limit);
    end = GetTickCount();
    *time_ms = (long)(end - start);

    if (wait_result == WAIT_TIMEOUT) {
        TerminateProcess(pi.hProcess, 1);
        WaitForSingleObject(pi.hProcess, INFINITE);
        result = R_TLE;
    } else {
        GetExitCodeProcess(pi.hProcess, &exit_code);

        if (exit_code == 0) {
            result = R_OK;
        } else if (exit_code == 0xC0000017UL) {
            /* STATUS_NO_MEMORY，作为内存超限的兜底判断 */
            result = R_MLE;
        } else if (exit_code == 0xC0000005UL) {
            result = R_SEGV;
        } else if (exit_code == 0xC0000094UL) {
            result = R_FPE;
        } else if (exit_code == 0xC0000409UL ||
                   exit_code == 0xC000001DUL ||
                   exit_code == 0xC00000FDUL) {
            result = R_ABRT;
        } else {
            result = R_OTHER;
        }
    }

    /*
     * 测量子进程峰值内存（工作集）。子进程终止后只要 Job 句柄仍有效，
     * 即可查询到峰值数据。
     */
    if (hJob != NULL) {
        ZeroMemory(&qjeli, sizeof(qjeli));
        if (QueryInformationJobObject(hJob, JobObjectExtendedLimitInformation,
                                      &qjeli, sizeof(qjeli), NULL)) {
            *mem_kb = (long)(qjeli.PeakProcessMemoryUsed / 1024);
        }
    }

    if (result != R_TLE && mem_limit > 0 && *mem_kb > (long)mem_limit) {
        result = R_MLE;
    }

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    if (hJob != NULL) CloseHandle(hJob);
    CloseHandle(hIn);
    CloseHandle(hOut);
    CloseHandle(hNul);

    return result;
}

#else

static long now_ms(void)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (long)tv.tv_sec * 1000L + (long)tv.tv_usec / 1000L;
}

static void sleep_ms(int ms)
{
    struct timeval tv;
    tv.tv_sec = ms / 1000;
    tv.tv_usec = (ms % 1000) * 1000;
    select(0, NULL, NULL, NULL, &tv);
}

static int run_program(const char *input_path, const char *output_path,
                       int time_limit, int mem_limit,
                       long *time_ms, long *mem_kb)
{
    pid_t pid;
    pid_t w;
    int status;
    struct rusage ru;
    long start, elapsed, mem;
    int in_fd, out_fd, nul_fd;
    int result;

    *time_ms = 0;
    *mem_kb = 0;

    pid = fork();
    if (pid < 0) return R_OTHER;

    if (pid == 0) {
        in_fd = open(input_path, O_RDONLY);
        if (in_fd < 0) _exit(127);

        out_fd = open(output_path, O_WRONLY | O_CREAT | O_TRUNC, 0666);
        if (out_fd < 0) _exit(127);

        nul_fd = open("/dev/null", O_WRONLY);
        if (nul_fd < 0) _exit(127);

        dup2(in_fd, 0);
        dup2(out_fd, 1);
        dup2(nul_fd, 2);

        close(in_fd);
        close(out_fd);
        close(nul_fd);

        /*
         * 不设置 RLIMIT_AS 硬限制：过小的虚拟地址空间限制会使程序
         * 在 exec 阶段就失败（即使实际内存远未超标）。内存超限改由
         * 父进程在程序结束后依据 ru_maxrss 峰值判断。
         */
        execl("./student", "student", (char *)NULL);
        _exit(127);
    }

    memset(&ru, 0, sizeof(ru));
    start = now_ms();

    while (1) {
        w = wait4(pid, &status, WNOHANG, &ru);
        if (w == pid) break;

        if (now_ms() - start > time_limit) {
            kill(pid, SIGKILL);
            wait4(pid, &status, 0, &ru);
            *time_ms = now_ms() - start;
            return R_TLE;
        }

        sleep_ms(10);
    }

    elapsed = now_ms() - start;
    *time_ms = elapsed;

    mem = (long)ru.ru_maxrss;
#ifdef __APPLE__
    mem /= 1024; /* macOS 的 ru_maxrss 单位是字节 */
#endif
    *mem_kb = mem;

    if (mem_limit > 0 && mem > (long)mem_limit) {
        return R_MLE;
    }

    if (WIFEXITED(status)) {
        if (WEXITSTATUS(status) == 0) return R_OK;
        return R_OTHER;
    }

    if (WIFSIGNALED(status)) {
        int sig = WTERMSIG(status);

        if (sig == SIGSEGV) return R_SEGV;
        if (sig == SIGFPE)  return R_FPE;
        if (sig == SIGABRT) return R_ABRT;
        return R_OTHER;
    }

    result = R_OTHER;
    return result;
}

#endif

/*
 * 定位某道题第 index 个测试点的数据文件。
 * 同时兼容 data1.in / data1.out 与 data01.in / data01.out 两种命名方式。
 */
static int pick_data_file(const char *data_dir, int index, const char *ext,
                          char *out_path)
{
    sprintf(out_path, "%sdata%d.%s", data_dir, index, ext);
    if (file_exists(out_path)) return 1;

    sprintf(out_path, "%sdata%02d.%s", data_dir, index, ext);
    if (file_exists(out_path)) return 1;

    return 0;
}

int main(void)
{
    char letter;
    char data_dir[256];
    char cfg_path[300];
    int n, time_limit, mem_limit, best;
    int i, pass_count;
    char input_path[512];
    char answer_path[512];
    char output_path[512];
    int run_result, final_result;
    long run_time, run_mem;
    char *compile_log;
    long compile_log_len;
    double score;

#ifdef _WIN32
    /* 抑制 Windows 错误弹窗，子进程会继承此设置，崩溃时立即退出 */
    SetErrorMode(SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX |
                 SEM_NOOPENFILEERRORBOX);
#endif

    printf("Enter problem letter (A-K): ");
    if (scanf(" %c", &letter) != 1) return 1;
    while ( getchar() != '\n' );

    if (letter >= 'a' && letter <= 'z') {
        letter = (char)(letter - 'a' + 'A');
    }

    if (letter < 'A' || letter > 'K') {
        printf("Invalid input. Please enter a letter from A to K.\n");
        printf("Press Enter to close...");
        getchar();
        return 1;
    }

    sprintf(data_dir, "./data/%c/", letter);
    sprintf(cfg_path, "%scfg.txt", data_dir);

    if (!read_cfg(cfg_path, &n, &time_limit, &mem_limit, &best)) {
        printf("Unable to read configuration file: %s\n", cfg_path);
        printf("Press Enter to close...");
        getchar();
        return 1;
    }

    if (n <= 0) {
        printf("Invalid number of test cases.\n");
        printf("Press Enter to close...");
        getchar();
        return 1;
    }

    if (!file_exists("student.c")) {
        printf("Cannot find student.c under current directory.\n");
        printf("Press Enter to close...");
        getchar();
        return 0;
    }

    if (!compile_student(&compile_log, &compile_log_len)) {
        printf("Compile Error\n");
        if (compile_log != NULL && compile_log_len > 0) {
            printf("%s", compile_log);
        }
        free(compile_log);
        printf("Press Enter to close...");
        getchar();
        return 0;
    }

    printf("Compilation successful.\n");

    pass_count = 0;
    sprintf(output_path, "./student_output.tmp");

    for (i = 1; i <= n; i++) {
        if (!pick_data_file(data_dir, i, "in", input_path) ||
            !pick_data_file(data_dir, i, "out", answer_path)) {
            printf("Test case %d: %-30s\n", i, result_name(R_OTHER));
            continue;
        }

        remove(output_path);

        run_result = run_program(input_path, output_path,
                                 time_limit, mem_limit,
                                 &run_time, &run_mem);

        if (run_result == R_OK) {
            final_result = compare_files(output_path, answer_path);
        } else {
            final_result = run_result;
        }

        if (final_result == R_AC) {
            pass_count++;
        }

        printf("Test case %d: %-30s", i, result_name(final_result));

        if (run_result == R_OK ||
            run_result == R_TLE ||
            run_result == R_MLE ||
            run_result == R_SEGV ||
            run_result == R_FPE ||
            run_result == R_ABRT ||
            run_result == R_OTHER) {
            printf("  Time %ld ms", run_time);
            if (run_mem > 0) {
                printf("  Memory %ld KB", run_mem);
            }
        }

        printf("\n");
        remove(output_path);
    }

    score = (double)pass_count / (double)n;
    printf("Score: %.6f\n", score);

    if (pass_count > best) {
        update_cfg(cfg_path, pass_count);
    }

    free(compile_log);

    printf("Press Enter to close...");
    getchar();
    return 0;
}