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
int n,T,x[11],y[15],z[15],a,b,c;
int func(int i,int j,int k)
{
   return (y[i]*z[j]-y[j]*z[i])*x[k]+(z[i]*x[j]-z[j]*x[i])*y[k]+(x[i]*y[j]-x[j]*y[i])*z[k];
}
int main()
{
   scanf("%d%d",&n,&T);
   for(int i=1;i<=n;i++)scanf("%d%d%d",&x[i],&y[i],&z[i]);
   for(int i=1;i<=T;i++)
   {
   	  scanf("%d%d%d",&a,&b,&c);
   	  printf("%d\n",func(a,b,c));
   }
   return 0;
}


