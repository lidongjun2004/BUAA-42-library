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
int d[200005];
int main()
{
   int n,m,limit,l,r,x,ans=0;
   long long sum=0;
   scanf("%d%d%d",&n,&m,&limit);
   for(int i=1;i<=m;i++)
   {
   	  scanf("%d%d%d",&l,&r,&x);
   	  d[l]+=x;d[r+1]-=x;
   }
   for(int i=1;i<=n;i++)
   {
   	  sum+=d[i];
   	  if(sum>=limit)ans++;
   }
   printf("%d",ans);
   return 0;
}

