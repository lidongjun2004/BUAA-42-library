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
int a,b,ran[1000005],maxn; 
int main()
{
   while(scanf("%d%d",&a,&b)!=EOF)
   {
   	  if(b>ran[a])ran[a]=b;
   	  if(maxn<b)maxn=b;
   }
   for(int i=1;i<=maxn;i++)
   {
   	  if(!ran[i])continue;
   	  printf("%d ",i);
	  for(int n=ran[i];i<=n;i++)
   	  {
   	  	 if(ran[i]>n)n=ran[i];
	  }
	  i--;
	  printf("%d\n",i);
   }
   return 0;
}


