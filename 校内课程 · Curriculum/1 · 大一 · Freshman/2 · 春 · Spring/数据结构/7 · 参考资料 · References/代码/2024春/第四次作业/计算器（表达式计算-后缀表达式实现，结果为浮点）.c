#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
char ch,stacksym[N];
int topn=-1,tops=-1,n;
double stacknum[N],suffix[N];
void check()
{
	for(int i=1;i<=n;i++)printf("%2.0lf ",suffix[i]);
	printf("\n");
}
double numdo()
{
	double num=0;
	while(ch>='0'&&ch<='9')
	{
		num=num*10+ch-'0';
		ch=getchar();
	}
	return num;
}
void symdo()
{
	if(ch=='(')stacksym[++tops]=ch;
	if(ch=='+'||ch=='-')
	{
		while(tops!=-1&&(stacksym[tops]=='*'||stacksym[tops]=='/'||stacksym[tops]=='+'||stacksym[tops]=='-'))suffix[++n]=-stacksym[tops--];
		stacksym[++tops]=ch;
	}
	if(ch=='*'||ch=='/')
	{
		while(tops!=-1&&(stacksym[tops]=='*'||stacksym[tops]=='/'))suffix[++n]=-stacksym[tops--];
		stacksym[++tops]=ch;
	}
	if(ch==')')
	{
		while(stacksym[tops]!='(')suffix[++n]=-stacksym[tops--];
		tops--;
	}
}
void tosuffix()
{
	while(1)
    {
    	ch=getchar();
    	if(ch>='0'&&ch<='9')suffix[++n]=numdo();
        if(ch==' ')continue;
		if(ch=='=')break;
		symdo();
	}
	while(tops!=-1)suffix[++n]=-stacksym[tops--];
	check();
}
void work()
{
	for(int i=1;i<=n;i++)
	{
		if(suffix[i]>=0)stacknum[++topn]=suffix[i];
		else
		{
			double a=stacknum[topn--],b=stacknum[topn--];
			char sym=-suffix[i];
			if(sym=='-')stacknum[++topn]=b-a;
			if(sym=='+')stacknum[++topn]=b+a;
			if(sym=='*')stacknum[++topn]=b*a;
			if(sym=='/')stacknum[++topn]=b/a;
		}
	}
	printf("%.2lf",stacknum[0]);
}
int main()
{
    tosuffix();
    work();
    return 0;
}
/*
24 1 5 3 / + 36 6 / 2 / + 2 - / 12 2 / 2 / *
/ -47
+ -43
- -45
* -42
*/


