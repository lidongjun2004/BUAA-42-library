#include<stdio.h>
#include<math.h>
#include<string.h>
int a[7],b[7],c[7];
int main()
{
   long long A,B,C,a1,b1,c1;
   int flag=0,ans=0,num=0;
   scanf("%lld%lld%lld",&a1,&b1,&c1);
   for(int i=1;i<=6;i++)
   {
   	  a[i]=a1%10;a1/=10;
   	  if(a[i]>num)num=a[i];
   	  b[i]=b1%10;b1/=10;
	  if(b[i]>num)num=b[i];
   	  c[i]=c1%10;c1/=10;
   	  if(c[i]>num)num=c[i];
   }
   for(int i=num+1;i<=16;i++)
   {
   	  A=0;B=0;C=0;
   	  for(int j=6;j>0;j--)
   	  {
   	  	 
   	  	 A*=i;
   	  	 A+=a[j];
	  }
	  for(int j=6;j>0;j--)
   	  {
   	  	 B*=i;
		 B+=b[j];
   	  	 
	  }
	  for(int j=6;j>0;j--)
   	  {
   	  	 C*=i;
		 C+=c[j];
	  }
	  if(A*B==C)
	  {
	  	 ans=i;
		 break;
	  }
   }
   printf("%d",ans);
   return 0;
}

