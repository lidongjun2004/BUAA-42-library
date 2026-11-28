#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
#define max(a,b) (a>b)?a:b
#define min(a,b) (a<b)?a:b
int gcd(int a,int b)
{
    if(b==0)return a;
    return gcd(b,a%b);
}
void swap(void *a,void *b,int data_type_size)
{
    unsigned char *p=(unsigned char *)a;
    unsigned char *q=(unsigned char *)b;
    unsigned char temp;
    while(data_type_size--)
    {
       temp=*p;
       *p=*q;
       *q=temp;
       p++;
       q++;
    }
}

int main()
{
    int x[10]={0,1,2,3,4,5,6,7,8,9},*p1;
    p1=x+2;
    int m=*(p1++);
    printf("%d %d",*(p1++),m);
    return 0;
}



