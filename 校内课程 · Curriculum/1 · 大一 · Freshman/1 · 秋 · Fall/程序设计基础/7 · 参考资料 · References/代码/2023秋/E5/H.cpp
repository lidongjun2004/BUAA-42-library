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
long long am=2,an=2; 
void work1(long long m)
{
   if(m==1||m==2)return;
   if(m==3||m==4)
   {
   	  am++;
   	  return;
   }
   if(m==6)
   {
   	  am+=2;
   	  return;
   }
   if(m==7||m==8||m==9||m==10||m==11)
   {
   	  am+=3;
   	  return;
   }
   work1((m-1)/2);
   am++;
   work1(m/2);
}
void work2(long long n)
{
   if(n==1||n==2)return;
   if(n==3||n==4||n==5)
   {
   	  an++;
   	  return;
   }
   if(n==6)
   {
   	  an+=2;
   	  return;
   }
   if(n==7||n==8||n==9||n==10||n==11)
   {
   	  an+=3;
   	  return;
   }
   work2((n-1)/2);
   an++;
   work2(n/2);
}
int main()
{
   long long m,n;
   scanf("%lld%lld",&m,&n);
   if(m>2)work1(m-2);
   else am=1;
   if(n>2)work2(n-2);
   else an=1;
   long long a=am*an; 
   long long b=am*n+an*m-a;
   long long c=m*n-b;
   printf("%lld\n%lld\n%lld",a,b,c);
   return 0;
}

