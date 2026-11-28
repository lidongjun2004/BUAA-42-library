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
int abs(int a)
{
   if(a>=0)return a;
   else return -a;
}
void func(int n)
{
   if(n==2)
   {
   	  printf("00");
   	  return;
   }
   if(n==1)
   {
   	  printf("0");
   	  return;
   }
   if(n%2)
   {
   	  func((n-1)/2);
   	  printf("1");
   	  func((n-1)/2);
   }
   else
   {
   	  func(n/2-1);
   	  printf("1");
   	  func(n/2);
   }
}
int main()
{
   int n;
   scanf("%d",&n);
   if(n==1)
   {
   	  printf("1");
   	  return 0;
   }
   if(n==2)
   {
   	  printf("10");
   	  return 0;
   }
   printf("1");
   func(n-2);
   printf("1");
   return 0;
}

