#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1005
#define INF 2147483647
int n,e,ans;
int map[N][N],edge[N],minw[N],road[N][N],cnt[N];
void prim()
{
	for(int i=0;i<n;i++)minw[i]=map[0][i];
	minw[0]=0;
	for(int a=1;a<n;a++)
	{
		int min=INF,temp;
		for(int i=0;i<n;i++)
		{
			if(min>minw[i]&&minw[i])
			{
				min=minw[i];
				temp=i;
			}
		}
		ans+=min;cnt[road[temp][edge[temp]]]=1;
		minw[temp]=0;
		for(int i=0;i<n;i++)
		{
			if(map[temp][i]<minw[i])
			{
				minw[i]=map[temp][i];
				edge[i]=temp;
			}
		}
	}
}
int main()
{
    scanf("%d%d",&n,&e);
    for(int i=0;i<n;i++)
		for(int j=0;j<n;j++)map[i][j]=INF;
    for(int i=1;i<=e;i++)
    {
    	int id,u,v,w;
    	scanf("%d%d%d%d",&id,&u,&v,&w);
    	map[u][v]=w;map[v][u]=w;
    	road[u][v]=id;road[v][u]=id;
	}
	prim();
	printf("%d\n",ans);
	for(int i=1;i<=e;i++)
	{
		if(cnt[i])printf("%d ",i);
	}
	printf("\n");
    return 0;
}



