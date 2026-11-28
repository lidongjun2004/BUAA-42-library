#include<stdio.h>
#include<math.h>
#include<string.h>
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
void swap(int a,int b)
{
   int t=a;
   a=b;
   b=t;
}
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
int main()
{
   int a,b,m,n;
   scanf("%d%d",&a,&b);
   while(a%b!=0)
   {
   	  printf("%d ",a/b);
   	  m=a;n=b;
   	  a=n;b=m%n;
   }
   printf("%d",a);
   return 0;
}

