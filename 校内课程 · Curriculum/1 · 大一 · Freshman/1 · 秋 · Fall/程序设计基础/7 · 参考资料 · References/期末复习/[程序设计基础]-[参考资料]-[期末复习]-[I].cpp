#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
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
int T,n,m,a,odd,even,ji,ou;
int main()
{
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%d",&n);odd=0;even=0;
   	  for(int i=1;i<=n;i++)
   	  {
   	  	 scanf("%d",&m);ji=0;ou=0;
   	  	 for(int j=1;j<=m;j++)
   	  	 {
   	  	 	scanf("%d",&a);
   	  	 	if(a%2==0)ou=1;
   	  	 	else ji=1;
		 }
		 if(ji&&!ou)odd++;
		 if(ji&&ou)even++;
	  }
	  if(odd%2==1&&!even)printf("bzjt!\n");
	  else printf("siuuuuu\n");
   }
   return 0;
}


