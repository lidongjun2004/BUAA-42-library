#include<stdio.h>
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
int f(int a)
{
   if(a>=0)return a;
   else return -a;
}
int main()
{
   int a,b,ans1=1,ans2=1;
   while(scanf("%d%d",&a,&b)!=EOF)
   {
   	  ans1=1;ans2=1;
	  for(int i=1;i<=b;i++)ans1*=a;
      for(int i=1;i<=a;i++)ans2*=b;
      printf("%d\n",f(ans1-ans2));
   }
   
   return 0;
}

