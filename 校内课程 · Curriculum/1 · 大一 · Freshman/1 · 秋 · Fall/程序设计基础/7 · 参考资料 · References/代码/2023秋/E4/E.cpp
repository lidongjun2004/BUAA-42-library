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
   int n,year,month,day,hour,minute;
   scanf("%d",&n);
   for(int i=1;i<=n;i++)
   {
   	  scanf("%d.%d.%d %d:%d",&year,&month,&day,&hour,&minute);
   	  if(minute>=60)
   	  {
   	  	 minute-=60;
   	  	 hour++;
	  }
	  if(hour>=24)
	  {
	  	 day+=hour/24;
	  	 hour%=24;
	  }
	  if(month>12)
	  {
	  	 year+=(month-1)/12;
	  	 month-=(month-1)/12*12;
	  }
	  if(month==1)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==2)
	  {
	  	 if(day>28)
	  	 {
		    if(day>28)
	  	    {
		       if(((year%4==0&&year%100!=0)||year%400==0)&&year%3200!=0)
		       {
		     	  if(day>29)
				  {
				     day-=29;
		   	         month++;
				  }
		       }
		       else
		       {
		          day-=28;
		          month++;
			   }
		    }
		 }
	  }
	  if(month==3)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==4)
	     if(day>30)
	  	 {
	  	 	day-=30;
	  	 	month++;
		 }
	  if(month==5)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==6)
	     if(day>30)
	  	 {
	  	 	day-=30;
	  	 	month++;
		 }
	  if(month==7)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==8)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==9)
	     if(day>30)
	  	 {
	  	 	day-=30;
	  	 	month++;
		 }
	  if(month==10)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month==11)
	     if(day>30)
	  	 {
	  	 	day-=30;
	  	 	month++;
		 }
	  if(month==12)
	     if(day>31)
	  	 {
	  	 	day-=31;
	  	 	month++;
		 }
	  if(month>12)
	  {
	  	 month%=12;
	  	 year++;
	  	 if(month==1)
	        if(day>31)
	  	    {
	  	 	   day-=31;
	  	 	   month++;
		    }
	     if(month==2)
	     {
	  	    if(day>28)
	  	    {
		       if(((year%4==0&&year%100!=0)||year%400==0)&&year%3200!=0)
		       {
		     	  if(day>29)
				  {
				     day-=29;
		   	         month++;
				  }
		       }
		       else
		       {
		          day-=28;
		          month++;
			   }
		    }
	     }
	  }
	  printf("%d.",year);
	  if(month<10)printf("0%d.",month);
	  else printf("%d.",month);
	  if(day<10)printf("0%d ",day);
	  else printf("%d ",day);
	  if(hour<10)printf("0%d:",hour);
	  else printf("%d:",hour);
	  if(minute<10)printf("0%d\n",minute);
	  else printf("%d\n",minute);
   }
   return 0;
}

