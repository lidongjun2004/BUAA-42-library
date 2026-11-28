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
char a[105][105];
int n,m,sum;
int check(int i,int j)
{
   sum=0;
   if(a[i][j]=='M')return 0;
   if(a[i-1][j]=='M')sum++;
   if(a[i-1][j-1]=='M')sum++;
   if(a[i-1][j+1]=='M')sum++;
   if(a[i+1][j]=='M')sum++;
   if(a[i+1][j-1]=='M')sum++;
   if(a[i+1][j+1]=='M')sum++;
   if(a[i][j]=='M')sum++;
   if(a[i][j-1]=='M')sum++;
   if(a[i][j+1]=='M')sum++;
   return sum;
}
int main()
{
   scanf("%d%d",&n,&m);getchar();
   for(int i=1;i<=n;i++)
   {
      for(int j=1;j<=m;j++)scanf("%c",&a[i][j]);
      getchar();
   }
      
   for(int i=1;i<=n;i++)
   {
      for(int j=1;j<=m;j++)
	  {
	     a[i][j]+=check(i,j);
	     printf("%c",a[i][j]);
	  }
	  printf("\n");
   }
   return 0;
}

