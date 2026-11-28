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
char ch[100005];
char a[400][400];
int main()
{
   int len,tot=0;
   scanf("%s",&ch);
   len=strlen(ch);
   //scanf("%d",&len);
   int n=ceil(sqrt((double)len));
   //printf("%d",n);
   for(int i=1;i<=n;i++)
   {
   	  for(int j=1;j<=n;j++)
   	  {
   	  	 if(tot<len)a[i][j]=ch[tot++];
   	  	 else a[i][j]=' ';
	  }
   }
   for(int i=1;i<=n;i++)
      for(int j=1;j<=n;j++)
      	 if(a[j][i]!=' ')printf("%c",a[j][i]);
   return 0;
}

