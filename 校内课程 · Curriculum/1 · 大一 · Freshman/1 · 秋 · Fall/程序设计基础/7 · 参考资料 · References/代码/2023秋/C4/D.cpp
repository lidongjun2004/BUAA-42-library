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
int num[6];
int main()
{
   int a,b,sum=0;
   while(scanf("%d%d",&a,&b)!=EOF)
   {
   	  num[a]+=b;sum++;
   	  if(num[a]==9)
   	  {
   	  	 printf("%d %d\n",sum,a);
   	  	 num[a]=0;
	  }
   }
   return 0;
}

