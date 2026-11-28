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
	int id;
}list[105];
int n,flag,len,same;
ll rep[105];
int cmp(const void *a,const void *b)
{
	if(strcmp(((struct node*)a)->name,((struct node*)b)->name))return strcmp(((struct node*)a)->name,((struct node*)b)->name);
	return ((struct node*)a)->id-((struct node*)b)->id;
}
int main()
{
    scanf("%d",&n);
	for(int i=1;i<=n;i++)
	{
		scanf("%s%lld",list[i].name,&list[i].tel);
		list[i].id=i;
	}
    qsort(list+1,n,sizeof(list[0]),cmp);
//    for(int i=1;i<=n;i++)printf("%s %lld\n",list[i].name,list[i].tel);
	for(int i=1;i<=n;i++)
    {
    	if(!strcmp(list[i].name,list[i-1].name))
    	{
    		same=0;
    		for(int j=1;j<=len;j++)
    		    if(rep[j]==list[i].tel)same=1;
			if(same)continue;
			flag++;
		}
		else 
		{
		    flag=0;len=0;
		    memset(rep,0,sizeof(rep));
		}
		rep[++len]=list[i].tel;
		printf("%s",list[i].name);
		if(flag)printf("_%d",flag);
		printf(" %lld\n",list[i].tel);
	}
    return 0;
}



