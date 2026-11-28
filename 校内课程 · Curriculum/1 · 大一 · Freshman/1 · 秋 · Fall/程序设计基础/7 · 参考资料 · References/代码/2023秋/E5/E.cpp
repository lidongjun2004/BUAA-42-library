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
double abs(double a)
{
   if(a>=0)return a;
   else return -a;
}
double x[1005],avx,ua;
int main()
{
   int n;
   scanf("%d",&n);
   for(int i=1;i<=n;i++)
   {
   	  scanf("%lf",&x[i]);
   	  avx+=x[i];
   }
   avx/=n;
   for(int i=1;i<=n;i++)ua+=abs(avx-x[i])*abs(avx-x[i]);
   ua=sqrt(ua/(n*(n-1)));
   printf("%.6lf\n%.6lf",avx,ua);
   return 0;
}

