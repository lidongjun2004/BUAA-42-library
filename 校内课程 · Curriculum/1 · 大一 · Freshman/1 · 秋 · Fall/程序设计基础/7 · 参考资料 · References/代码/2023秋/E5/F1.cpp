#include<stdio.h>
#include<math.h>
#include<string.h>
#define eps 1e-4
double x1,y1,x2,y2,x0,s1,s2;
double f(double x)
{
   double d1=sqrt(y1*y1+x*x);
   double d2=sqrt(y2*y2+(x0-x)*(x0-x));
   return s1*d1+s2*d2;
}
int main()
{
   
   scanf("%lf%lf%lf%lf%lf%lf",&x1,&y1,&x2,&y2,&s1,&s2);
   x0=x2-x1;
   double l=x1,r=x2,mid1,mid2;
   mid1=(2*l+r)/3;
   mid2=(l+2*r)/3;
   while(r-l>eps)
   {
   	  if(f(mid1-x1)>f(mid2-x1))l=mid1;
   	  else r=mid2;
   	  mid1=(l*2+r)/3;
   	  mid2=(l+r*2)/3;
   }
   printf("%.3lf %.3lf",l,f(l-x1));
   return 0;
}

