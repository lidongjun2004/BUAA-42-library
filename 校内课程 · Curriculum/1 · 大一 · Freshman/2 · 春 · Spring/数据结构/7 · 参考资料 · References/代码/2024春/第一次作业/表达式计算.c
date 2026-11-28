#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int max(int a,int b)
{
    if(a>b)return a;
    return b;
}
int min(int a,int b)
{
    if(a<b)return a;
    return b;
}
int gcd(int a,int b)
{
    if(b==0)return a;
    return gcd(b,a%b);
}
void swap(void *a,void *b,int data_type_size)
{
    unsigned char *p=(unsigned char *)a;
    unsigned char *q=(unsigned char *)b;
    unsigned char temp;
    while(data_type_size--)
    {
       temp=*p;
       *p=*q;
       *q=temp;
       p++;
       q++;
    }
}
char str[N]; 
int i,ans,j,num,sum=1,jj=1,cc=1;
void ridspace()
{
	for(i=0,j=0;i<strlen(str);i++)
		if(str[i]!=' ')str[j++]=str[i];
	str[j]='\0';
}
void readnum()
{
	num=0;
	while(str[i]>='0'&&str[i]<='9')
	{
		num=num*10+str[i]-'0';
		i++;
	}
}
int main()
{
    gets(str);
    ridspace();
    //printf("%s",str);
    i=0;
    while(i<strlen(str))
    {
    	readnum();
    	if(cc==1)sum*=num;
    	if(cc==-1)sum/=num;
    	if(str[i]=='+'||str[i]=='-')
    	{
    		ans+=sum*jj;
    		if(str[i]=='+')jj=1;
			if(str[i]=='-')jj=-1;
			cc=1;sum=1;
		}
		if(str[i]=='*')cc=1;
		if(str[i]=='/')cc=-1;
		if(str[i]=='=')ans+=sum*jj;
		i++;
	}
	printf("%d",ans);
    return 0;
}



