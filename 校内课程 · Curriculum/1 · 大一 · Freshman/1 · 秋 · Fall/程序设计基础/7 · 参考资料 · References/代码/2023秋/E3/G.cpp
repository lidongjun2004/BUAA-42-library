#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   int n,m,num,ans,i;
   scanf("%d",&n);
   while(n--)
   {
   	  scanf("%d",&m);
   	  if(m%2)
	  {
	     ans=0;
   	     for(i=1;i<=m;i++)
   	     {
   	  	    scanf("%d",&num);
   	  	    ans=ans^num;
	     }
	     printf("Single Dog! %d\n",ans);
	  }
   	  else
   	  {
		 for(i=1;i<=m;i++)scanf("%d",&num);
		 printf("Congratulations!\n");
	  }
   } 
   return 0;
}

