#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
char str[520];
int n,top=-1;
typedef struct node
{
	int op;
	int pos;
	int num;
	char s[520];
}ope;
ope stack[N];
void insert(int pos,char *s)
{
	int len=strlen(s);
	for(int i=strlen(str)-1;i>=pos;i--)str[i+len]=str[i];
	for(int i=pos;i<pos+len;i++)str[i]=s[i-pos];
}
void del(int pos,int num)
{
	int len=strlen(str);
	for(int i=pos;i<pos+num;i++)str[i]=0;
	for(int i=pos;i<len-num;i++)
	{
		str[i]=str[i+num];
		str[i+num]=0;
	}
}
void preedit()
{
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
	{
		int op;
		scanf("%d",&op);
		if(op==1)
		{
			stack[++top].op=1;
			scanf("%d%s",&stack[top].pos,stack[top].s);
			stack[top].num=strlen(stack[top].s);
		}
		if(op==2)
		{
			stack[++top].op=2;
			scanf("%d%s",&stack[top].pos,&stack[top].s);
			stack[top].num=strlen(stack[top].s);
		}
	}
}
void get_s(int pos,int num)
{

	for(int i=pos;i-pos<num;i++)stack[top].s[i-pos]=str[i];
	stack[top].s[pos+num]='\0';
}
void edit()
{
	int op=0;
	while(op!=-1)
	{
		scanf("%d",&op);
		if(op==1)
		{
			stack[++top].op=1;
			scanf("%d%s",&stack[top].pos,&stack[top].s);
			stack[top].num=strlen(stack[top].s);
			insert(stack[top].pos,stack[top].s);
		}
		if(op==2)
		{
			stack[++top].op=2;
			scanf("%d%d",&stack[top].pos,&stack[top].num);
			get_s(stack[top].pos,stack[top].num);
			del(stack[top].pos,stack[top].num);
		}
		if(op==3)
		{
			if(top>=0)
			{
				if(stack[top].op==1)del(stack[top].pos,stack[top].num);
				if(stack[top].op==2)insert(stack[top].pos,stack[top].s);
				top--;
				
			}
		}
	}
}
int main()
{
    gets(str);
    preedit();
    edit();
    printf("%s",str);
    return 0;
}



