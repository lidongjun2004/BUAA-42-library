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
int a[2100]={0,0,1};
int mi[12]={1,2,4,8,16,32,64,128,256,512,1024,2048};
int main()
{
   int n;
   //printf("%d %d",a[1],a[2]);
   scanf("%d",&n);
   for(int i=2;i<=n;i++)
      for(int j=mi[i-1]+1;j<=mi[i];j++)a[j]=a[mi[i]-j+1]+mi[i-1];
   for(int i=1;i<=mi[n];i++)
   {
   	  for(int j=n-1;j>=0;j--)
   	  {
   	  	 printf("%d",a[i]/mi[j]);
   	  	 a[i]%=mi[j];
	  }
	  printf("\n");
   }
   return 0;
}

