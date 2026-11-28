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
long long a,b,c,d;
char ch1[20],ch2[20];
long long m,n,len1,len2,flag;
int main()
{
   scanf("%lld%lld%lld%lld",&a,&b,&c,&d);
   printf("%lld\n%lld\n",a+b,c+d);
   m=a+b;n=c+d;
   if(m<0&&n>=0)printf("a+b<c+d\n");
   if(n<0&&m>=0)printf("a+b>c+d\n");
   if(m<0&&n<0)
   {
   	  m=-m;n=-n;
   }
   while(m>0)
   {
   	  ch1[len1++]=m%10+48;
   	  m/=10;
   }
   while(n>0)
   {
   	  ch2[len2++]=n%10+48;
   	  n/=10;
   }
   while(flag==0&&len1>0&&len2>0)
   {
   	  len1--;len2--;
	  if(ch1[len1]>ch2[len2])flag=1;
   	  if(ch1[len1]<ch2[len2])flag=-1;
   }
   if(flag==1)printf("a+b>c+d\n");
   else if(flag==-1)printf("a+b<c+d\n");
   else 
   {
   	  if(len1)printf("a+b>c+d\n");
   	  else if(len2)printf("a+b<c+d\n");
	  else printf("a+b=c+d\n");
   }
   return 0;
}


