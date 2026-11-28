#include<stdio.h>
#include<math.h>
#include<string.h>
#define MOD 1000000007
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
long long jie(long long n)
{
   long long ans=1;
   while(n)
   {
   	  ans*=n;
   	  n--;
   	  ans=ans%MOD;
   }
   return ans;
}
int main()
{
   long long n;
   while(scanf("%lld",&n)!=EOF)printf("%lld\n",jie(jie(n)));
   return 0;
}

