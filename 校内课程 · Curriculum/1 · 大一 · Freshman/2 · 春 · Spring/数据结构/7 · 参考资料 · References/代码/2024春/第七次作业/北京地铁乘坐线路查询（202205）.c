#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1005
#define INF 2147400000
int line_n,station_n;
typedef struct Node
{
	int state;
	char name[30];
}node;
node station[N];
int map[N][N],line_id[N][N];
int search_id(char *name,int state)
{
	for(int i=1;i<=station_n;i++)
		if(!strcmp(station[i].name,name))return i;
	station[++station_n].state=state;
	strcpy(station[station_n].name,name);
	return station_n;
}
void add_edge(int u,int v,int id)
{
	map[u][v]=1;
	map[v][u]=1;
	line_id[u][v]=id;
	line_id[v][u]=id;
}
void initmap()
{
	FILE *in=fopen("bgstations.txt","r");
	fscanf(in,"%d",&line_n);
	for(int i=0;i<N;i++)
		for(int j=0;j<N;j++)map[i][j]=INF;
	for(int i=1;i<=line_n;i++)
	{
		int line,station_num;
		fscanf(in,"%d%d",&line,&station_num);
		int pre_id=0;
		for(int j=1;j<=station_num;j++)
		{
			char station_name[30];
			int station_state;
			fscanf(in,"%s%d",station_name,&station_state);
			int id=search_id(station_name,station_state);
			add_edge(pre_id,id,line);
			pre_id=id;
		}
	}
}
int minw[N],wfound[N],spath[N];
void dijkstra(int s,int e)
{
	for(int i=1;i<=station_n;i++)
	{
		minw[i]=map[s][i];
		spath[i]=s;
	}
	minw[s]=0;wfound[s]=1;
	for(int i=1;i<station_n;i++)
	{
		int min=INF,tar;
		for(int j=1;j<=station_n;j++)
		{
			if(!wfound[j]&&min>minw[j])
			{
				min=minw[j];
				tar=j;
			}
		}//12.5x-125=100-20x
		wfound[tar]=1;
		if(tar==e)return;
		for(int j=1;j<=station_n;j++)
		{
			if(!wfound[j]&&min+map[tar][j]<minw[j])
			{
				minw[j]=min+map[tar][j];
				spath[j]=tar; 
			}
		} 
	}
}
void output(int s,int e)
{
	int path[N],top=-1;
	for(int i=e;i!=s;i=spath[i])
	{
		path[++top]=i;
	}
	int cnt=1,pre_id=path[top],id,line=line_id[s][pre_id];
	printf("%s-%d",station[s].name,line);
	for(int i=top-1;i>=0;i--)
	{
		id=path[i];
		if(line!=line_id[pre_id][id])
		{
			line=line_id[pre_id][id];
			printf("(%d)-%s-%d",cnt,station[pre_id].name,line);
			cnt=0;
		} 
		pre_id=id;cnt++;
	}
	printf("(%d)-%s",cnt,station[e].name);
}
char start_station[30],end_station[30];
int main()
{
    initmap(); 
    scanf("%s%s",start_station,end_station);
    int start_id=search_id(start_station,0),end_id=search_id(end_station,0);
    dijkstra(start_id,end_id);
    output(start_id,end_id);
    return 0;
}



