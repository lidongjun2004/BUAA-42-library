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
	char c[105];
	int num;
}letter;
char r[105],ch;
letter list[N];
int n,len;
void insert()
{
	for(int i=1;i<=n;i++)
	{
		if(!strcmp(list[i].c,r))
		{
			list[i].num++;
			return;
		}
	}
	strcpy(list[++n].c,r);
	list[n].num++;
}
void input()
{
	FILE *in=fopen("article.txt","r");
	while(fscanf(in,"%c",&ch)!=EOF)
	{
		if(ch>='a'&&ch<='z')
		{
			r[len++]=ch;
			continue;
		}
		if(ch>='A'&&ch<='Z')
		{
			ch+=32;
			r[len++]=ch;
			continue;
		}
		else
		{
			if(r[0]!=0)insert();
			memset(r,0,sizeof(r));
			len=0;
		}
	}
}
int cmp(const void *p,const void *q)
{
	letter x=*(letter*)p,y=*(letter*)q;
	return strcmp(x.c,y.c);
}
int main()
{
    input(); 
    qsort(list+1,n,sizeof(list[0]),cmp);
    for(int i=1;i<=n;i++)
    {
    	printf("%s %d\n",list[i].c,list[i].num);
	}
    return 0;
}



