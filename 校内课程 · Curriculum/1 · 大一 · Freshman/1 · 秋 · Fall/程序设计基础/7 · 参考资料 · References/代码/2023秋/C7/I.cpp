#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
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
void swap(void *a,void *b,int data_type_size)
{
   unsigned char *p=(unsigned char *)a;
   unsigned char *q=(unsigned char *)b;
   unsigned char temp;
   while(data_type_size--)
   {
      temp=*p;
      *p=*q;
      *q=temp;
      p++;
      q++;
   }
}
int h,w,a[1005][1005],ans,d[1005][1005],flag[1005][1005];
int dfs(int i,int j)
{
   if(d[i][j])return d[i][j];
   if(!flag[i-1][j]&&a[i-1][j])
   {
   	  flag[i-1][j]=1;
      d[i][j]=max(d[i][j],dfs(i-1,j));
      flag[i-1][j]=0;
   }
   if(!flag[i][j-1]&&a[i][j-1])
   {
   	  flag[i][j-1]=1;
	  d[i][j]=max(d[i][j],dfs(i,j-1));
	  flag[i][j-1]=0;
   }
   if(!flag[i][j+1]&&a[i][j+1])
   {
   	  flag[i][j+1]=1;
	  d[i][j]=max(d[i][j],dfs(i,j+1));
	  flag[i][j+1]=0;
   }
   if(!flag[i+1][j]&&a[i+1][j])
   {
   	  flag[i+1][j]=1;
	  d[i][j]=max(d[i][j],dfs(i+1,j));
	  flag[i+1][j]=0;
   }
   d[i][j]=max(d[i][j],i);
   return d[i][j];
}
int main()
{
   scanf("%d%d",&h,&w);
   for(int i=1;i<=h;i++)
      for(int j=1;j<=w;j++)scanf("%d",&a[i][j]);
   for(int i=1;i<=w;i++)
      if(a[1][i])ans=max(ans,dfs(1,i));
   printf("%d",ans);
   return 0;
}

