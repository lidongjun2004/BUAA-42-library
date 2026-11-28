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
	int site;
	int mem;
	struct Node *next,*pre;
}node;
node *head,*p;
int n,apply;
node* createnode(int a,int b)
{
	node *q=(node*)malloc(sizeof(node));
	q->site=a;q->mem=b;q->next=NULL;q->pre=NULL;
	return q;
}
void read()
{
	scanf("%d",&n);
    for(int i=1;i<=n;i++)
    {
    	int a,b;
    	scanf("%d%d",&a,&b);
		if(head==NULL)
		{
		    head=createnode(a,b);
		    p=head;
		    head->next=head;
		    head->pre=head;
		}
        else 
        {
        	node *q=createnode(a,b);
        	q->next=head;
        	q->pre=p;
        	p->next=q;
        	head->pre=q;
        	p=q;
		}
	}
	p=head;
}
void del(node *q)
{
    node *pre,*next;
    pre=q->pre;
    next=q->next;
	pre->next=next;
    next->pre=pre;
    free(q);
}
void search()
{
	node *q=p,*ans=NULL;
	do
	{
		if(q->mem>=apply)
		{
			ans=q;break;
		}
		q=q->next;
	}while(q!=p);
	if(ans==NULL)return;
	p=ans;
	p->mem-=apply;
	if(p->mem==0)
	{
		p=p->next;
		del(p->pre);
	}
}
void output()
{
	node *q=p;
	if(p->mem==0)return;
	do
	{
		printf("%d %d\n",q->site,q->mem);
		q=q->next;
	}while(q!=p);
}
int main()
{
    read();
	while(1)
	{
		scanf("%d",&apply);
		if(apply==-1)break;
		search();
	}
	output();
    return 0;
}



