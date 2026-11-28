#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   int n;
   scanf("%d",&n);
   for(int i=1;i<=n;i++)
   {
   	  int sum=0,a;
   	  scanf("%d",&a);
   	  if(sum+a>=48)sum=48;
   	  else sum+=a;
   	  scanf("%d",&a);
   	  if(sum+a>=96)sum=96;
   	  else sum+=a;
   	  scanf("%d",&a);
   	  if(sum+a>=144)sum=144;
   	  else sum+=a;
   	  scanf("%d",&a);
   	  if(sum+a>=192)sum=192;
   	  else sum+=a;
   	  scanf("%d",&a);
   	  if(sum+a>=240)sum=240;
   	  else sum+=a;
   	  scanf("%d",&a);
   	  if(sum+a>=288)sum=288;
   	  else sum+=a;
   	  if(sum==288)printf("Sucess\n");
   	  else printf("Failure %d\n",288-sum);
   }
   return 0;
}

