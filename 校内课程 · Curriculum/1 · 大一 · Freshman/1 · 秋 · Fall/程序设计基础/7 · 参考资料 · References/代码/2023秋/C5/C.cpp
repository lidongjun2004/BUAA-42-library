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
int abs(int a)
{
   if(a>=0)return a;
   else return -a;
}
int a,b;
int f(int x)
{
   int ans=a;
   ans=(ans%b+b)%b;
   ans*=x;
   ans=(ans%b+b)%b;
   ans*=x;
   ans=(ans%b+b)%b;
   ans+=x;
   ans=(ans%b+b)%b;
   return ans;
}
int main()
{
   scanf("%d%d",&a,&b);
   int x;
   while(scanf("%d",&x)!=EOF)printf("%d\n",f(f(f(x))));
   return 0;
}

