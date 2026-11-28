#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
#define max(a,b) a>b?a:b
#define min(a,b) a<b?a:b
int n,num[N],totnum,r,windows=3;
int time[N],ans[N],window[6];
int wait[N],head=0,tail=-1,inqueue=0;
void input()
{
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
	{
		scanf("%d",&num[i]);
		num[i]+=num[i-1];
	}
	totnum=num[n];
	for(int id=1;id<=totnum;id++)scanf("%d",&time[id]);
}
void output()
{
	for(int i=1;i<=totnum;i++)printf("%d : %d\n",i,ans[i]);
}
void work()
{
	for(int i=1;i<=5;i++)
	{
		if(window[i])window[i]--;
	}
}
void insert()
{
	for(int id=num[r-1]+1;id<=num[r];id++)
	{
		wait[++tail]=id;
		inqueue++;
		ans[id]=-r;
	}
}
void addwin()
{
	if(inqueue<21)windows=3;
	if(inqueue>=21&&inqueue<28)windows=4;
	if(inqueue>=28)windows=5;
}
void delwin()
{
	if(inqueue<28)windows=3;
	if(inqueue>=28&&inqueue<35)windows=4;
	if(inqueue>=35)windows=5;
}
void service()
{
	for(int i=1;i<=windows;i++)
	{
		if(window[i])continue;
		if(inqueue>0)
		{
			window[i]=time[wait[head]];
			ans[wait[head]]+=r;
			head++;
			inqueue--;
		}
	}
}

int main()
{
    input();
    for(r=1;r<=n;r++)
    {
    	insert();
    	addwin();
    	service();
    	delwin();
    	work();
	}
	while(inqueue>0)
	{
		service();
		delwin();
		work();
		r++;
	}
	output();
    return 0;
}



