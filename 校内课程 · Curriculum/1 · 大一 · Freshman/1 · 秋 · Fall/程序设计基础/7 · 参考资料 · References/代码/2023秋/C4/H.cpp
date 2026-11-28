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
   int T,n,p;
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%d%d",&n,&p);
   	  if(p>=2*n-1)
   	  {
   	  	 for(int i=1;i<=n;i++)printf("%d ",i);
   	  	 printf("\n");
   	  	 continue;
	  }
   	  int num[200005]={0};
   	  for(int i=1;i<=n;i++)num[i%p]++;
   	  int sum=0,s=0;
   	  	 while(num[s])
   	  	 {
   	  	 	printf("%d ",(num[s]-1)*p+s);num[s]--;
   	  	 	if(num[(p-s)%p]){
				  printf("%d ",(num[(p-s)%p]-1)*p+(p-s)%p);
				  num[(p-s)%p]--;
   	  	 	}
   	  	 	if(num[s]==0)s++;
		 }
   }
   return 0;
}

