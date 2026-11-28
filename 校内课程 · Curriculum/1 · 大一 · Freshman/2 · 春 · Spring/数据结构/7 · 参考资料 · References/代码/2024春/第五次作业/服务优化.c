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
	int son[4];
	int depth;
}node;
typedef struct GATE
{
	int id,trfc;
}Gate;
node tree[201];
int ans[101],n;
Gate gate[101];
void buildtree()
{
	int r,son;
	while(1)
	{
		scanf("%d",&r);
		if(r==-1)break;
		for(int i=1;i<=4;i++)
		{
			scanf("%d",&son);
			if(son==-1)break;
			tree[r].son[i]=son;
			tree[son].depth=tree[r].depth+1;
		}
	}
}
int queue[201],head=0,tail=-1;
void layerorder()
{
	queue[++tail]=100;
	while(head<=tail)
	{
		int now=queue[head++];
		if(now<100)
		{
			ans[++n]=now;
			continue;
		}
		for(int i=1;i<=3;i++)
		{
			if(tree[now].son[i])queue[++tail]=tree[now].son[i];
		}
	}
}
int cmp(const void *p,const void *q)
{
	Gate a=*(Gate*)p,b=*(Gate*)q;
	if(a.trfc!=b.trfc)return b.trfc-a.trfc;
	return a.id-b.id; 
}
void readgate()
{
	for(int i=1;i<=n;i++)scanf("%d%d",&gate[i].id,&gate[i].trfc);
	qsort(gate+1,n,sizeof(Gate),cmp);
}
void output()
{
	for(int i=1;i<=n;i++)
	{
		printf("%d->%d\n",gate[i].id,ans[i]);
	}
}
void check()
{
	for(int i=1;i<=n;i++)printf("%d\n",ans[i]);
}
int main()
{
    buildtree();
    layerorder();
    //check();
    readgate();
    output();
    return 0;
}
/*
100 101 102 103 -1
103 14 108 13 -1
101 5 104 6 -1
104 7 8 -1
102 105 106 107 -1
106 1 110 2 -1
108 16 15 -1
107 18 111 17 -1
110 3 4 -1
105 9 109 10 -1
111 20 19 -1
109 11 12 -1
-1
17 865
5 668
20 3000
13 1020
11 980
8 2202
15 1897
6 1001
14 922
7 2178
19 2189
1 1267
12 3281
2 980
18 1020
10 980
3 1876
9 1197
16 980
4 576
*/


