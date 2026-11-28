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
char s[1005],ch;
int st,ed,sum;
int main()
{
   gets(s);
   while(scanf("%c",&ch)!=EOF)
   {
   	  sum=0;
   	  for(int i=0;i<strlen(s);i++)
   	  {
   	  	 if(s[i]==ch)
   	  	 {
   	  	 	sum++;
   	  	 	if(sum==1)st=i;
   	  	 	else ed=i;
		 }
	  }
	  if(!sum)printf("-1\n");
	  else if(sum==1)printf("%d\n",st);
	  else printf("%d\n",ed-st);
   }
   return 0;
}

