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
long long qpow(long long a, unsigned long long b, long long p)
{
	long long ans = 1;
	a = a % p;
	while (b)
	{
		if (b & 1)
			ans = (ans * a) % p;
		b >>= 1;
		a = a * a % p;
	}
	return ans;
}
int main()
{
   long long a,b,p;
   scanf("%lld%lld%lld",&a,&b,&p);
   printf("%lld",qpow(a,b,p));
   return 0;
}

