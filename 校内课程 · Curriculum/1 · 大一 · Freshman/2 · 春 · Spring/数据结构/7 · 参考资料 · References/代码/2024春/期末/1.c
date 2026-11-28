#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
typedef struct NODE
{
	char type;
	double time;
	int cnt,id;
}node;
node stu[1005];
int n,num;
int checkid(int id,char type)
{
	for(int i=1;i<=num;i++)
	{
		if(stu[i].id==id&&stu[i].type==type)return i;
	}
	stu[++num].id=id;stu[num].type=type;
	return num;
}
int catagory(char a,char b)
{
	if(a==b)return 0;
	if(a=='B')return -1;
	if(b=='B')return 1;
	if(a=='M')return -1;
	if(b=='M')return 1;
}
int cmp(const void *p,const void *q)
{
	node a=*(node*)p,b=*(node*)q;
	if(catagory(a.type,b.type))return catagory(a.type,b.type);
	if(a.time<b.time)return -1;
	if(a.time>b.time)return 1;
	return 0;
}
int main()
{
	scanf("%d",&n);getchar();
	int id,sh,sm,ss,eh,em,es;
	char type;
    for(int i=1;i<=n;i++)
    {
    	type=getchar();
    	scanf("%d%d%d%d%d%d%d",&id,&sh,&sm,&ss,&eh,&em,&es);getchar();
    	int no=checkid(id,type);
    	double s=sh*3600+sm*60+ss,e=eh*3600+em*60+es;
    	stu[no].time+=(e-s)/3600;stu[no].cnt++;
	}
	qsort(stu+1,num,sizeof(stu[0]),cmp);
	for(int i=1;i<=num;i++)printf("%c%d %.2f %d\n",stu[i].type,stu[i].id,stu[i].time,stu[i].cnt);
    return 0;
}
/*
28
B230330 06 00 08 07 02 56
B230326 06 00 10 06 31 09
M220160 06 30 02 07 02 56
B230312 06 50 03 07 12 56
D230126 07 00 02 07 25 01
M220126 07 00 03 07 30 08
B230101 09 30 00 10 31 05
B230330 10 00 07 11 00 10
B230326 10 00 10 11 30 00
M220126 14 05 06 15 06 25
B230330 15 00 07 16 00 10
B230326 15 00 10 16 00 15
D220028 16 00 05 18 30 09
M230507 16 30 06 17 38 56
D210037 17 00 00 17 47 39
D220012 17 00 01 17 47 40
D230126 17 03 56 18 15 55
B230108 17 59 58 19 02 10
B230312 18 00 00 19 02 07
B230101 18 00 01 19 02 06
B230102 18 00 02 19 02 08
D210037 18 02 00 18 40 22
D220012 18 02 05 18 35 56
M230507 19 00 35 20 30 23
B230326 20 00 10 21 33 01
M220126 20 05 03 22 04 01
M220156 20 05 06 22 04 05
M220160 20 05 08 22 04 03
*/


