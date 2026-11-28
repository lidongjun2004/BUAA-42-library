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
char s[2005];
int n,len;
void change(int x)
{
   for(int i=0;i<len;i++)s[i]=s[2*i+x];
}
int main()
{
   scanf("%s%d",&s,&n);
   len=strlen(s);
   while(n--)
   {
   	  for(int i=0;i<len;i++)s[len+i]=s[len-i-1];
   	  for(int i=0;i<2*len-1;i+=2)
   	  {
   	  	 if(s[i]>s[i+1])
   	  	 {
   	  	 	change(1);
   	  	 	break;
		 }
		 if(s[i]<s[i+1])
   	  	 {
   	  	 	change(0);
   	  	 	break;
		 }
	  }
   }
   for(int i=0;i<len;i++)printf("%c",s[i]);
   return 0;
}

