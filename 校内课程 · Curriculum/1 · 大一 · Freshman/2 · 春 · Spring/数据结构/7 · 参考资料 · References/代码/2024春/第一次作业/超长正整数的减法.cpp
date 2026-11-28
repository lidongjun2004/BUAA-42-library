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
void reverse(char *s)
{
    int temp,i,j;
	for(i=0,j=strlen(s)-1;i<j;i++,j--)
	{
	    temp=s[i];
		s[i]=s[j];
		s[j]=temp;
	}
}
char a[85],b[85];
int len,ans[85],flag;
void work(char *x,char *y)
{
	reverse(x);reverse(y);
	len=strlen(y);
	//printf("%d %d",len,strlen(x));return;
	for(int i=0;i<len;i++)
	{
		ans[i]=10+x[i]-y[i]-flag;
		flag=1-ans[i]/10;
		ans[i]%=10;
	}
	for(int i=len;i<strlen(x);i++)
	{
		ans[i]=10+x[i]-'0'-flag;
		flag=1-ans[i]/10;
		ans[i]%=10;
	}
	if(ans[strlen(x)-1])printf("%d",ans[strlen(x)-1]);
	for(int i=strlen(x)-2;i>=0;i--)printf("%d",ans[i]);
}
int main()
{
    gets(a);gets(b);
    if(strlen(a)==strlen(b))
    {
    	if(strcmp(a,b)>=0)work(a,b);
    	else
    	{
    		printf("-");
    		work(b,a);
		}
	}
	else if(strlen(a)>strlen(b))
	{
		work(a,b);
	}
	else
	{
		printf("-");
		work(b,a);
	}
    return 0;
}



