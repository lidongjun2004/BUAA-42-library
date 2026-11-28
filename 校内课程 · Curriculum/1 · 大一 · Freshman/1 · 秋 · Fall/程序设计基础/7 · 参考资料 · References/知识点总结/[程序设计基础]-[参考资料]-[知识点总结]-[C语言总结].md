# C语言总结

## 原码，补码和反码

### 一、原码 补码 反码的基本概念

1. 原码:就是符号位加上真值的绝对值
2. 反码:正数的反码是其本身,负数的反码是其原码符号位不变,其余位取反
3. 补码:正数的补码是其本身,负数的补码是其反码加1（保留符号位，其他位+1）
4. 注意：计算机内数值以补码进行存储

### 二、原理解析

结论：~的结果为其本身正负变号，然后-1（符号变号，大小-1）
（~按位取反，符号位也需要取反，即0–1,1–0）
计算机输入数值保存过程
输入数->转为二进制补码保存在计算机中
按位取反（~）过程
对计算机内保存的补码进行按位取反->求得按位取反数值的补码->求其反码->求其原码

原理：按位取反的计算
正整数取反： 例如 1 (1字节8位数)

原码： 0000 0001
-> 补码：0000 0001
-> 取反：1111 1110
(此时为负数，计算机内数值以补码保存，会认为这是一个负数的补码，负数原码和补码不同需要转变为反码，再转变为原码 ）
-> 补码+（-1）转变为其反码：1111 1101
->反码除符号位按位取反得到其原码1000 0010 即 -2；
所以输出-2

负整数的取反过程： 例如 -1 （1字节8位数）
原码： 1000 0001 (以补码形式存储，负数应该先求补码）
-> 反码：1111 1110
->补码：1111 1111（计算机以补码保存）
->取反：0000 0000 即 0（正数的原码反码补码相同）；
所以输出为0

## 初始模板

```c
#include<stdio.h>
#include<math.h>
#include<ctype.h>
#include<stdlib.h>
#include<string.h>
#include<assert.h>
#include<limits.h>
#include<time.h>
#include<malloc.h>
#define f1(a,s,e,d) for(int a = s;a <= e;a += d)
#define f2(a,s,e,d) for(int a = s;a >= e;a -= d)
#define LL long long
#define db double

int main()
{



 return 0;
}
```

## 快速读入

```c
int read()
{ 
 int p = 0,k = 1;;
 char c = getchar();
 while(c < '0' || c > '9') 
    { 
  if(c == '-') k = -1;
  c = getchar();
 }
 while(c >= '0' && c <= '9') 
    {
  p = p * 10 + c - '0';
  c = getchar();
 }
    return x * k;
}

```

## 欧拉素数筛

```c
int a[N];
void prime()
{
 a[1]=1;
 for(int i = 2;i <= sqrt(n);i ++)
 {   
  if(a[i] == 0)
  {
   for(int j = i;j * i <= n;j ++)
    a[i * j] = 1;
  }
  
 }
}
```

## swap函数

```c
void swap(int *p1,int *p2)
{
    int temp;
    temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}
```

## Zellar公式

```c
int zellar(int y,int m,int d)
{
    
    if(m == 1) m = 13,y --;
    if(m == 2) m = 14,y --;
    int c = y / 100;
    y = y % 100;
    return (y + y / 4 + c / 4 - 2 * c + (26 * (m + 1)) / 10 + d - 1) % 7;//星期日-0 星期一-1，以此类推
}
```

## memcpy和memset函数

```c
//第一个参数是清空对象
//第二个参数是对每个字节初始化的大小
//第三个是从开始初始化多少个字节
memset(a,0x3f,sizeof(a));//极大值初始化
memset(a,0,sizeof(a));//初始化为0
memset(a,'A',6);//字符的初始化
//将a中的字节（个数为sizeof（a）复制到b中）
memcpy(a,0x3f,sizeof(a));
```

## sort函数

```c
#include <stdio.h>
#include <stdlib.h>
 
int compar(const void *e1, const void *e2){
    return (*(int *)e1 - *(int *)e2);
}
int cmp(const void *e1, const void *e2){
   return (int)(*(float*)e1 - *(float*)e2);
}//浮点
int cmp(const void *e1, const void *e2){
    return strcmp((char*)e1,(char*)e2);
}//字符串
int cmp(const void *e1, const void *e2){
    return strlen((char*)e1) - strlen((char*)e2);
}//字符长度
int cmp(const void *e1, const void *e2){
    return (int)(((stu*)e1)->weight - ((stu*)e2)->weight);
}//结构体变量
int main()
{
    int arr[5] = {5, 2, 1, 4, 3};
    qsort(arr, 5, sizeof(arr[0]), compar);
    for (int i = 0; i < 5; i++){
        printf("%d ", arr[i]);
    }
    return 0;
}
```

## 快排（手写版）

```c
const int N = 1e6 + 10;
int n,a[N];
void swap(int *p1,int *p2)
{
    int temp;
    temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}
void qs(int l,int r)
{
 if(l == r) return ;
 int mid = a[(l + r) / 2];
 int i = l,j = r;
 do{
  while(a[i] < mid) i ++;
  while(a[j] > mid) j --;
  if(i <= j)
  {
   swap(&a[i],&a[j]);
   i ++;
   j --;
  }
 }while(i <= j);
 if(l < j) qs(l,j);
 if(i < r) qs(i,r);
 return ;
}
int main()
{
 scanf("%d",&n);
 for(int i = 1;i <= n;++ i) scanf("%d",&a[i]);
 qs(1,n);
 for(int i = 1;i <= n;++ i) printf("%d ",a[i]);
 return 0;
}
```

## 二分

```c
int lower_bound(int l0,int r0)
{
    int l = l0,r = r0,mid;
    while(l < r)
    {
        mid = (l + r) >> 1;
        if(!check(mid)) l = mid + 1;
        else r = mid; 
    }
 return l;
}
int upper_bound(int l0,int r0)
{
    int l = l0,r = r0,mid;
    while(l < r)
    {
        mid = (l + r + 1) >> 1;
        if(check(mid)) l = mid;
        else r = mid - 1; 
    }
 return l;
}
```

## gcd(最小公约数)

```c
int gcd(int a,int b)
{
    return a % b ? gcd(b,a % b) : b;
}
```

## 字符串排序

```c
#include<stdio.h>
#include<math.h>
#include<ctype.h>
#include<stdlib.h>
#include<string.h>
#include<assert.h>
#include<limits.h>
#include<time.h>
#include<malloc.h>
#define f1(a,s,e,d) for(int a = s;a <= e;a += d)
#define f2(a,s,e,d) for(int a = s;a >= e;a -= d)
#define db double
const int N = 200;

struct str{

    char s[200];
    int len;

}data[100];

int cmp_str(const void *a,const void *b)
{
    const struct str *p1 = (struct str *)a,*p2 = (struct str *)b;
    if(p1->len < p2->len) return -1;
    if(p1->len > p2->len) return 1;
    if(strcmp(p1->s,p2->s) == 1) return 1;
    return -1;
}


int main()
{
    // freopen("qsort.in","r",stdin);
    int n;
    scanf("%d",&n);
    f1(i,1,n,1)
    {
        scanf("%s",data[i].s);
        data[i].len = strlen(data[i].s);
    }
    qsort(data + 1,n,sizeof(data[1]),cmp_str);
    f1(i,1,n,1)
    {
        printf("%s\n",data[i].s);
    }
}
/*cmp函数返回1，说明第一个在第二个后面，-1说明在前面*/
```

## 矩阵乘法

### 基本版本

```c
void mat_multi(const db (*a)[N],const db (*b)[N],db (*c)[N])
{
    f1(i,1,n,1)
    {
        f1(j,1,n,1)
        {
            f1(k,1,n,1)
                c[i][j] += a[i][k] * b[k][j];
        }
    }
}
```

### 复数版本

```c
typedef struct _cplx{
 int R, I;
} cplx;
typedef struct _Matrix{
 int row, col;
 cplx a[10][10];
} Matrix;
cplx multi(cplx A,cplx B)
{
 cplx ans;
 ans.R = A.R * B.R - A.I * B.I;
 ans.I = A.I * B.R + B.I * A.R;
 return ans;
}
cplx add(cplx A,cplx B)
{
 cplx ans;
 ans.R = A.R + B.R;
 ans.I = A.I + B.I;
 return ans;
}
void clear(Matrix * A)
{
 f1(i,1,7,1)
  f1(j,1,7,1)
  {
   A->a[i][j].I = 0;
   A->a[i][j].R = 0;
  }
}
Matrix prod(Matrix A, Matrix B)
{
 Matrix ans;
 ans.row = A.row;
 ans.col = B.col;
 clear(&ans);
 f1(i,1,A.row,1)
 {
  f1(j,1,B.col,1)
  {
   f1(k,1,A.col,1)
   {
    ans.a[i][j] = add(ans.a[i][j],multi(A.a[i][k],B.a[k][j]));
   }
  }
 }
 return ans;
}
```

## 余子式(三阶版本)

```c
void change(LL x)
{
 LL ii = 0,jj = 0;
 for(LL i = 1;i <= 4;++ i)
 { 
  if(i != b[x][0])
  {
   ii ++;
   jj = 0;
   for(LL j = 1;j <= 4;++ j)
   {
    if(j != b[x][1])
    {
     jj ++;
     c[ii][jj] = a[i][j];
    }
   } 
  }
 }
}//转换余子式矩阵
void put()
{
 LL ans = 0;
 ans = (c[1][1] * c[2][2] * c[3][3] + c[1][2] * c[2][3] * c[3][1]+c[1][3] * c[2][1] * c[3][2]);
 ans -= (c[1][3] * c[2][2] * c[3][1] + c[1][2] * c[2][1] * c[3][3]+c[1][1] * c[2][3] * c[3][2]);
 printf("%lld\n",ans);
}//计算余子式
```

## 冒泡排序

```c
for(int i = 1;i <= K;++ i)
 {
  for(int j = 1;j <= n - i;++ j)
  {
   if(a[j] < a[j + 1]) swap(&a[j],&a[j + 1]);
  }
  printf("%d ",a[n - i + 1]);
 }
```

## Exgcd

```c
void Exgcd(int a,int b)
{
    if(!b) 
 {
  d =a;x = 1;y = 0;
  return ;
 }
 else
 {
  Exgcd(b,a % b);
  int temp = x;
  x = y;
  y = temp - (a / b) * y;
  return ;
 }
}
int main()
{
 Exgcd(a,b);
 printf("%d = %d*(%d) + %d*(%d)",d,a,x,b,y);
 return 0;
}
```

## 字符串

```c

char a[100100];
char s[100100];
char temp[100100],temp2[100100];

int main()
{   
    scanf("%s",a);
    int opt;
    int lena = strlen(a);
    while(scanf("%d",&opt) && opt != -1)
    {
        if(opt == 1)
        {
            scanf("%s",s);
            strcat(a,s);
            
            int lenb = strlen(s);
            for(int i = lena;i < lena + lenb;++ i)
                a[i] = s[i - lena];
                lena += lenb;
    //             for(int k = 0;k < lena;++ k)
    // printf("%c",a[k]);
    // printf("\n");
        }
        else if(opt == 2)
        {
            int i;
            scanf("%d",&i);
            lena = i;
    //         for(int k = 0;k < lena;++ k)
    // printf("%c",a[k]);
    // printf("\n");
        }
        else if(opt == 3)
        {
            int i;
            scanf("%d %s",&i,s);

            int lenb = strlen(s);
            for(int j = lena;j >= i;-- j) a[j + lenb] = a[j];
            for(int j = 0;j < lenb;++ j) a[j + i] = s[j];
            lena += lenb;
    //         for(int k = 0;k < lena;++ k)
    // printf("%c",a[k]);
    // printf("\n");
        }
        else if(opt == 4)
        {
            int i,j;
            scanf("%d%d",&i,&j);
            for(int k = i;k + (j - i) + 1 < lena;++ k)
            {
                a[k] = a[k + (j - i) + 1];
            }
            lena -= (j - i + 1);
    //         for(int k = 0;k < lena;++ k)
    // printf("%c",a[k]);
    // printf("\n");
            // strcpy(temp,a + j);
            // strncpy(temp2,a,i);
            // strcpy(a,temp2);
            // strcat(a,temp);
            //  printf("%d:%s\n",opt,a);
        }
        else
        {
            int i;
            scanf("%d %s",&i,s);
            int lenb = strlen(s);
            for(int j = 0;j < lenb;++ j)
                a[i + j] = s[j];
            lena = fmax(i + lenb,lena);
    //         for(int k = 0;k < lena;++ k)
    // printf("%c",a[k]);
    // printf("\n");
            // memcpy(a + i,s,strlen(s));
            //  printf("%d:%s\n",opt,a);
        }
    }
    scanf("%s",s);
    char *p = strstr(a,s);
    int ans=  0;
    while(p != NULL && (p - a) <= lena)
    {
        ans ++;
        p = strstr(a + (p - a) + 1,s);
    }
    printf("%d\n",ans);
    for(int i = 0;i < lena;++ i)
    printf("%c",a[i]);
 return 0;
}
```

## 会错掉的地方

### 没考虑特殊情况

### 数据类型错误

```unsigned long long```的占位符为 ```%llu```。

```1```的 ```unsigned long long``` 形式为 ```1ull```，如果你要把 ```1``` 左移超过 ```32```位，最好考虑把``` 1 ```修改为 ```1ull```

### 打印方式

```%2d```，表示打印该数字的时候打印两位，不够两位用空格补上，右对齐；
```%-2d```，表示打印该数字的时候打印两位，不够两位用空格补上，左对齐；

制表符 ```\t```

```c
unsigned char %hhd
```

### 负数取模

$a < 0$的情况下，答案 $=(a \mod b + b) \mod b$

### 四舍五入

## 指针

```c
int a[10];
int (*p)[20] = &a;//指向整个数组首地址的指针，p+1指向越过整个a数组的下一个地址
int *p2 = a;//指向a数组首地址的指针，p2 + x指向a[x]

```

## str函数

1. memcpy
    void *memcpy(void*dest, const void *src, size_t n);
    功能：从源src所指的内存地址的起始位置开始拷贝n个字节到目标dest所指的内存地址的起始位置中
    返回：函数返回指向dest的指针
2. strcat
    char *strcat(char*dest,char *src);
    功能：把src所指字符串添加到dest结尾处(覆盖dest结尾处的’\0’)并添加’\0’。
3. strncat
    char *strncat(char* s1,const char * s2.size_t n);
    功能：把src所指字符串的前n个字符添加接功能到dest结尾处（覆盖dest结尾处接功能的’\0’）并添加’\0’。
4. strcpy
    char strcpy(char dest, const char *src);
    功能：把从src地址开始且含有NULL结束符的字符串复制到以dest开始的地址空间
    说明：src和dest所指内存区域不可以重叠且dest必须有足够的空间来容纳src的字符串。返回指向dest的指针。
