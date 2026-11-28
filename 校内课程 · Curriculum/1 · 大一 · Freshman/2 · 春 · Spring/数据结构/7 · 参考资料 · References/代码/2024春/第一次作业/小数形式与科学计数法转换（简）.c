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
char str[105];
int main()
{
    gets(str);
    if(str[0]=='0')
    {
    	int i=2,sum=1;
		while(str[i++]=='0')sum++;
		i--;
		printf("%c",str[i]);
		if(i!=strlen(str)-1)printf(".");
		for(i++;i<strlen(str);i++)printf("%c",str[i]);
		printf("e-%d",sum);
	}
	else
	{
		int i=1,sum=0;
		printf("%c",str[0]);
		while(str[i++]!='.')sum++;
		printf(".");
		for(i=1;i<strlen(str);i++)
		    if(str[i]!='.')printf("%c",str[i]);
		printf("e%d",sum);
	}
    return 0;
}



