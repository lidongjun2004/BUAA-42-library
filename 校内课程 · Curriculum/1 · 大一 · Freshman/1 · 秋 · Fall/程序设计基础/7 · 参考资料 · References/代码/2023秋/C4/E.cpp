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
int pts[15],fga[15],fta[15];
int main()
{
   int m;
   scanf("%d",&m);
   int i,x,y;
   while(scanf("%d%d%d",&i,&x,&y)!=EOF)
   {
   	  if(x==1)fta[i]++;
   	  else fga[i]++;
	  if(y)pts[i]+=x;
   }
   for(int i=1;i<=m;i++)
   {
   	  if(fga[i]==0&&fta[i]==0)printf("NULL\n");
   	  else
   	  {
   	  	 double ts,thr;
   	  	 thr=2.0*((double)fga[i]+0.44*(double)fta[i]);
   	  	 ts=(double)pts[i]/thr;
   	  	 ts*=100;
   	  	 printf("%.2lf%%\n",ts);
	  }
   }
   return 0;
}

