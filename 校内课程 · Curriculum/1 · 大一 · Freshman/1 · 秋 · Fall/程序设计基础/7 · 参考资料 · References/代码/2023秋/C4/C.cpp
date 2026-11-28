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
int score[1005],rank[1005];
int main()
{
   int n;
   scanf("%d",&n);
   int a=n/10,b=n/4,c=n*3/5,d=n*9/10;
   rank[0]=1;
   for(int i=1;i<=n;i++)
   {
   	  scanf("%d",&score[i]);
   	  if(score[i]==score[i-1])rank[i]=rank[i-1];
   	  else rank[i]=i;
   	  if(rank[i]<=a)printf("A ");
   	  else if(rank[i]<=b)printf("B ");
   	  else if(rank[i]<=c)printf("C ");
   	  else if(rank[i]<=d)printf("D ");
   	  else printf("E ");
   }
   return 0;
}

