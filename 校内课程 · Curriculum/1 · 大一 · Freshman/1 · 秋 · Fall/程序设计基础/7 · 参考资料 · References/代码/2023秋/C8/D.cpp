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
int n,sum,tar;
double a[105],ave[105];
int main()
{
   while(scanf("%d",&n)!=EOF)
   {
   	  for(int i=1;i<=n;i++)scanf("%lf",&a[i]);
   	  tar=0;sum=0;
	  for(int i=5;i<=n;i++)
   	  {
   	  	 ave[i]=(a[i]+a[i-1]+a[i-2]+a[i-3]+a[i-4])/5.0;
   	  	 if(ave[i]<10.0)sum++;
   	  	 else sum=0;
   	  	 if(sum==5)
		 {
		    tar=i-4;
		    break;
		 }
	  }
	  if(tar)
	  {
	  	 for(int i=tar-4;i<=tar;i++)
	  	    if(a[i]<10.0)
			{
			   printf("Success %d\n",i);
			   break;
			}
	  }
	  else printf("Failure\n");
   }
   return 0;
}


