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
int a[40][40],b[40][40];
int n,m;
int work(int x,int y)
{
   int sum=0;
   for(int i=0;i<n;i++)
      for(int j=0;j<n;j++)sum+=a[i][j]*b[i+x][j+y];
   return sum;
}
int main()
{
   scanf("%d%d",&n,&m);
   for(int i=0;i<n;i++)
      for(int j=0;j<n;j++)scanf("%d",&a[i][j]);
   for(int i=0;i<m;i++)
      for(int j=0;j<m;j++)scanf("%d",&b[i][j]);
   for(int i=0;i<=m-n;i++)
   {
   	  for(int j=0;j<=m-n;j++)printf("%d ",work(i,j));
   	  printf("\n");
   }
   return 0;
}

