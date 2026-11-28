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
int a[11],b[8][4]={0,0,0,0,0,1,5,9,0,2,7,10,0,2,3,6,0,8,9,10,0,6,7,10,0,3,4,8,0,1,2,6};
char c[4][100]={"no triangle\n","acute triangle\n","right triangle\n","obtuse triangle\n"};
char d[3][100]={"","isosceles triangle\n","equilateral triangle\n"};
int f1(int x,int y,int z)
{
   if(x+y<=z||x+z<=y||y+z<=x)return 0;
   if(x*x+y*y>z*z&&z*z+y*y>x*x&&z*z+x*x>y*y)return 1;
   if(x*x+y*y==z*z||z*z+y*y==x*x||z*z+x*x==y*y)return 2;
   return 3;
}
int f2(int x,int y,int z)
{
   if(x==y&&y==z)return 2;
   if(x==y||y==z||z==x)return 1;
   return 0;
}
int main()
{
   for(int i=1;i<=10;i++)scanf("%d",&a[i]);
   for(int i=1;i<=7;i++)
   {
   	  printf("Question %d:\n",i);
   	  int flag1=f1(a[b[i][1]],a[b[i][2]],a[b[i][3]]);
   	  printf("%s",c[flag1]);
   	  if(flag1==0)continue;
   	  int flag2=f2(a[b[i][1]],a[b[i][2]],a[b[i][3]]);
   	  printf("%s",d[flag2]);
   }
   return 0;
}

