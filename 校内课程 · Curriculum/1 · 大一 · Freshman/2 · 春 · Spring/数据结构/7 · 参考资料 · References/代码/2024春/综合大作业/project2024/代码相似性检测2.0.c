#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
#define max2(a,b) ((a)>(b)?(a):(b))
#define LIMIT 0.95
int **Dp, MaxDP=3300;
int min3(int a,int b,int c){
    int min = a < b ? a : b;
    return min < c ? min : c;
}
int error2(char *s){
    fprintf(stderr,"%s\n",s); 
    exit(-1); 
}
int initDP(){		
    int i;
    Dp = (int **)malloc(MaxDP*sizeof(int *));
    for(i=0; i<MaxDP; i++)
    Dp[i] = (int *)malloc(MaxDP*sizeof(int));
	return 0;	
}
int editdistDP(char *str1, char *str2) {
    int i,j;
    int len1, len2;
    static int flag=0;
	
    (flag++) ? 1 : initDP(); 
    len1 = strlen(str1)+1; len2 = strlen(str2)+1;
    (max2(len1,len2)>=MaxDP) ? error2("DP memory error!") : len1;
    for (i=0; i<=len1; i++) {
        for (j=0; j<=len2; j++) {
            if (i==0)
                Dp[i][j] = j;
            else if (j==0)
                Dp[i][j] = i;
            else if (str1[i-1] == str2[j-1])
                Dp[i][j] = Dp[i-1][j-1];
            else
                Dp[i][j] = 1 + min3(Dp[i][j-1], Dp[i-1][j], Dp[i-1][j-1]);
        }
    }
    return Dp[len1][len2];
}
char keepwords[166][10];
void init_keepwords(){
	FILE *in=fopen("keepwords.txt","r");
	for(int i=0;i<165;i++)fscanf(in,"%s",keepwords[i]);
}
int check_keep(char *word){//¿É×ÖµäÊ÷ÓÅ»¯O(n)>>O(logn) 
	for(int i=0;i<165;i++)
		if(strcmp(word,keepwords[i])==0)return 1;
	return 0;
}
typedef struct NODE{
	int id;
	char key[3305];
}node;
node code[10005];
int n;
int check_ch(char ch){
	if(ch>='a'&&ch<='z')return 1;
	if(ch>='A'&&ch<='Z')return 1;
	if(ch=='_')return 1;
	if(ch>='0'&&ch<='9')return 2;
	if(ch=='(')return 3;
	if(ch==')')return 4;
	if(ch=='{')return 5;
	if(ch=='}')return 6;
	if(ch=='\n'||ch=='\t'||ch=='\r'||ch==' ')return 0;
	return 10;
}
void work(FILE *in){
	char ch=0;int op;
	char key[15][3305],name[15][105],order[15][105];
	char word[105];
	int flag[15]={0};
	int len=0,fn=0,cnt1=0,cnt2=0,num=0,key_len=0;
	memset(key,0,sizeof(key));
	memset(name,0,sizeof(name));
	memset(order,0,sizeof(order));
	memset(word,0,sizeof(word));
	while(ch!='\f')
	{
		fscanf(in,"%c",&ch);
		if(ch=='\f')break;
		op=check_ch(ch);
		if(op==0)continue;
		if(op==1||(op==2&&len))word[len++]=ch;
		if(op==3)
		{
			key_len=0;
			if(strcmp(word,"main")==0)
			{
				strcpy(name[0],word);
				len=0;
				memset(word,0,sizeof(word));
				cnt1++;
				while(cnt1)
				{
					fscanf(in,"%c",&ch);
					if(ch=='(')cnt1++;
					if(ch==')')cnt1--;
				}
				while(ch!='{')fscanf(in,"%c",&ch);
				cnt2++;
				strcat(key[0],"{");key_len++;
				while(cnt2)
				{
					fscanf(in,"%c",&ch);
					op=check_ch(ch);
					if(op==5)cnt2++;
					if(op==6)cnt2--;
					if(op==1||(op==2&&len))word[len++]=ch;
					else if(!len)
					{
						if(op)key[0][key_len++]=ch;
						else continue;
					}
					else
					{
						if(check_keep(word))
						{
							strcat(key[0],word);
							key_len=strlen(key[0]);
							len=0;
							memset(word,0,sizeof(word));
						}
						if(!op)continue;
						if(op==3)
						{
							if(len)
							{
								strcpy(order[++num],word); 
								strcat(key[0],"FUNC");
								key_len=strlen(key[0]);
								len=0;
								memset(word,0,sizeof(word));
							}
						}
						key[0][key_len++]=ch;
						len=0;
						memset(word,0,sizeof(word));
					}
				}
				continue;
			}
			strcpy(name[++fn],word);
			len=0;
			memset(word,0,sizeof(word));
			cnt1++;
			while(cnt1)
			{
				fscanf(in,"%c",&ch);
				if(ch=='(')cnt1++;
				if(ch==')')cnt1--;
			}
			while(ch!='{')fscanf(in,"%c",&ch);
			cnt2++;
			strcat(key[fn],"{");key_len++;
			while(cnt2)
			{
				fscanf(in,"%c",&ch);
				op=check_ch(ch);
				if(op==5)cnt2++;
				if(op==6)cnt2--;
				if(op==1||(op==2&&len))word[len++]=ch;
				else if(!len)
				{
					if(op)key[fn][key_len++]=ch;
					else continue;
				}
				else
				{
					if(check_keep(word))
					{
						strcat(key[fn],word);
						key_len=strlen(key[fn]);
						len=0;
						memset(word,0,sizeof(word));
					}
					if(!op)continue;
					if(op==3)
					{
						if(len)
						{
							strcat(key[fn],"FUNC");
							key_len=strlen(key[fn]);
							len=0;
							memset(word,0,sizeof(word));
						}
					}
					key[fn][key_len++]=ch;
					len=0;
					memset(word,0,sizeof(word));
				}
			}
		}
	}
	//for(int i=0;i<=fn;i++)printf("%s\n%s\n",name[i],key[i]);
	strcat(code[n].key,key[0]);
	for(int i=1;i<=num;i++)
	{
		for(int j=1;j<=fn;j++)
		{
			if(!flag[j]&&strcmp(order[i],name[j])==0)
			{
				strcat(code[n].key,key[j]);
				flag[j]=1;
			}
		}
	}
	//printf("%s\n",code[n].key);
}
void init_key(){
	FILE *in=fopen("codes.txt","r");
	int id;
	while(fscanf(in,"%d",&id)!=EOF)
	{
		//printf("%d\n",id);
		code[++n].id=id;
		work(in);
	}
}
int main()
{
	init_keepwords();//checked
	init_key();
	int flag[10005]={0};
	for(int i=1;i<n;i++)
	{
		if(flag[i])continue;
		int check=0;
		for(int j=i+1;j<=n;j++)
		{
			int editDistance=editdistDP(code[i].key,code[j].key);
			double sim=1-(double)editDistance/max2(strlen(code[i].key),strlen(code[j].key));
			if(sim>LIMIT)
			{
				flag[j]=1;
				if(!check)
				{
					printf("%d %d",code[i].id,code[j].id);
					check=1;
				}
				else printf(" %d",code[j].id);
			}
		}
		if(check)printf("\n");
	}
    return 0;
}



