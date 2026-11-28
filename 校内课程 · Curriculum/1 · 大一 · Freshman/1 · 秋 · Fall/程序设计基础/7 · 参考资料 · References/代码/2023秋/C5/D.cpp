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
double e(double a,double b)
{
   if(b>=a)return e(b,a);
   return sqrt(a*a-b*b)/a;
}
int main()
{
   double p1,p2,p3,p4,p5,p6,p7,p8;
   scanf("%lf%lf%lf%lf%lf%lf%lf%lf",&p1,&p2,&p3,&p4,&p5,&p6,&p7,&p8);
   printf("%.2lf %.2lf %.2lf %.2lf %.2lf",e(p1,p5),e(p3,p1),e(p7,p6),e(p2,p4),e(p8,p3));
   return 0;
}

