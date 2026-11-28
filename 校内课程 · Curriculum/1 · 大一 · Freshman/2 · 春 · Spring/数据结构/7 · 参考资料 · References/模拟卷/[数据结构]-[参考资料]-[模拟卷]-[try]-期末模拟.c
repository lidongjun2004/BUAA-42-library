#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
typedef struct STU
{
	int id,state;
	int cid;
	char name[20];
}Stu;
Stu stu[205];
int n,num;
void insert(int pos,int id,char name[],int cid)
{
	num++;
	for(int i=num;i>pos;i--)
	{
		stu[i].id=stu[i-1].id;
		stu[i].state=stu[i-1].state;
		stu[i].cid=stu[i-1].cid;
		strcpy(stu[i].name,stu[i-1].name);
	}
	stu[pos].id=id;
	stu[pos].state=0;
	stu[pos].cid=cid;
	strcpy(stu[pos].name,name);
}
void check(int id,char name[],int cid)
{
	for(int i=1;i<=num;i++)
	{
		if(stu[i].id==id)
		{
			if(stu[i].cid!=cid)stu[i].state=1;
			return;
		}
		if(stu[i].id>id)
		{
			insert(i,id,name,cid);
			return;
		}
	}
	insert(num+1,id,name,cid);
}
void input()
{
	scanf("%d",&n);
	for(int i=1;i<=n;i++) 
	{
		int id,cid;
		char name[20],time[10];
		scanf("%d%s%d%s",&id,name,&cid,time);
		check(id,name,cid);
	}
}
void output()
{
	for(int i=1;i<=num;i++)
	{
		if(stu[i].state)
			printf("%d %s\n",stu[i].id,stu[i].name);
	}
}
int main()
{
    input();
    output();
    return 0;
}
/*
21
191028 wangdi 15 093000
192387 litong 39 093000
190877 liugang 37 093001
197583 huangqinian 196 093004
195211 liuhao 201 093005
193098 zhaogang 377 093006
190001 zhousheng 1 093007
190009 wuhong 12 093007
197583 huangqinian 197 093008
195877 lisisi 202 093008
192387 litong 309 093009
191000 tonghao 201 093402
197583 huangqinian 196 093500
191028 wangdi 15 093507
190010 wangzhuang 85 093558
195333 zhangye 63 093600
197583 huangqinian 195 094100
195211 liuhao 200 095103
190010 wangzhuang 287 095509
193098 zhaogang 377 095606
191028 wangdi 15 095709
*/



