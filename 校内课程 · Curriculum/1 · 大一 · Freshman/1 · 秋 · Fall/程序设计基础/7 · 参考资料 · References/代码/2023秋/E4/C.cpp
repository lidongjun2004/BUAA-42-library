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
int abs(int a)
{
   if(a>=0)return a;
   else return -a;
}
int main()
{
   int n,flag=0,score=0,combo=0,mostcombo=0;
   char ch;
   scanf("%d",&n);getchar();
   for(int i=1;i<=n;i++)
   {
   	  scanf("%c",&ch);
   	  getchar();
   	  if(ch=='p')
	  {
	     score+=300;
	     combo++;
	     if(combo>mostcombo)mostcombo=combo;
	  }
   	  if(ch=='g')
   	  {
   	  	 score+=208;
   	  	 combo++;
   	  	 if(combo>mostcombo)mostcombo=combo;
   	  	 if(flag==0)flag=1;
	  }
	  if(ch=='b')
	  {
	  	 score+=105;
	  	 flag=2;
	  	 if(combo>mostcombo)mostcombo=combo;
	  	 combo=0;
	  }
	  if(ch=='m')
	  {
	  	 flag=2;
	  	 if(combo>mostcombo)mostcombo=combo;
	  	 combo=0;
	  }
   }
   printf("%d\n%d\n",score,mostcombo);
   if(flag==0)printf("All Perfect!");
   if(flag==1)printf("Full Combo!");
   if(flag==2)printf("Moca Complete!");
   return 0;
}

