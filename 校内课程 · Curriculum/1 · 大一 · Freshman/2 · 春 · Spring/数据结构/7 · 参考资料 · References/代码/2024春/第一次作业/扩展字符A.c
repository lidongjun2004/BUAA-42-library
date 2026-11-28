#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int max(int a,int b){
   if(a>b)return a;
   return b;
}
int min(int a,int b){
   if(a<b)return a;
   return b;
}
int gcd(int a,int b){
   if(b==0)return a;
   return gcd(b,a%b);
}
void swap(void *a,void *b,int data_type_size){
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
char s[10005];
int len;
int main()
{
   scanf("%s",s);
   len=strlen(s);
   printf("%c",s[0]);
   for(int i=1;i<len;i++)
   {
   	  if(s[i]=='-')
   	  {
   	  	 if(s[i-1]>='A'&&s[i-1]<='Z'&&s[i+1]>='A'&&s[i+1]<='Z')
   	  	 	for(char ch=s[i-1]+1;ch<s[i+1];ch++)
			   printf("%c",ch);
   	  	 else if(s[i-1]>='a'&&s[i-1]<='z'&&s[i+1]>='a'&&s[i+1]<='z')
   	  	 	for(char ch=s[i-1]+1;ch<s[i+1];ch++)
			   printf("%c",ch);
	     else if(s[i-1]>='0'&&s[i-1]<='9'&&s[i+1]>='0'&&s[i+1]<='9')
   	  	 	for(char ch=s[i-1]+1;ch<s[i+1];ch++)
			   printf("%c",ch);	
		 else printf("%c",s[i]);
	  }
	  else printf("%c",s[i]);
   }
   return 0;
}



