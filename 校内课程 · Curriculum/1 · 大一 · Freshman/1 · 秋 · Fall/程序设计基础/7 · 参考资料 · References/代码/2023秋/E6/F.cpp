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
int len;
char s[105],ans[105],cap[105];
int less()
{
   for(int i=0;i<len;i++)
   {
   	  if(ans[i]>cap[i])return 1;
   	  if(ans[i]<cap[i])return 0;
   }
   return 0;
}
int main()
{
   scanf("%s",&s);
   len=strlen(s);
   for(int i=0;i<len;i++)ans[i]=s[i];
   for(int i=0;i<len;i++)
   {
   	  for(int j=0;j<len;j++)cap[j]=s[(j+i)%len];
   	  if(less())
   	     for(int k=0;k<len;k++)ans[k]=cap[k];
   }
   printf("%s",ans);
   return 0;
}

