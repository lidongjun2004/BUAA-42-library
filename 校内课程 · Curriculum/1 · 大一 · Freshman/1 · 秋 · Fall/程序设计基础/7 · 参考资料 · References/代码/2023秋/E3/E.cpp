#include<stdio.h>
#include<math.h>
#include<string.h>
int scan(long long x)
{
   for(long long i=2;i<=1073741824;i*=2)
      if(x==i)return 1;
   return 0;
}
int main()
{
   int T;long long x,y;
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%lld",&x);
   	  y=2;
   	  if(x==1)printf("3\n");
   	  else if(x%2)printf("1\n");
   	  else if(scan(x))printf("%lld\n",x+1);
	  else
   	  {
		 int flag1=0,flag2=0;
		 while(1)
		 {
		 	flag1=0;flag2=0;
			if(x&y)flag1=1;
			if(x^y)flag2=1;
			if(flag1&&flag2)break;
			y*=2;
		 }
		 printf("%lld\n",y);
	  }
   }
   return 0;
}

