#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   double r,x;
   scanf("%lf%lf",&r,&x);
   printf("%.1lf %.1lf",r*cos(x),r*sin(x));
   return 0;
}

