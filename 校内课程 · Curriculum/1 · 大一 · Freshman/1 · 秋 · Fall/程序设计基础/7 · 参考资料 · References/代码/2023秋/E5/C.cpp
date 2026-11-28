#include<stdio.h>
#include<math.h>
#include<string.h>
#define eps 1e-7
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
double f(double x)
{
   return x*exp(x);
}
int main()
{
   double x;
   scanf("%lf",&x);
   double l=-1.0,r=10.0;
   double mid=(l+r)/2;
   while(r-l>eps)
   {
   	  if(f(mid)>x)r=mid;
   	  else l=mid;
   	  mid=(l+r)/2;
   }
   printf("%.6lf",l);
   return 0;
}

