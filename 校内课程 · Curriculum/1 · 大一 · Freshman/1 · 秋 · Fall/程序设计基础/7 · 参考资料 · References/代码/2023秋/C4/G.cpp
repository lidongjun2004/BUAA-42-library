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
   int a,b,c,d,op,m,n,g;
   while(scanf("%d/%d %d/%d %d",&a,&b,&c,&d,&op)!=EOF)
   {
   	  if(op==1)
   	  {
   	  	 m=a*d+b*c;
   	  	 n=b*d;
   	  	 g=gcd(abs(m),abs(n));
   	  	 m/=g;
   	  	 n/=g;
   	  	 if(n<0){m=-m;n=-n;}
   	  	 if(n==1)printf("%d\n",m);
   	  	 else printf("%d/%d\n",m,n);
	  }
	  if(op==2)
   	  {
   	  	 m=a*d-b*c;
   	  	 n=b*d;
   	  	 g=gcd(abs(m),abs(n));
   	  	 m/=g;
   	  	 n/=g;
   	  	 if(n<0){m=-m;n=-n;}
   	  	 if(n==1)printf("%d\n",m);
   	  	 else printf("%d/%d\n",m,n);
	  }
	  if(op==3)
   	  {
   	  	 m=a*c;
   	  	 n=b*d;
   	  	 g=gcd(abs(m),abs(n));
   	  	 m/=g;
   	  	 n/=g;
   	  	 if(n<0){m=-m;n=-n;}
   	  	 if(n==1)printf("%d\n",m);
   	  	 else printf("%d/%d\n",m,n);
	  }
	  if(op==4)
   	  {
   	  	 m=a*d;
   	  	 n=b*c;
   	  	 g=gcd(abs(m),abs(n));
   	  	 m/=g;
   	  	 n/=g;
   	  	 if(n<0){m=-m;n=-n;}
   	  	 if(n==1)printf("%d\n",m);
   	  	 else printf("%d/%d\n",m,n);
	  }
   }
   return 0;
}

