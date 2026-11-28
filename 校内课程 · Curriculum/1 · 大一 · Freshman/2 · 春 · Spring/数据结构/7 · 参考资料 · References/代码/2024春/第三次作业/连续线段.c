#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 105
typedef struct node
{
	int x1,y1;
	int x2,y2;
	int sum;
}line;
line l[N],in[N];
int n,ans,num,x,y;
int cmp(const void *p,const void *q)
{
	line *a=(line*)p,*b=(line*)q;
	return a->x1-b->x1;
}
int main()
{
    scanf("%d",&n);
    for(int i=1;i<=n;i++)scanf("%d%d%d%d",&in[i].x1,&in[i].y1,&in[i].x2,&in[i].y2);
    qsort(in+1,n,sizeof(in[0]),cmp);
    for(int i=1;i<=n;i++)
    {
    	int flag=0;
    	for(int j=1;j<=num;j++)
    	{
    		if(in[i].x1==l[j].x2&&in[i].y1==l[j].y2)
    		{
    			l[j].x2=in[i].x2;
    			l[j].y2=in[i].y2;
    			l[j].sum++;
    			flag=1;
    			break;
			}
			if(in[i].x2==l[j].x1&&in[i].y2==l[j].y1)
    		{
    			l[j].x1=in[i].x1;
    			l[j].y1=in[i].y1;
    			l[j].sum++;
    			flag=1;
    			break;
			}
		}
		if(!flag)
		{
			l[++num].x1=in[i].x1;
			l[num].y1=in[i].y1;
			l[num].x2=in[i].x2;
			l[num].y2=in[i].y2;
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



