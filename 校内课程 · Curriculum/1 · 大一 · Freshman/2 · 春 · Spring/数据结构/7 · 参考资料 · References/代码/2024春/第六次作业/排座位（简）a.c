#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int n,hash[105];
typedef struct NODE
{
	int id,pos;
	char name[25];
}node;
node stu[105];
int cmp(const void *a,const void *b)
{
	node p=*(node*)a,q=*(node*)b;
	if(p.pos-q.pos)return p.pos-q.pos;
	return p.id-q.id;
} 
int cmp2(const void *a,const void *b)
{
	node p=*(node*)a,q=*(node*)b;
	return p.id-q.id;
} 
void input()
{
	scanf("%d",&n);
    FILE *in=fopen("in.txt","r");
    for(int i=1;i<=n;i++)fscanf(in,"%d%s%d",&stu[i].id,stu[i].name,&stu[i].pos);
	qsort(stu+1,n,sizeof(node),cmp);
	fclose(in);
}
void work1()
{
	int q=stu[n].pos<n?stu[n].pos:n;
	int cnt=n;
	for(int i=1;i<=n;i++)hash[stu[i].pos]++;
	for(int i=1;i<=q;i++)
	{
		if(hash[i])continue;
		if(i>=stu[cnt].pos)break;
		hash[stu[cnt].pos]--;
		stu[cnt].pos=i;
		hash[i]++;
		cnt--;
	}
	qsort(stu+1,n,sizeof(node),cmp);
}
void work2()
{
	int m=n;
	for(int i=n;i>=1;i--)
	{
		if(hash[stu[i].pos]==1)continue;
		hash[stu[i].pos]--;
		stu[i].pos=m--;
		hash[stu[i].pos]++;
	}
	qsort(stu+1,n,sizeof(node),cmp2);
}
void output()
{
	FILE *out=fopen("out.txt","w");
	for(int i=1;i<=n;i++)printf("%d %s %d\n",stu[i].id,stu[i].name,stu[i].pos);
	for(int i=1;i<=n;i++)fprintf(out,"%d %s %d\n",stu[i].id,stu[i].name,stu[i].pos);
	fclose(out);
}
int main()
{
    input();
	work1();
	work2();
	output();
    return 0;
}



