#include<stdio.h>
#include<math.h>
#include<string.h>
int ans[32];
int main()
{
   unsigned int a,b,c,d,e,m;
   scanf("%u%u",&a,&b);
   c=a&b;
   d=a^b;
   e=(c<<1)+d;
   m=e;
   for(int i=31;i>=0;i--)
   {
   	  ans[i]=a&1;
   	  a=a>>1;
   }
   for(int i=0;i<32;i++)printf("%u",ans[i]);
   printf("\n");
   for(int i=31;i>=0;i--)
   {
   	  ans[i]=b&1;
   	  b=b>>1;
   }
   for(int i=0;i<32;i++)printf("%u",ans[i]);
   printf("\n");
   for(int i=31;i>=0;i--)
   {
   	  ans[i]=c&1;
   	  c=c>>1;
   }
   for(int i=0;i<32;i++)printf("%u",ans[i]);
   printf("\n");
   for(int i=31;i>=0;i--)
   {
   	  ans[i]=d&1;
   	  d=d>>1;
   }
   for(int i=0;i<32;i++)printf("%d",ans[i]);
   printf("\n");
   for(int i=31;i>=0;i--)
   {
   	  ans[i]=e&1;
   	  e=e>>1;
   }
   for(int i=0;i<32;i++)printf("%u",ans[i]);
   printf("\n");
   printf("%u",m);
   return 0;
}

