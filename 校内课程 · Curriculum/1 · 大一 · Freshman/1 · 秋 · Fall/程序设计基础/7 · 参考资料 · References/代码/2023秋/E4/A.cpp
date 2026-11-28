#include<stdio.h>
#include<math.h>
#include<string.h>
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
void swap(int a,int b)
{
   int t=a;
   a=b;
   b=t;
}
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
int abs(int a)
{
   if(a>=0)return a;
   else return -a;
}
int main()
{
   char ch;
   int n;
   scanf("%c%d",&ch,&n);
   for(int i=1;i<=n;i++)
   {
   	  for(int j=1;j<i;j++)printf(" ");
   	  for(int j=i;j<=n;j++)printf("%c",ch);
   	  printf("\n");
   } 
   return 0;
}

