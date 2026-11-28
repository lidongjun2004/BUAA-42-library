#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   long long n,T;
   scanf("%lld",&T);
   for(int m=1;m<=T;m++)
   {
   	  double pi1=0,pi2=0;
	  scanf("%lld",&n);
   	  for(double i=0;i<n;i++)
   	  {
   	  	 if((int)i%2==0)pi1+=1/(2*i+1);
   	  	 else pi1-=1/(2*i+1);
	  }
	  pi1*=4;
	  for(double i=0;i<n;i++)
   	  {
   	  	 double k=1;
   	  	 k/=2*i+1;
   	  	 k/=2*i+1;
   	  	 pi2+=k;
	  }
	  pi2*=8;
	  pi2=sqrt(pi2);
	  if(pi1>=pi2)printf("%.6lf\n",pi1-pi2);
	  else printf("%.6lf\n",pi2-pi1);
   }
   return 0;
}

