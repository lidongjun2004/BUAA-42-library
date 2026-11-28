#include<stdio.h>
#include<math.h>
#include<string.h>
double a[500005];
int n,m;
double sum[500005];
int check(double x)
{
   for(int i=1;i<=n;i++)sum[i]=sum[i-1]+a[i]-x;
   double inf=0;
   for(int i=m;i<=n;i++)
   {
   	  if(inf>sum[i-m])inf=sum[i-m];
   	  if(sum[i]-inf>=0)return 1;
   }
   return 0;
}
int main()
{
   scanf("%d%d",&n,&m);
   for(int i=1;i<=n;i++)scanf("%lf",&a[i]);
   double l=20,r=20000,mid;
   while(l!=r)
   {
   	  mid=(l+r+1)/2;
	  if(check(mid))l=mid;
	  else r=mid-1;
   }
   printf("%d",int(l+0.5));
   return 0;
}

