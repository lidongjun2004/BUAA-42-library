#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10000005
#define min(a,b) a<b?a:b
char str[105],s[105];
int m,n,len,flag;
int main()
{
    scanf("%s\n",s);
    if(s[1]!='-')
    {
    	flag=1;
    	sscanf(s,"%%%d:%dS",&m,&n); 
	}
    else sscanf(s,"%%-%d:%dS",&m,&n); 
    while(str[len-1]!='\n')
    {
    	str[len++]=getchar();
	}
	len--;
	str[len]='\0';
    m=min(len,m);
    if(flag==0)
    {
		for(int i=m;i<n;i++)printf("#");
		for(int i=0;i<m;i++)printf("%c",str[i]);
	}
	else
	{
		for(int i=0;i<m;i++)printf("%c",str[i]);
		for(int i=m;i<n;i++)printf("#");
	}
	
    return 0;
}



