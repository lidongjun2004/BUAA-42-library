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
   while(scanf("%c",&ch)!=EOF)
   {
   	  if(ch=='0')printf("0000");
   	  if(ch=='1')printf("0001");
   	  if(ch=='2')printf("0010");
   	  if(ch=='3')printf("0011");
   	  if(ch=='4')printf("0100");
   	  if(ch=='5')printf("1011");
   	  if(ch=='6')printf("1100");
   	  if(ch=='7')printf("1101");
   	  if(ch=='8')printf("1110");
   	  if(ch=='9')printf("1111");
   }
   return 0;
}

