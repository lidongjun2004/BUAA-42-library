#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
typedef struct Node
{
	int id;
	int son[33],type,stat,num,fa;
}node;
node mach[2005];
int n;
void bfs(int id)
{
	if(mach[id].num==0)
	{
		return;
	}
	for(int i=1;i<=32;i++)
	{
		int sonid=mach[id].son[i];
		if(sonid)
		{
			bfs(sonid);
			if(mach[sonid].stat==1)mach[id].stat=1;
		}
	}
} 
void dfs(int id)
{
	if(mach[id].stat==0)
	{
		printf("%d ",id);
		return;
	}
	for(int i=1;i<=32;i++)
	{
		int sonid=mach[id].son[i];
		if(sonid)
		{
			dfs(sonid);
		}
	}
} 
int main()
{
    scanf("%d",&n);
    int id,fa,no,type;
    scanf("%d%d%d%d",&id,&fa,&no,&type);
    mach[0].fa=fa;mach[id].type=type;
    for(int i=2;i<=n;i++)
    {
    	scanf("%d%d%d%d",&id,&fa,&no,&type);
    	mach[id].fa=fa;mach[fa].son[no]=id;mach[id].type=type;
    	mach[fa].num++;
	}
	while(1)
	{
		scanf("%d",&id);
		if(id==-1)break;
		mach[id].stat=1;
	}
	bfs(0);
	dfs(0);
    return 0;
}



