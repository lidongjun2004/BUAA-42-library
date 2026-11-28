#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
char dic[3505][25],word[25];
int n;
void readdic()
{
	char s[25];
	FILE *in=fopen("dictionary3000.txt","r");
	while(fscanf(in,"%s",dic[n++])!=EOF);
	fclose(in);
}
void search1()
{
	for(int i=0;i<n;i++)
	{
		if(strcmp(word,dic[i])==0)
		{
			printf("1 %d\n",i+1);
			return;
		}
		if(strcmp(word,dic[i])<0)
		{
			printf("0 %d\n",i+1);
			return;
		}
	}
}
void search2()
{
	int mid;
    int l=0,r=n-1,cmp=0;
    while(l<=r)
	{
        mid=l+(r-l)/2;
        cmp++;
        if(strcmp(dic[mid],word)==0)
		{
            printf("1 %d\n",cmp);return;
        }
        else if(strcmp(dic[mid],word)>0)
		{
            r=mid-1;
        }
        else if(strcmp(dic[mid],word)<0)
		{
            l=mid+1;
        }
    }
    printf("0 %d\n",cmp);
}
typedef struct index
{
	int s,e;
}index;
index list[30]; 
void indexset()
{
	for(int i=0;i<26;i++)list[i].e=-1;
	int now=0;
	for(int i=0;i<n;i++)
	{
	    int id=dic[i][0]-'a';
	    if(id!=now)
	    {
	    	list[now].e=i-1;
	    	now=id;
	    	list[now].s=i;
		}
	}
	list[now].e=n-1;
}
void search3()
{
	int mid;
    int l=list[word[0]-'a'].s,r=list[word[0]-'a'].e,cmp=0;
    while(l<=r)
	{
        mid=l+(r-l)/2;
        cmp++;
        if(strcmp(dic[mid],word)==0)
		{
            printf("1 %d\n",cmp);return;
        }
        else if(strcmp(dic[mid],word)>0)
		{
            r=mid-1;
        }
        else if(strcmp(dic[mid],word)<0)
		{
            l=mid+1;
        }
    }
    printf("0 %d\n",cmp);
}
#define NHASH  3001
#define MULT  37
unsigned int hash(char *str)
{
    unsigned int h=0;
    char*p;
    for(p=str;*p!='\0';p++)
        h=MULT*h+*p;
    return h%NHASH;
}
typedef struct node
{
	char word[25];
	struct node *next;
}Hash;
Hash *hashlist[3005];
Hash *createnode(char *word)
{
	Hash *p=(Hash*)malloc(sizeof(Hash));
    p->next=NULL;
    strcpy(p->word,word);
    return p;
}
void hashset()
{
	for(int i=0;i<n;i++)
	{
		int key=hash(dic[i]);
    	Hash *temp=hashlist[key];
    	if(NULL==temp)hashlist[key]=createnode(dic[i]);
    	else
		{
        	while(temp->next!=NULL)temp=temp->next;
        	temp->next=createnode(dic[i]);
    	}
	}
}
void search4()
{
	int key=hash(word);int cmp=0;
    Hash *temp=hashlist[key];
    if(NULL==temp)
	{
		printf("%d %d\n",0,cmp);
		return;
	}
    while(NULL!=temp)
	{
        cmp++;
        if(strcmp(word,temp->word)==0)
		{
			printf("%d %d\n",1,cmp);
			return;
		}
        else if(strcmp(temp->word,word)<0)temp=temp->next;
        else 
		{
			printf("%d %d\n",0,cmp);
			return;
		}
    }
    printf("%d %d\n",0,cmp);
}
void work()
{
	int op;
	n--;
	indexset();
	hashset();
	while(scanf("%s%d",word,&op)!=EOF)
	{
		if(op==1)search1(word);
		if(op==2)search2(word);
		if(op==3)search3(word);
		if(op==4)search4(word);
	}
}
int main()
{
    readdic();
    work();
    return 0;
}
/*
input: 
wins 1
wins 2
wins 3
wins 4
yes 1
yes 2
yes 3
yes 4

output: 
0 3314
0 12
0 7
0 2
1 3357
1 10
1 4
1 1
*/


