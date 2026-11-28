#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   int ans=0,x;
   for(int i=31;i>=0;i--)
   {
   	  scanf("%1u",&x);
   	  ans=ans|(x<<i);
   }
   printf("%d",ans);
   return 0;
}

