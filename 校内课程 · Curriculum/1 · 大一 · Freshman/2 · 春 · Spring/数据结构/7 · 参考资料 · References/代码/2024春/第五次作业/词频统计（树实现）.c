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
	char word[105];
	int cnt;
	struct Node *lson,*rson;
}node;
node *root;
node *buildnode(node *p,char *word)
{
	if(p==NULL)
	{
		p=(node*)malloc(sizeof(node));
		strcpy(p->word,word);
		p->cnt=1;
		p->lson=p->rson=NULL;
		return p;
	}
	if(strcmp(p->word,word)>0)p->lson=buildnode(p->lson,word);
	else if(strcmp(p->word,word)<0)p->rson=buildnode(p->rson,word);
	else p->cnt++;
	return p;
}
void input()
{
	FILE *in=fopen("article.txt","r");
	char word[105],ch;
	int len=0;
	memset(word,0,sizeof(word));
	while(fscanf(in,"%c",&ch)!=EOF)
	{
		if(ch>='a'&&ch<='z')
		{
			word[len++]=ch;
			continue;
		}
		if(ch>='A'&&ch<='Z')
		{
			ch+=32;
			word[len++]=ch;
			continue;
		}
		else
		{
			if(word[0]!=0)root=buildnode(root,word);
			memset(word,0,sizeof(word));
			len=0;
		}
		
	}
	fclose(in);
}
void inorder(node *p)
{
	if(p==NULL)return;
	inorder(p->lson);
	printf("%s %d\n",p->word,p->cnt);
	inorder(p->rson);
}
int main()
{
	input();
	if(root!=NULL)printf("%s ",root->word);
    if(root->rson!=NULL)printf("%s ",root->rson->word);
    if(root->rson->rson!=NULL)printf("%s",root->rson->rson->word);
    printf("\n");
	inorder(root);
    return 0;
}



