#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
char back[100][85],forw[100][85];
char comm[10],web[85];
int topb=-1,topf=-1;
char name[105][85];
int cnt[105],num;
char na[85];
void push(int type,char *w)
{
	if(type==1)strcpy(back[++topb],w);
	if(type==2)strcpy(forw[++topf],w);
}
char *pop(int type)
{
	if(type==1)return back[topb--];
	if(type==2)return forw[topf--];
}
char *checkname(char id[])
{
	memset(na,0,sizeof(na));
	int len=strlen(id);
	for(int i=8;id[i]!='/';i++)
	{
		if(id[i]=='/')break;
		na[i-8]=id[i];
	}
	return na;
}
void count(char *w)
{
	char word[85];
	strcpy(word,checkname(w));
	//printf("%s\n",word);
	for(int i=0;i<num;i++)
	{
		if(!strcmp(name[i],word))
		{
			cnt[i]++;
			return;
		}
	}
	strcpy(name[num++],word);
	cnt[num-1]++;
}
int main()
{
	strcpy(web,"https://www.baidu.com/");
	printf("%s\n",web);
	count(web);
    while(strcmp(comm,"QUIT"))
    {
    	scanf("%s",comm);
    	if(!strcmp(comm,"VISIT"))
    	{
    		push(1,web);
    		scanf("%s",web);
    		count(web);
    		topf=-1;
    		printf("%s\n",web);
		}
		if(!strcmp(comm,"<-"))
    	{
    		if(topb==-1)continue;
    		push(2,web);
    		strcpy(web,pop(1));
    		count(web);
    		printf("%s\n",web);
		}
		if(!strcmp(comm,"->"))
    	{
    		if(topf==-1)continue;
    		push(1,web);
    		strcpy(web,pop(2));
    		count(web);
    		printf("%s\n",web);
		}
		if(!strcmp(comm,"QUIT"))
		{
			int y,ii;
			scanf("%d",&y);
			if(y==1)
			{
				int m=0;
				for(int i=0;i<num;i++)
				{
					//printf("%s %d\n",name[i],cnt[i]);
					if(m<cnt[i])
					{
						m=cnt[i];
						ii=i;
					}
				}
				printf("%s %d\n",name[ii],m);
			} 
		}
	}
    return 0;
}
/*
VISIT https://www.buaa.edu.cn/
VISIT https://www.taobao.com/
<-
<-
<-
->
VISIT https://www.buaa.edu.cn/jgsz/jxkyjg.htm
<-
<-
->
->
->
QUIT 1
*/


