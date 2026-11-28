#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
int max(int a,int b)
{
   if(a>b)return a;
   return b;
}
int min(int a,int b)
{
   if(a<b)return a;
   return b;
}
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
void ExGCD(int a, int b, int *d, int *x, int *y)
{
    if(b == 0)
    {
        *d=a;
        *x=1;
		*y=0;
        return;
    }
    int dd, xx, yy;
    ExGCD(b,a%b,&dd,&xx,&yy);
    *d=dd;
    *x=yy;
    *y=xx-(a/b)*yy;
}
int main()
{
    int a, b, d, x, y;
    scanf("%d%d",&a,&b);
    ExGCD(a,b,&d,&x,&y);
    printf("%d = %d*(%d) + %d*(%d)",d,a,x,b,y);
    return 0;
}

