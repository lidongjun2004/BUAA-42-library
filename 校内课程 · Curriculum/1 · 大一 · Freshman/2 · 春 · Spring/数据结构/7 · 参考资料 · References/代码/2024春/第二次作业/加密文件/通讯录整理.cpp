#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
struct node
{
	char name[25];
	ll tel;
}list[105];
int n;
int cmp(const node *a,const node *b)
{
	return strcmp(a->name,b->name);
}
int main()
{
    scanf("%d",&n);
	for(int i=1;i<=n;i++)scanf("%s%lld",list[i].name,&list[i].tel);
    qsort(list+1,n,sizeof(list[0]),cmp);
    return 0;
}



