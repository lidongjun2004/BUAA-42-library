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
char s[1005];
int sum,last;
void change()
{
   for(int i=0;i<strlen(s);i++)
      if(s[i]>='A'&&s[i]<='Z')s[i]+=32;
}
int main()
{
   while(scanf("%s",&s)!=EOF)
   {
   	  change();sum=0;last=-1;
   	  int len=strlen(s);
	  for(int i=0;i<len;i++)
	  {
	  	 if(s[i]=='k'&&s[i+1]=='i'&&s[i+2]=='s'&&s[i+3]=='s')
         {
            sum++;
            last=i;
         }
	  }
	  printf("%d %d\n",sum,last);
   }
   return 0;
}

