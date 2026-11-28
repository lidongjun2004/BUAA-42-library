#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   char ch;
   while(scanf("%c",&ch)!=EOF)
   {
   	  if(ch>'A'&&ch<='Z')printf("%c",ch-1);
   	  else printf("%c",ch);
   } 
   return 0;
}

