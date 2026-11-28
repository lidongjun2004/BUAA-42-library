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
char s[1005];
int cal0,cal1,c1[1005],p=-1;
int main()
{
   scanf("%s",&s);
   int len=strlen(s);
   for(int i=0;i<len;i++)
   {
   	  if(s[i]=='1')
   	  {
   	  	 cal0=0;
   	  	 c1[i]=++cal1;
 	  }
   	  else
   	  {
   	  	 cal0++;
   	  	 c1[i]=cal1;
   	  	 if(cal0==4)
   	  	 {
   	  	 	s[i]='V';
   	  	 	cal0=0;
   	  	 	cal1=0;
		 }
	  }
   }
   for(int i=0;i<len;i++)
      if(s[i+3]=='V'&&c1[i]%2==0)s[i]='B';
   for(int i=0;i<len;i++)
   {
   	  if(s[i]=='1'||s[i]=='B')
   	  {
   	  	 p=-p;
		 if(p==1)printf("+1 ");
   	  	 else printf("-1 ");
	  }
	  else if(s[i]=='V')
	  {
	  	 if(p==1)printf("+1 ");
   	  	 else printf("-1 ");
	  }
	  else printf("0 ");
   }
   return 0;
}

