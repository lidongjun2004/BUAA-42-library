#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int postfix[N][2];
char ch,stksym[N];
int tops=-1,n,topt=-1;
typedef struct Node
{
	int num,type;
	struct Node *lson,*rson;
}node;
node *stktree[N];
void check()
{
	for(int i=1;i<=n;i++)
	{
		if(postfix[i][1])printf("%d ",postfix[i][0]);
		else printf("%c ",postfix[i][0]);
	}
	printf("\n");
}
double readnum()
{
	int num=0;
	while(ch>='0'&&ch<='9')
	{
		num=num*10+ch-'0';
		ch=getchar();
	}
	return num;
}
void symdo()
{
	if(ch=='(')stksym[++tops]=ch;
	if(ch=='+'||ch=='-')
	{
		while(tops!=-1&&(stksym[tops]=='*'||stksym[tops]=='/'||stksym[tops]=='+'||stksym[tops]=='-'))postfix[++n][0]=stksym[tops--];
		stksym[++tops]=ch;
	}
	if(ch=='*'||ch=='/')
	{
		while(tops!=-1&&(stksym[tops]=='*'||stksym[tops]=='/'))postfix[++n][0]=stksym[tops--];
		stksym[++tops]=ch;
	}
	if(ch==')')
	{
		while(stksym[tops]!='(')postfix[++n][0]=stksym[tops--];
		tops--;
	}
}
void create_postfix()
{
	while(1)
    {
    	ch=getchar();
    	if(ch>='0'&&ch<='9')
		{
			postfix[++n][0]=readnum();
			postfix[n][1]=1;
		}
        if(ch==' ')continue;
		if(ch=='=')break;
		symdo();
	}
	while(tops!=-1)postfix[++n][0]=stksym[tops--];
	//check();
}
node *buildnode(int num,int type,node *lson,node *rson)
{
	node *now=(node*)malloc(sizeof(node));
	now->num=num;now->type=type;now->lson=lson;now->rson=rson;
	return now;
}
int postorder(node *now)
{
	if(now->type)return now->num;
	if(now->num=='+')return postorder(now->lson)+postorder(now->rson);
	if(now->num=='-')return postorder(now->lson)-postorder(now->rson);
	if(now->num=='*')return postorder(now->lson)*postorder(now->rson);
	if(now->num=='/')return postorder(now->lson)/postorder(now->rson);
}
int main()
{
    create_postfix();
    for(int i=1;i<=n;i++)
    {
    	if(postfix[i][1])
    	{
    		stktree[++topt]=buildnode(postfix[i][0],1,NULL,NULL);
		}
    	else 
    	{
    		node *p=stktree[topt--],*q=stktree[topt--];
    		stktree[++topt]=buildnode(postfix[i][0],0,q,p);
		}
	}
	node *root=stktree[0];
	if(root->type)printf("%d ",root->num);
	else printf("%c ",root->num);
	if(root->lson->type)printf("%d ",root->lson->num);
	else printf("%c ",root->lson->num);
	if(root->rson->type)printf("%d ",root->rson->num);
	else printf("%c ",root->rson->num);
	printf("\n");
	printf("%d",postorder(root));
    return 0;
}



