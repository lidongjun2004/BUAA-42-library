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
void sort(int *arr,int left,int right)
{
   if(left>right)return;
   int tmp=arr[left];
   int i=left;
   int j=right;
   while(i!=j)
   {
      while(arr[j]>=tmp&&j>i)j--;
      while(arr[i]<=tmp&&j>i)i++;
      if(j>i)
      {
         int t=arr[i];
         arr[i]=arr[j];
         arr[j]=t;
      }
   }
   arr[left]=arr[i];
   arr[i]=tmp;
   sort(arr,left,i-1);
   sort(arr,i+1,right);
}
int a[1005][1005],n,m,sum[7],ans,flag[7];
char s[7]={'0','V','I','O','L','E','T'};
int main()
{
   scanf("%d%d",&m,&n);
   for(int i=1;i<=m;i++)
   {
   	  for(int j=1;j<=n;j++)
   	  {
   	  	 scanf("%d",&a[i][j]);
	  }
   }
   for(int i=1;i<=m-2;i++)
   {
   	  for(int j=1;j<=n-2;j++)
   	  {
   	  	 sum[1]=a[i][j]+a[i+1][j]+a[i+2][j+1]+a[i+1][j+2]+a[i][j+2];
   	  	 sum[2]=a[i][j+1]+a[i+1][j+1]+a[i+2][j+1];
   	  	 sum[3]=a[i][j]+a[i+1][j]+a[i+2][j]+a[i][j+1]+a[i+2][j+1]+a[i][j+2]+a[i+1][j+2]+a[i+2][j+2];
   	  	 sum[4]=a[i][j]+a[i+1][j]+a[i+2][j]+a[i+2][j+1]+a[i+2][j+2];
		 sum[5]=a[i][j]+a[i+1][j]+a[i+2][j]+a[i][j+1]+a[i+1][j+1]+a[i+2][j+1]+a[i][j+2]+a[i+1][j+2]+a[i+2][j+2];
	     sum[6]=a[i][j]+a[i][j+1]+a[i+1][j+1]+a[i+2][j+1]+a[i][j+2];
	     for(int k=1;k<=6;k++)
	     {
	     	if(sum[k]>ans)
	     	{
	     	   ans=sum[k];
	     	   for(int ii=1;ii<=6;ii++)flag[ii]=0;
	     	   flag[k]=1;
			}
			if(sum[k]==ans)flag[k]=1;
		 }
	  }
   }
   printf("%d\n",ans);
   for(int i=1;i<=6;i++)
   {
   	  if(flag[i])printf("%c",s[i]);
   }
   return 0;
}


