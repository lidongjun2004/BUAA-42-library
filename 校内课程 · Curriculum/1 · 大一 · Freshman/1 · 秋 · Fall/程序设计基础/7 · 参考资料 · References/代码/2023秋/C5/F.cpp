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
int su(int n)
{
   if(n==1)return 0;
   for(int i=2;i<=sqrt(double(n));i++)
      if(n%i==0)return 0;
   return 1;
}
int main()
{
   int l,r,sum=0;
   scanf("%d%d",&l,&r);
   for(int i=l;i<=r-2;i++)
   {
   	  if(su(i)&&su(i+2))
   	  {
   	  	 printf("%d %d\n",i,i+2);
   	  	 sum++;
	  }
   }
   printf("%d",sum); 
   return 0;
}

