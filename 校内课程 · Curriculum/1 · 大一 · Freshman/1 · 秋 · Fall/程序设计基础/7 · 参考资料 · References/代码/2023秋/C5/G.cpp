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
void move(int i, char from, char to)
{
   printf("Eika moved Koishi %02d form the %c to the %c\n", i, from, to);
}
void hanoi(int n,char from,char via,char to)
{
   if(n==1)
   {
      move(n,from,to);
      return;
   }
   hanoi(n-1,from,to,via);
   move(n, from, to);
   hanoi(n-1,via,from,to);
}

int main()
{
   char ch1,ch2,ch3;
   int n;
   scanf("%c %c %c %d",&ch1,&ch2,&ch3,&n);
   hanoi(n,ch1,ch2,ch3);
   return 0;
}

