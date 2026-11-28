#include<stdio.h>
#include<math.h>
#include<string.h>
int a[32];
int main()
{
   int n;
   while(scanf("%d",&n)!=EOF)
   {
   	  if(n==0)printf("00000000000000000000000000000000\n");
   	  else if(n>0)
   	  {
   	  	 printf("0");
   	  	 for(int i=31;i>=1;i--)
   	  	 {
   	  	 	a[i]=n&1;
   	  	 	n=n>>1;
		 }
		 for(int i=1;i<=31;i++)printf("%d",a[i]);
		 printf("\n");
	  }
	  else
	  {
	  	 printf("1");
	  	 for(int i=31;i>=1;i--)
   	  	 {
   	  	 	a[i]=n&1;
   	  	 	n=n>>1;
		 }
		 for(int i=1;i<=31;i++)printf("%d",a[i]);
		 printf("\n");
	  }
   }
   return 0;
}

