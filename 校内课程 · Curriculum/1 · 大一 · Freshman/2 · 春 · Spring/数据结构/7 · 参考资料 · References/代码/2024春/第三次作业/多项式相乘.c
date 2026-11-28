#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10000005
typedef struct node
{
	int xi;
	int mi;
	struct node *next;
}term,*termptr;
term a[N],b[N];
termptr list;
int in1,in2,numa,numb;
void insert(int x,int m)
{
	termptr p,q;
	q=(termptr)malloc(sizeof(term));
	q->mi=m;q->xi=x;q->next=NULL;
	if(list==NULL)
	{
	    list=q;
		return;
	}
	for(p=list;p->next!=NULL&&m<=p->next->mi;p=p->next);
	if(m==p->mi)
	{
		p->xi+=x;
		free(q);
		return;
	}
	q->next=p->next;
	p->next=q;
}
int main()
{
    scanf("%d%d",&in1,&in2);
    a[++numa].xi=in1;
    a[numa].mi=in2;
	while(getchar()!='\n')
    {
    	scanf("%d%d",&in1,&in2);
        a[++numa].xi=in1;
        a[numa].mi=in2;
	}
	scanf("%d%d",&in1,&in2);
    b[++numb].xi=in1;
    b[numb].mi=in2;	
	while(getchar()!='\n')
    {
    	scanf("%d%d",&in1,&in2);
        b[++numb].xi=in1;
        b[numb].mi=in2;
	}
	for(int i=1;i<=numa;i++)
	{
		for(int j=1;j<=numb;j++)
		{
			insert(a[i].xi*b[j].xi,a[i].mi+b[j].mi);
		}
	}
	for(termptr p=list;p!=NULL;p=p->next)
	{
		printf("%d %d ",p->xi,p->mi);
	}
    return 0;
}



