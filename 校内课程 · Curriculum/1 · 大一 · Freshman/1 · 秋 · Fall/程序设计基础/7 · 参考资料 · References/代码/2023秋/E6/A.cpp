#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
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
int main()
{
   int sum,n=0;
   char ch;
   scanf("%d %c",&sum,&ch);
   while(ch!='=')
   {
   	  scanf("%d",&n);
   	  if(ch=='-')sum-=n;
   	  if(ch=='+')sum+=n;
   	  scanf(" %c",&ch);
   } 
   printf("%d",sum);
   return 0;
}

