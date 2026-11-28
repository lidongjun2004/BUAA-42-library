#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#include<ctype.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
#define max(a,b) a>b?a:b
#define min(a,b) a<b?a:b
typedef struct Node
{
	int data;
	struct Node *next,*pre;
}node;
node *head;
node *addnode(int data,int pos)
{
	node *now=head;
	for(int i=1;i<pos;i++)now=now->next;
	node *p=(node*)malloc(sizeof(node));
	
}
void buildlist(int len)
{
	head=(node*)malloc(sizeof(node));
	node *now=head;
	for(int i=1;i<=len;i++)
	{
		node *p=malloc()
	}
}
int main()
{
    
    return 0;
}



