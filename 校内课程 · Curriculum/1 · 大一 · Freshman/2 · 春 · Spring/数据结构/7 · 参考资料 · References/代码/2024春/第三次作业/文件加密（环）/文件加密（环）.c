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
	char ch;
	struct Node *next,*pre;
}node;
char s[127],list[127],c;
int hash[127],step,num=95;
node *head,*now;
node *createnode(char ch)
{
	node *p=(node*)malloc(sizeof(node));
	p->ch=ch;p->next=NULL;p->pre=NULL;
	return p;
}
void insert(node *p,node *q)
{
	q->next=p->next;
	q->pre=p;
	p->next->pre=q;
	p->next=q;
} 
void del(node *p)
{
	p->pre->next=p->next;
	p->next->pre=p->pre;
	free(p);
}
void input()
{
	int len=0,j=0;
	c=getchar();
	while(c!='\n')
	{
		s[len++]=c;
		c=getchar();
	}
	for(int i=0;i<len;i++)
	{
		if(!hash[(int)s[i]])
		{
			hash[(int)s[i]]=1;
			s[j++]=s[i];
		}
	}
	len=j;
	for(int i=32;i<=126;i++)
	{
		if(!hash[i])
		{
			s[len++]=i;
		}
	}
	for(int i=0;i<len;i++)
	{
		node *p=createnode(s[i]);
		if(head==NULL)
		{
			head=p;
			head->next=head;
			head->pre=head;
			now=head;
		}
		else
		{
			insert(now,p);
			now=p;
		}
	}
	now=head;
}
void createlist()
{
	c=head->ch;
	while(now->next!=now)
	{
		step=now->ch;
		now=now->next;
		del(now->pre);
		for(int i=2;i<=step;i++)now=now->next;
		list[step]=now->ch;
	}
	list[now->ch]=c;
	//for(int i=32;i<=126;i++)printf("%c",list[i]);
}
void output()
{
	FILE *in=fopen("in.txt","r"),*out=fopen("in_crpyt.txt","w");
	fprintf(out,"\n");
    while(fscanf(in,"%c",&c)!=EOF)
    {
    	if(c>=32&&c<=126)fprintf(out,"%c",list[(int)c]);
    	else fprintf(out,"%c",c);
	}
    fclose(in);
    fclose(out);
}
int main()
{
    input();
    createlist();
    output();
	return 0;
}



