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
int con[30][30][30],T;
int f(int a,int b,int c)
{
   if(a<=0||b<=0||c<=0)return con[0][0][0]=1;
   if(a>25||b>25||c>25)return con[25][25][25]=f(25,25,25);
   if(con[a][b][c])return con[a][b][c];
   if(a<b&&b<c)return con[a][b][c]=f(a,b,c-1)+f(a,b-1,c-1)-f(a,b-1,c);
   return con[a][b][c]=f(a-1,b,c)+f(a-1,b-1,c)+f(a-1,b,c-1)-f(a-1,b-1,c-1);
}
int main()
{
   scanf("%d",&T);
   int a,b,c;
   while(T--)
   {
   	  scanf("%d%d%d",&a,&b,&c);
   	  printf("%d\n",f(a,b,c));
   }
   return 0;
}

