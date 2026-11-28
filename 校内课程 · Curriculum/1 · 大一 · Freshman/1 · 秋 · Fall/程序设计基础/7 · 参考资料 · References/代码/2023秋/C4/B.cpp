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
char ch[1005];
int main()
{
   int sum=0;
   scanf("%s",&ch);
   int len=strlen(ch);
   for(int i=0;i<len;i++)
   {
   	  if(ch[i]=='0')printf("0 ");
   	  else
   	  {
   	  	 sum++;
   	  	 if(sum%2)printf("+1 ");
   	  	 else printf("-1 ");
	  }
   } 
   return 0;
}

