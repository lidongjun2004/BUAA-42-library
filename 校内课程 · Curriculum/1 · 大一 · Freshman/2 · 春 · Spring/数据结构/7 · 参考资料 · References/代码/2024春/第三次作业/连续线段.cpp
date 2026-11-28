#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
typedef struct node
{
	int x1,y1;
	int x2,y2;
	int sum;
}line;
line l[N];
int n,ans,num,a1,b1,a2,b2,x,y;
int main()
{
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
    {
    	scanf("%d%d%d%d",&a1,&b1,&a2,&b2);
    	int flag=0;
    	for(int j=1;j<=num;j++)
    	{
    		if(a1==l[j].x2&&b1==l[j].y2)
    		{
    			l[j].x2=a2;
    			l[j].y2=b2;
    			l[j].sum++;
    			flag=1;
    			break;
			}
		}
		if(!flag)
		{
			l[++num].x1=a1;
			l[num].y1=b1;
			l[num].x2=a2;
			l[num].y2=b2;
			l[num].sum=1;
		}
	}
	for(int i=1;i<=num;i++)
	{
		if(ans<l[i].sum)
		{
			ans=l[i].sum;
			x=l[i].x1;
			y=l[i].y1;
		}
	}
	printf("%d %d %d",ans,x,y);
    return 0;
}



