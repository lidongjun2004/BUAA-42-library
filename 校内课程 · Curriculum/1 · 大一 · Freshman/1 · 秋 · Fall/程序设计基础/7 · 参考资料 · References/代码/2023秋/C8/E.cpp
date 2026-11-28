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
int n,a[100005],b[100005],c[100005];
int count(int x)
{
   int sum=0;
   if(x<0)x=~x+1;
   while(x!=0)
   {
   	  x=x&(x-1);
   	  sum++;
   }
   return sum;
}
int comp(const void *x,const void* y)
{
   int *t1,*t2,sum1=0,sum2=0;
   if(x>0)t1=x;
   else t1=~(x)+1;
   if(y>0)t2=y;
   else t2=~(y)+1;
   while(t1!=0)
   {
   	  t1=t1&(t1-1);
   	  sum1++;
   }
   while(t2!=0)
   {
   	  t2=t2&(t2-1);
   	  sum2++;
   }
   if(sum1>sum2)return 1;
   else if(sum1<sum2)return -1;
   else
   {
   	  if(x>y)return -1;
   	  if(x<y)return 1;
   	  if(x==y)return 0;
   }
}
int main()
{
   scanf("%d",&n);
   for(int i=1;i<=n;i++)
   {
      scanf("%d",&a[i]);
      if(a[i]<0)c[i]=~a[i]+1;
      else c[i]=a[i];
      b[i]=count(a[i]);
   }
   qsort(a+1,n,4,comp);
   for(int i=1;i<=n;i++)
   {
      printf("%11d %2d ",a[i],b[i]);
      for(int i=31;i>=0;i--)printf("%d",c[i]>>i);
      printf("\n");
   }
   return 0;
}


