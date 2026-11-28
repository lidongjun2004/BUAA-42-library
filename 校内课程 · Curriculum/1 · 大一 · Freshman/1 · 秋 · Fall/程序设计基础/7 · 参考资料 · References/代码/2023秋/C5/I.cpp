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
int f[100000005];
int func(long long n)
{
   if(n==1)return 2;
   if(n%3==0)
   {
      if(n<100000005)
      {
      	 if(f[n])return f[n];
         f[n]=func(n/3)+1;
         return f[n];
	  }
	  return func(n/3)+1;
   }
   if(n<100000005)
   {
      if(f[n])return f[n];
      f[n]=func(n-1)+1;
      return f[n];
   }
   return func(n-1)+1;
}
int main()
{
   int T,ans=0;
   long long l,r;
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%lld%lld",&l,&r);
   	  ans=0;
   	  for(long long i=l;i<=r;i++)
   	  {
		 int fu;
		 if(i<100000005)
		 {
		    if(f[i])fu=f[i];
		    else
			{
			   fu=func(i);
			   f[i]=fu;
			}
		 }
		 else fu=func(i);
		 if(fu>ans)ans=fu;
	  }
   	  printf("%d\n",ans);
   }
   return 0;
}

