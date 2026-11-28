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
int main()
{
   char s[32],s1[32]="long long",s2[32]="long",s3[32]="int",s4[32]="short",s5[32]="char";
   int n;
   while(gets(s)!=NULL)
   {
	  scanf("%d",&n);
      getchar();
	  if(!strcmp(s,s1))printf("%d\n",sizeof(long long)*n);
	  else if(!strcmp(s,s2))printf("%d\n",sizeof(long)*n);
   	  else if(!strcmp(s,s3))printf("%d\n",sizeof(int)*n);
   	  else if(!strcmp(s,s5))printf("%d\n",sizeof(char)*n);
   	  else if(!strcmp(s,s4))printf("%d\n",sizeof(short)*n);
   	  else printf("Err0r!\n");
   } 
   return 0;
}

