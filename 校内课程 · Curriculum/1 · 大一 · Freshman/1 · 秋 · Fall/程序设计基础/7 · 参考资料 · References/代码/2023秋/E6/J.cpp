#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
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
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
int n;
int a[1000005],ans;
void swap(int x,int y)
{
   int t=a[x];
   a[x]=a[y];
   a[y]=t;
}
void con(int l,int r,int s)
{
   if(l==s)return;
   int m=s-1;
   while(a[m]>a[m+1])
   {
   	  swap(m,m+1);
   	  ans++;
   	  m++;
   }
   con(l,r,s-1);
}
void sort(int l,int r)
{
   if(l==r)return;
   int mid=(l+r)/2;
   sort(l,mid);sort(mid+1,r);
   con(l,r,mid+1);
}
int main()
{
   scanf("%d",&n);a[n+1]=2147483647;
   for(int i=1;i<=n;i++)scanf("%d",&a[i]);
   sort(1,n);
   printf("%d",ans);
   return 0;
}

