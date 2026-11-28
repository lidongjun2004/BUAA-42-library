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
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
double abs(double a)
{
   if(a>=0)return a;
   else return -a;
}
double f(double x,double y1,double y2,double x0,double s1,double s2)
{
   double d1=sqrt(y1*y1+x*x);
   double d2=sqrt(y2*y2+(x0-x)*(x0-x));
   return s1*d1+s2*d2;
}
int main()
{
   double x1,y1,x2,y2,x0,s1,s2;
   scanf("%lf%lf%lf%lf%lf%lf",&x1,&y1,&x2,&y2,&s1,&s2);
   x0=x2-x1;
   double l=x1,r=x2,mid1,mid2;
   mid1=(2*l+r)/3;
   mid2=(l+2*r)/3;
   while(r-l>eps)
   {
   	  if(f(mid1-x1,y1,y2,x0,s1,s2)>f(mid2-x1,y1,y2,x0,s1,s2))l=mid1;
   	  else r=mid2;
   	  mid1=(l*2+r)/3;
   	  mid2=(l+r*2)/3;
   }
   printf("%.3lf %.3lf",l,f(l-x1,y1,y2,x0,s1,s2));
   return 0;
}

