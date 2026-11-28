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
	int pos,size;
	struct Node *next,*pre;
}node;
node *head;
int cnt;
node *insertnode(int pos,int size)
{
	if(head==NULL)
	{
		head=(node*)malloc(sizeof(node));
		head->pos=pos;head->size=size;
		head->next=head;head->pre=head;
		return head;
	}
	node *p=(node*)malloc(sizeof(node));
	p->pos=pos;p->size=size;
	node *now=head;
	do
	{
		if(p->pos<now->pos)
		{
			p->next=now;
			p->pre=now->pre;
			now->pre->next=p;
			now->pre=p;
			if(now==head)head=p;
			return p;
		}
		now=now->next;
		cnt++;
	}while(now!=head);
	p->next=now;
	p->pre=now->pre;
	now->pre->next=p;
	now->pre=p;
	return p; 
}
void combin(node *p)
{
	if(p->pos==p->pre->pos+p->pre->size)
	{
		p->pre->size+=p->size;
		p->pre->next=p->next;
		p->next->pre=p->pre;
		p=p->pre;
	}
	if(p->pos+p->size==p->next->pos)
	{
		p->size+=p->next->size;
		p->next=p->next->next;
		p->next->next->pre=p;
	}
}
int main()
{
    while(1)
    {
    	int a,b;
    	scanf("%d%d",&a,&b);
    	if(a==-1)break;
    	node *p=insertnode(a,b);
    	combin(p);
	}
	printf("%d\n",cnt);
	node *now=head;
	do
	{
		printf("%d %d\n",now->pos,now->size);
		now=now->next; 
	}while(now!=head);
    return 0;
}

/*
4000 400
6000 800
8000 600
10168 624
12004 828
8808 808
2000 800
7248 328
-1 -1


16
2000 800
4000 400
6000 800
7248 328
8000 600
8808 808
10168 624
12004 828
*/

/*
4000 400
6000 800
6800 240
8000 808
10168 624
12004 828
8808 808
2000 800
7248 328
-1 -1


18
2000 800
4000 400
6000 1040
7248 328
8000 1616
10168 624
12004 828
*/

