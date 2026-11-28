#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int n;
typedef struct Node
{
	int num;
	struct Node *lson,*rson;
}node;
node *root;
node *insert(node *p,int num)
{
	if(p==NULL)
	{
		p=(node*)malloc(sizeof(node));
		p->num=num;
		p->lson=p->rson=NULL;
	}
	else if(num<p->num)p->lson=insert(p->lson,num);
	else p->rson=insert(p->rson,num);
	return p;
}
void preorder(node *p,int depth)
{
	if(p->lson==NULL&&p->rson==NULL)
	{
		printf("%d %d\n",p->num,depth);
		return;
	}
	if(p->lson!=NULL)preorder(p->lson,depth+1);
	if(p->rson!=NULL)preorder(p->rson,depth+1);
}
int main()
{
    scanf("%d",&n);
    for(int i=1;i<=n;i++)
    {
    	int num;
    	scanf("%d",&num);
    	root=insert(root,num);
	}
	preorder(root,1);
    return 0;
}



