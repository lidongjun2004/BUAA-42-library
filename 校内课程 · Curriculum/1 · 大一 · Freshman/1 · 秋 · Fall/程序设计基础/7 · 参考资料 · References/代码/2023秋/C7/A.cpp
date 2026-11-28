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
int n; 
int main()
{
   while(scanf("%d",&n)!=EOF)
   {
   	  if(n==1)printf("Shall I compare thee to a summer's day?\n");
   	  if(n==2)printf("Thou art more lovely and more temperate:\n");
   	  if(n==3)printf("Rough winds do shake the darling buds of May,\n");
   	  if(n==4)printf("And summer's lease hath all too short a date;\n");
   	  if(n==5)printf("Sometime too hot the eye of heaven shines,\n");
   	  if(n==6)printf("And often is his gold complexion dimm'd;\n");
   	  if(n==7)printf("And every fair from fair sometime declines,\n");
   	  if(n==8)printf("By chance or nature's changing course untrimm'd;\n");
   	  if(n==9)printf("But thy eternal summer shall not fade,\n");
   	  if(n==10)printf("Nor lose possession of that fair thou ow'st;\n");
   	  if(n==11)printf("Nor shall death brag thou wander'st in his shade,\n");
   	  if(n==12)printf("When in eternal lines to time thou grow'st:\n");
   	  if(n==13)printf("    So long as men can breathe or eyes can see,\n");
   	  if(n==14)printf("    So long lives this, and this gives life to thee.\n");
   }
   return 0;
}

