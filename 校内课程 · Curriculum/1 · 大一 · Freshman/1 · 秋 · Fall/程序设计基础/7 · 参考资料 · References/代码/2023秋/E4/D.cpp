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
int flag[1005];
int main()
{
   int n,k;
   scanf("%d%d",&n,&k);
   int tot=n,num=0,i=0;
   while(tot>1)
   {
   	  num++;i++;
   	  if(i>n)i=1; 
   	  while(flag[i])
   	  {
   	  	 i++;
   	  	 if(i>n)i=1;
	  }
   	  if(num==k)
   	  {
   	  	 num=0;
   	  	 flag[i]=1;
   	  	 tot--;
	  }
   }
   for(i=1;i<=n;i++)
      if(!flag[i])printf("%d",i);
   return 0;
}

