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
long long a[45][45],b[45][45],ans[45][45];
int main()
{
   int m,n,p;
   scanf("%d%d%d",&m,&n,&p);
   for(int i=1;i<=m;i++)
      for(int j=1;j<=n;j++)scanf("%lld",&a[i][j]);
   for(int i=1;i<=n;i++)
      for(int j=1;j<=p;j++)scanf("%lld",&b[i][j]);
   for(int i=1;i<=m;i++)
   {
   	  for(int j=1;j<=p;j++)
   	  {
   	  	 for(int k=1;k<=n;k++)ans[i][j]+=a[i][k]*b[k][j];
   	  	 printf("%lld ",ans[i][j]);
	  }
	  printf("\n");
   }
   return 0;
}


