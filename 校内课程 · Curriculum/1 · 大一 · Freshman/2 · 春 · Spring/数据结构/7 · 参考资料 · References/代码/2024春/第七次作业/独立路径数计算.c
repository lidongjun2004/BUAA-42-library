#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
int n,e,vis[N],road[N];
typedef struct node
{
	int id;
	int dest;
	struct node *next;
}path;
path *list[N];
void addpath(int id,int u,int v)
{
	path *p,*temp=(path*)malloc(sizeof(path));
	temp->dest=v;temp->id=id;temp->next=NULL;
	if(list[u]==NULL)
	{
		list[u]=temp;
		return;
	}
	for(p=list[u];p->next!=NULL;p=p->next);
	p->next=temp;
}
void dfs(int u,int len)
{
	if(u==n-1)
	{
		for(int i=0;i<len;i++)printf("%d ",road[i]);
		printf("\n");
		return;
	}
	vis[u]=1;
	for(path *p=list[u];p!=NULL;p=p->next)
	{
		if(vis[p->dest])continue;
		road[len]=p->id;
		dfs(p->dest,len+1);
	}
	vis[u]=0;
}
int main()
{
    scanf("%d%d",&n,&e);
    for(int i=1;i<=e;i++)
    {
    	int id,u,v;
    	scanf("%d%d%d",&id,&u,&v);
		addpath(id,u,v);addpath(id,v,u);
	}
	dfs(0,0);
    return 0;
}



