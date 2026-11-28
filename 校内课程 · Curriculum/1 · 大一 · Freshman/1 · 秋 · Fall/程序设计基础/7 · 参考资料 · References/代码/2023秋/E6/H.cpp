#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
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
int n;
double f(int x)
{
   return log10((double)x)*(double)x;
}
int main()
{
   scanf("%d",&n);
   int l=1,r=255431604;
   while(l<r)
   {
   	  int mid=(l+r+1)/2;
   	  if(f(mid)>n)r=mid-1;
   	  else l=mid;
   }
   printf("%d",l);
   return 0;
}

