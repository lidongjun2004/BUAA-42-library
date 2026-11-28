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
long long gcd(long long a,long long b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
long long abs(long long a)
{
   if(a>=0)return a;
   else return -a;
}
int main()
{
   long long n,x0,y0,x1,y1,x2,y2,s=0,b,ans,a1,b1,a2,b2,c1,c2;
   scanf("%lld",&n);
   scanf("%lld%lld",&x0,&y0);
   scanf("%lld%lld",&x1,&y1);
   b=n;
   c1=abs(x1-x0);c2=abs(y1-y0);
   b+=gcd(c1,c2)-1;
   for(int i=3;i<=n;i++)
   {
   	  scanf("%lld%lld",&x2,&y2);
   	  a1=x1-x0;b1=y1-y0;
   	  a2=x2-x0;b2=y2-y0;
   	  c1=abs(x1-x2);c2=abs(y1-y2);
   	  s+=abs(a1*b2-a2*b1);
   	  b+=gcd(c1,c2)-1;
   	  x1=x2;y1=y2;
   }
   c1=abs(x2-x0);c2=abs(y2-y0);
   b+=gcd(c1,c2)-1;
   ans=(s-b)/2+1;
   printf("%lld",ans);
   return 0;
}

