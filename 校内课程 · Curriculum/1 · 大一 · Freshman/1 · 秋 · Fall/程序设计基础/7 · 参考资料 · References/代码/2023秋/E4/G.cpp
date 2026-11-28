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
int c[5005],r[5005];
int main()
{
   int a,b;
   scanf("%d%d",&a,&b);
   int GCD=gcd(a,b);
   a/=GCD;
   b/=GCD;
   if(b==1)
   {
      printf("%d.(0)",a);
      return 0;
   }
   printf("%d.",a/b);
   int res=a%b,len=0,flag=0,str,ans;
   while(!flag)
   {
   	  ans=res*10/b;
      res=res*10%b;
	  for(int i=1;i<=len;i++)
   	  {
   	  	 if(ans==c[i]&&res==r[i])
   	  	 {
   	  	 	flag=1;
   	  	 	str=i;
   	  	 	break;
		 }
	  }
	  len++;
	  c[len]=ans;r[len]=res;
   }
   for(int i=1;i<str;i++)printf("%d",c[i]);
   printf("(");
   for(int i=str;i<len;i++)printf("%d",c[i]);
   printf(")");
   return 0;
}

