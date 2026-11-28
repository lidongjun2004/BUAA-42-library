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
int n,m,s;
long long a[50][50],b;
int main()
{
   scanf("%d%d%d",&m,&n,&s);
   for(int i=1;i<=m;i++)
      for(int j=1;j<=n;j++)scanf("%lld",&a[i][j]);
   for(int i=1;i<=m;i++)
   {
   	  for(int j=1;j<=n;j++)
      {
      	 scanf("%lld",&b);
      	 if(s==1)a[i][j]+=b;
      	 else a[i][j]-=b;
      	 printf("%lld ",a[i][j]);
	  }
	  printf("\n");
   }
      
	
   return 0;
}

