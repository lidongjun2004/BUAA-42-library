#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 205
char s[N],stack[N],ans[N];
int flag1,flag2,flag3,flag4,cnt,line,sline[N],len,done,i,top=-1;
void check()
{
	if(flag1)
	{
		if(s[i]=='*'&&s[i+1]=='/')
		{
			flag1=0;
			i++;
		}
		return;
	}
	if(flag3)
	{
		if(s[i]=='\"')flag3=0;
		return;
	}
	if(flag4)
	{
		if(s[i]=='\'')flag4=0;
		return;
	}
	if(s[i]=='/'&&s[i+1]=='*')
	{
		flag1=1;
		i++;
	}
	else if(s[i]=='/'&&s[i+1]=='/')flag2=1;
	else if(s[i]=='\"')flag3=1;
	else if(s[i]=='\'')flag4=1;
}
void anscheck()
{
	char c=s[i];
    if(c=='(')
	{
		stack[++top]=c;
		sline[top]=line;
		return;
	}
    if(c=='{')
    {
    	if(stack[top]=='(')
    	{
    		printf("without maching \'(\' at line %d",sline[top]);
    		done=1;
    		return;
		}
    	stack[++top]=c;
    	sline[top]=line;
    	return;
	}
	if(c==')')
	{
		if(stack[top]=='(')
		{
			top--;
			return;
		}
		printf("without maching \')\' at line %d",line);
		done=1;
		return;
	}
	if(c=='}')
	{
		if(stack[top]=='{')
		{
			top--;
			return;
		}
		printf("without maching \'}\' at line %d",line);
		done=1;
		return;
	}
}
void input(char a[])
{
	FILE *in=fopen("example.c","r");
	while(fgets(s,N,in)!=NULL)
	{
		line++;flag2=0;
		for(i=0;i<strlen(s);i++)
		{
			check();
			if(flag1)continue;
			if(flag2)break;
			if(flag3)continue;
			if(flag4)continue;
			if(s[i]=='('||s[i]==')'||s[i]=='{'||s[i]=='}')
			{
				anscheck();
				if(done)return;
				ans[len++]=s[i];
			}
		}
	} 
}
int main()
{
    input("lysj loves ldj but ldj loves lysj more");
    if(done)return 0;
    if(top!=-1)printf("without maching \'%c\' at line %d",stack[top],sline[top]);
    else printf("%s",ans);
    return 0;
}



