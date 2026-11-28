//文件压缩-Huffman实现
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAXSIZE 32
struct tnode {					//Huffman树结构
	char c;		
	int weight;					//树节点权重，叶节点为字符和它的出现次数
	struct tnode *left,*right;
} ; 
int Ccount[128]={0};			//存放每个字符的出现次数，如Ccount[i]表示ASCII值为i的字符出现次数 
struct tnode *Root=NULL; 		//Huffman树的根节点
char HCode[128][MAXSIZE]={{0}}; //字符的Huffman编码，如HCode['a']为字符a的Huffman编码（字符串形式） 
int Step=0;						//实验步骤 
FILE *Src, *Obj;
	
void statCount();				//步骤1：统计文件中字符频率
void createHTree();				//步骤2：创建一个Huffman树，根节点为Root 
void makeHCode();				//步骤3：根据Huffman树生成Huffman编码
void atoHZIP(); 				//步骤4：根据Huffman编码将指定ASCII码文本文件转换成Huffman码文件

void print1();					//输出步骤1的结果
void print2(struct tnode *p);	//输出步骤2的结果 
void print3();					//输出步骤3的结果
void print4();					//输出步骤4的结果

int main()
{
	if((Src=fopen("input.txt","r"))==NULL) {
		fprintf(stderr, "%s open failed!\n", "input.txt");
		return 1;
	}
	if((Obj=fopen("output.txt","w"))==NULL) {
		fprintf(stderr, "%s open failed!\n", "output.txt");
		return 1;
	}
	scanf("%d",&Step);					//输入当前实验步骤 
	
	statCount();						//实验步骤1：统计文件中字符出现次数（频率）
	if(Step==1) 
		print1(); 			//输出实验步骤1结果	
	createHTree();						//实验步骤2：依据字符频率生成相应的Huffman树
	if(Step==2) 
		print2(Root); 		//输出实验步骤2结果	
	makeHCode();				   		//实验步骤3：依据Root为树的根的Huffman树生成相应Huffman编码
	if(Step==3) 
		print3(); 			//输出实验步骤3结果
	if(Step>=4) 
		atoHZIP(),print4(); 	//实验步骤4：据Huffman编码生成压缩文件，并输出实验步骤4结果	

	fclose(Src);
	fclose(Obj);

    return 0;
} 

//【实验步骤1】开始 

void statCount()
{
	Ccount[0]=1;
	char c;
	while(fscanf(Src,"%c",&c)!=EOF)
	{
		if(c=='\n')continue;
		Ccount[c]++;
	}
}

//【实验步骤1】结束

//【实验步骤2】开始
struct tnode *Forest[100005];
int size;
int cmp(const void *p,const void *q)
{
	struct tnode *a=*(struct tnode**)p,*b=*(struct tnode**)q;
	if(a->weight!=b->weight)return a->weight-b->weight;
	return a->c-b->c;
}
struct tnode *merge(struct tnode *p,struct tnode *q)
{
	struct tnode *father=(struct tnode*)malloc(sizeof(struct tnode));
	father->left=p;father->right=q;
	father->weight=p->weight+q->weight;
	return father;
}
void insert(struct tnode *p)
{
	int w=p->weight;
	for(int i=2;i<=size;i++)Forest[i-2]=Forest[i];
	size-=2;
	for(int i=0;i<=size;i++)
	{
		if(w<Forest[i]->weight)
		{
			for(int j=size;j>=i;j--)Forest[j+1]=Forest[j];
			Forest[i]=p;
			size++;
			break;
		}
	}
}
void check1()
{
	for(int i=0;i<size;i++)printf("%d %d\n",Forest[i]->c,Forest[i]->weight);
}
void createHTree()
{
	for(int i=0;i<128;i++)
	{
		if(Ccount[i]>0)
		{
			struct tnode *p=(struct tnode *)malloc(sizeof(struct tnode));
			p->c=i;p->weight=Ccount[i];
			p->left=NULL;p->right=NULL;
			Forest[size++]=p;
		}
	}
	qsort(Forest,size,sizeof(Forest[0]),cmp);
	//check1();
	Forest[size]=(struct tnode *)malloc(sizeof(struct tnode));
	Forest[size]->weight=2147483647;
	while(size>1)
	{
		struct tnode *p=merge(Forest[0],Forest[1]);
		insert(p);
	}
	Root=Forest[0];
}

//【实验步骤2】结束

//【实验步骤3】开始
void visitHtree(struct tnode *p,char *str,int depth)
{
	//printf("%d ",depth);
	//printf("%d %d\n",p->left->weight,p->right->weight);
	if(p->left==NULL&&p->right==NULL)
	{
		strcpy(HCode[p->c],str);
		return;
	}
	str[depth]='0';str[depth+1]=0;
	if(p->left!=NULL)visitHtree(p->left,str,depth+1);
	str[depth]='1';str[depth+1]=0;
	if(p->right!=NULL)visitHtree(p->right,str,depth+1);
}
void makeHCode()
{
	char str[MAXSIZE];
	memset(str,0,sizeof(str));
    visitHtree(Root,str,0);
} 

//【实验步骤3】结束

//【实验步骤4】开始

char s[1000005],ch;
void atoHZIP()
{
	rewind(Src);
	while(fscanf(Src,"%c",&ch)!=EOF)
	{
		//printf("%c",ch);
		if(ch!='\n')strcat(s,HCode[ch]);
	}
	//printf("\n");
	//printf("%s\n",s);
	strcat(s,HCode[0]);
	//printf("%s\n",s);
	if(strlen(s)%8)
	{
		for(int i=strlen(s);i<strlen(s)-strlen(s)%8+8;i++)s[i]='0';
		s[strlen(s)-strlen(s)%8+8]=0;
	}
	//printf("%s\n",s);
	unsigned char hc;
	for(int i=0;s[i]!='\0';i++)
	{
		hc=(hc<<1)|(s[i]-'0');
		if((i+1)%8==0) 
		{
			fputc(hc,Obj);
			printf("%x",hc);
		}
	}
}

//【实验步骤4】结束

void print1()
{
	int i;
	printf("NUL:1\n");
	for(i=1; i<128; i++)
		if(Ccount[i] > 0)
			printf("%c:%d\n", i, Ccount[i]);
}

void print2(struct tnode *p)
{
	if(p != NULL){
		if((p->left==NULL)&&(p->right==NULL)) 
			switch(p->c){
				case 0: printf("NUL ");break;
				case ' ':  printf("SP ");break;
				case '\t': printf("TAB ");break;
				case '\n':  printf("CR ");break;
				default: printf("%c ",p->c); break;
			}
		print2(p->left);
		print2(p->right);
	}
}

void print3()
{
	int i;
	
	for(i=0; i<128; i++){
		if(HCode[i][0] != 0){
			switch(i){
				case 0: printf("NUL:");break;
				case ' ':  printf("SP:");break;
				case '\t': printf("TAB:");break;
				case '\n':  printf("CR:");break;
				default: printf("%c:",i); break;
			}
			printf("%s\n",HCode[i]);
		}
	}
} 

void print4()
{
	long int in_size, out_size;
	
	fseek(Src,0,SEEK_END);
	fseek(Obj,0,SEEK_END);
	in_size = ftell(Src);
	out_size = ftell(Obj);
	
	printf("\n原文件大小：%ldB\n",in_size);
	printf("压缩后文件大小：%ldB\n",out_size);
	printf("压缩率：%.2f%%\n",(float)(in_size-out_size)*100/in_size);
}
