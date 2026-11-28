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
int f[10005][10005];
int popcount(int x)
{
   int sum=0;
   while(x>0)
   {
   	  if(x%2)sum++;
   	  x=x>>1;
   }
   return sum;
}
int func(int a,int b)
{
   if(b==0)return 0;
   int p=a^b;
   int g=a&b;
   if(a<10005&&b<10005)
   {
   	  if(f[a][b])return f[a][b];
   	  return f[a][b]=popcount(g)+func(p,2*g);
   }
   return popcount(g)+func(p,2*g);
}
int main()
{
   int a,b;
   while(scanf("%d%d",&a,&b)!=EOF)
   {
   	  if(b==0)printf("0\n");
	  else if(a<10005&&b<10005)
   	  {
   	  	 if(f[a][b])printf("%d\n",f[a][b]);
   	  	 else 
   	  	 {
   	  	 	f[a][b]=func(a,b);
   	  	 	printf("%d\n",f[a][b]);
		 }
	  }
	  else printf("%d\n",func(a,b));
   }
   return 0;
}


