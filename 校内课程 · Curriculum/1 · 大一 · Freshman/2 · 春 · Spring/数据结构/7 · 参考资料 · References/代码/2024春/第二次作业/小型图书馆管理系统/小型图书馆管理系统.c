#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
typedef struct node
{
	char name[55],auth[25],prod[35],date[15];
}book;
book lib[505];
int num,order=1;
char s[55];
int cmp(const void *a,const void *b)
{
	return strcmp(((book*)a)->name,((book*)b)->name);
}
void insert()
{
	num++;
	scanf("%s%s%s%s",lib[num].name,lib[num].auth,lib[num].prod,lib[num].date);
	qsort(lib+1,num,sizeof(lib[0]),cmp);
}
int check(int id)
{
	int len=strlen(lib[id].name);
	for(int i=0;i<len;i++)
	{
		int flag=0;
		for(int j=0;j<strlen(s);j++)
		{
			if(s[j]!=lib[id].name[i+j])
			{
				flag=1;break;
			}
		}
		if(!flag)return 1;
	}
	return 0;
}
void search()
{
	scanf("%s",s);
	for(int i=1;i<=num;i++)
	{
		if(check(i))
		{
			printf("%s",lib[i].name);
			for(int j=strlen(lib[i].name)+1;j<=50;j++)printf(" ");
			printf("%s",lib[i].auth);
			for(int j=strlen(lib[i].auth)+1;j<=20;j++)printf(" ");
			printf("%s",lib[i].prod);
			for(int j=strlen(lib[i].prod)+1;j<=30;j++)printf(" ");
			printf("%s",lib[i].date);
			for(int j=strlen(lib[i].date)+1;j<=10;j++)printf(" ");
			printf("\n");
		}
	}
}
void del()
{
	scanf("%s",s);
	int sum=0;
	for(int i=1;i<=num;i++)
	{
		if(check(i))
		{
			lib[i].name[0]=150;
			sum++;
		}
	}
	qsort(lib+1,num,sizeof(lib[0]),cmp);
	num-=sum;
}
int main()
{
    FILE *in=fopen("books.txt","r"),*out=fopen("ordered.txt","w");
    while(fscanf(in,"%s",lib[++num].name)!=EOF)fscanf(in,"%s%s%s",lib[num].auth,lib[num].prod,lib[num].date);
	qsort(lib+1,num,sizeof(lib[0]),cmp);
//	for(int i=1;i<=num;i++)
//	{
//		printf("%s",lib[i].name);
//		for(int j=strlen(lib[i].name)+1;j<=50;j++)printf(" ");
//		printf("%s",lib[i].auth);
//		for(int j=strlen(lib[i].auth)+1;j<=20;j++)printf(" ");
//		printf("%s",lib[i].prod);
//		for(int j=strlen(lib[i].prod)+1;j<=30;j++)printf(" ");
//		printf("%s",lib[i].date);
//		for(int j=strlen(lib[i].date)+1;j<=10;j++)printf(" ");
//		printf("\n");
//	}
	while(order)
    {
    	scanf("%d",&order);
    	if(order==1)insert();
    	if(order==2)search();
    	if(order==3)del();
	}
	for(int i=1;i<=num;i++)
	{
		fprintf(out,"%s",lib[i].name);
		for(int j=strlen(lib[i].name)+1;j<=50;j++)fprintf(out," ");
		fprintf(out,"%s",lib[i].auth);
		for(int j=strlen(lib[i].auth)+1;j<=20;j++)fprintf(out," ");
		fprintf(out,"%s",lib[i].prod);
		for(int j=strlen(lib[i].prod)+1;j<=30;j++)fprintf(out," ");
		fprintf(out,"%s",lib[i].date);
		for(int j=strlen(lib[i].date)+1;j<=10;j++)fprintf(out," ");
		fprintf(out,"\n");
	}
	fclose(in);
	fclose(out);
    return 0;
}



