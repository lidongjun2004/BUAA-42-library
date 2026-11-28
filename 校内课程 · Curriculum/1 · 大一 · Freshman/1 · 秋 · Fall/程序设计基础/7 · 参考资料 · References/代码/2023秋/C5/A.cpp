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
int main()
{
   double x;
   while(scanf("%lf",&x)!=EOF)
   {
   	  double y=exp(cos(atan(x)))/log(cosh(x)+1);
   	  printf("%.3lf\n",y);
   } 
   return 0;
}

