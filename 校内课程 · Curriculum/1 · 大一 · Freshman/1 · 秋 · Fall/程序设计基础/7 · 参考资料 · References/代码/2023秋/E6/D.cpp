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
   char ch1,ch2,chem;
   ch1=getchar();chem=ch1;
   int sum=0,cal=0;
   while(scanf("%c",&ch2)!=EOF)
   {
   	  if(ch2>='A'&&ch2<='Z')
   	  {
   	  	 if(ch1>='A'&&ch1<='Z')
   	  	 {
   	  	 	if(ch1=='H')sum+=1;
   	  	 	if(ch1=='C')sum+=12;
   	  	 	if(ch1=='N')sum+=14;
   	  	 	if(ch1=='O')sum+=16;
   	  	 	cal=0;
   	  	 	chem=ch2;
	     }
	     else
	     {
	     	if(chem=='H')sum+=1*cal;
   	  	 	if(chem=='C')sum+=12*cal;
   	  	 	if(chem=='N')sum+=14*cal;
   	  	 	if(chem=='O')sum+=16*cal;
   	  	 	cal=0;
   	  	 	chem=ch2;
		 }
	  }
	  else if(ch2>='0'&&ch2<='9')cal=cal*10+(int)(ch2-48);
	  else break;
	  	 
	  ch1=ch2;
   }
   if(ch1>='A'&&ch1<='Z')
         {
   	        if(ch1=='H')sum+=1;
            if(ch1=='C')sum+=12;
   	        if(ch1=='N')sum+=14;
   	        if(ch1=='O')sum+=16;
         }
         else
         {
   	        if(chem=='H')sum+=1*cal;
   	        if(chem=='C')sum+=12*cal;
   	        if(chem=='N')sum+=14*cal;
   	        if(chem=='O')sum+=16*cal;
         }
   printf("%d",sum);
   return 0;
}

