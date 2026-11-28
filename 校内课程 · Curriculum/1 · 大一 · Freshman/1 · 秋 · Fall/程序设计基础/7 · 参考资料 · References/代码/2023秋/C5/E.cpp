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
int catalan(int n)
{
   if(!n)return 1;
   int ans=0;
   for(int i=0;i<n;i++)ans+=catalan(i)*catalan(n-i-1);
   return ans;
}
int main()
{
   int T,n;
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%d",&n);
   	  printf("%d\n",catalan(n));
   }
   return 0;
}

