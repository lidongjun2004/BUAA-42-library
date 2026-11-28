#include<stdio.h>
#include<math.h>
#include<string.h>
#define PI acos(-1)
double dist(double a1,double b1,double a2,double b2)
{
   return sqrt((a1-a2)*(a1-a2)+(b1-b2)*(b1-b2));
}
double helen(double x,double y,double z)
{
   double p=(x+y+z)/2;
   return sqrt(p*(p-x)*(p-y)*(p-z));
}
double gcd(double x,double y)
{
   if(y>=x)return gcd(y,x);
   if(x-y<=1e-6)return x;
   return gcd(y,fmod(x,y));
}
int main()
{
   double x1,y1,x2,y2,x3,y3;
   scanf("%lf%lf%lf%lf%lf%lf",&x1,&y1,&x2,&y2,&x3,&y3);
   double a,b,c,s,r,ans;
   a=dist(x1,y1,x2,y2);
   b=dist(x3,y3,x2,y2);
   c=dist(x1,y1,x3,y3);
   s=helen(a,b,c);
   r=a*b*c/(4*s);
   if(a>c)
   {
   	  double m=a;
   	  a=c;c=m;
   }
   if(b>c)
   {
   	  double m=b;
   	  b=c;c=m;
   }
   double A=asin(a/(2*r));
   double B=asin(b/(2*r));
   double D=gcd(A,B);
   ans=(2*PI/D)*r*sin(D);
   printf("%lf",ans);
   return 0;
}

