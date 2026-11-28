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
int n,t;
int a[1000005],b[1000005],key;
void work()
{
   int l=1,r=n;
   while(l<r)
   {
   	  int mid=(l+r)/2;
   	  if(a[mid]>=key)r=mid;
	  else l=mid+1; 
   }
   if(a[l]!=key)printf("-1\n");
   else printf("%d %d\n",l,b[l]);
}
int main()
{
   scanf("%d%d",&n,&t);
   int flag=1,sum=1;
   scanf("%d",&a[1]);
   for(int i=2;i<=n;i++)
   {
      scanf("%d",&a[i]);
      if(a[i-1]==a[i])sum++;
      else
      {
      	 b[flag]=sum;
		 flag=i;
      	 sum=1;
	  }
   }
   b[flag]=sum;
   while(t--)
   {
   	  scanf("%d",&key);
   	  work();
   }
   return 0;
}


