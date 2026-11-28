#include<stdio.h>
#include<math.h>
#include<string.h>
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
void swap(int a,int b)
{
   int t=a;
   a=b;
   b=t;
}
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
int main()
{
   int year,score;
   while(scanf("%d%d",&year,&score)!=EOF)
   {
   	  if(year==2023)
   	  {
   	  	 if(score>=85)printf("%d\nYou can choose whether to take the course or not.\n",score);
   	  	 else printf("You have to take the course.\n");
	  }
	  else
	  {
	  	 if(score>=60)printf("%d\n",score);
	  	 else printf("You have to take the course.\n");
	  }
   }
   
   return 0;
}

