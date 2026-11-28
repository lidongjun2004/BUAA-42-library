#include<stdio.h>
#include<math.h>
#include<string.h>
int a[3000005];
int main()
{
   int n,m,M=6,sign=0;
   long long sum=0;
   scanf("%d%d",&n,&m);
   n++;m++;
   for(int i=1;i<=n;i++)
   {
   	  scanf("%d",&a[i]);
   	  if(a[i]>M)
	  {
	     M=a[i];
	     sign=i;
	  }
   }
   a[sign]=6;
   for(int i=1;i<=m-1;i++)
   {
   	  M=6;sign=0;
	  for(int j=1;j<=n;j++)
	  {
	  	 if(a[j]>M)
	     {
	        M=a[j];
	        sign=j;
	     }
	  }
	  a[sign]=6;
   }
   for(int i=1;i<=n;i++)sum+=a[i];
   printf("%lld",sum);
   return 0;
}

