#include<stdio.h>
#include<math.h>
#include<string.h>
int mi(int i)
{
   int a=1;
   for(int j=1;j<=i;j++)a*=2;
   return a;
}
int main()
{
   int num,ans=0;
   for(int i=31;i>=0;i--)
   {
   	  scanf("%1u",&num);
   	  if(num)ans+=mi(i);
   }
   printf("%d",ans);
   return 0;
}

