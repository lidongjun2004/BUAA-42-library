#include<stdio.h>
#include<math.h>
#include<string.h>
int main()
{
   int n,AK=0,pass=0,NoneAC=0,a,b,c,d,e,f,g,h,i,j,score;
   double sum=0;
   scanf("%d",&n);
   for(int k=1;k<=n;k++)
   {
   	  scanf("%d%d%d%d%d%d%d%d%d%d",&a,&b,&c,&d,&e,&f,&g,&h,&i,&j);
   	  score=a+b+c+d+e+f+g+h+i+j;
   	  if(score>=100)sum+=100;
	  else sum+=score;
   	  //printf("%d %lf\n",score,sum);
   	  if(score==110)AK++;
   	  if(score>=60)pass++;
   	  if(a<30&&b<20&&c<10&&d<10&&e<10&&f<10&&g<5&&h<5&&i<5&&j<5)NoneAC++;
   }
   sum/=(double)n;
   printf("%.2lf\n",sum);
   printf("%d\n%d\n%d\n",pass,AK,NoneAC);
   return 0;
}

