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
int n,cnt[11],num[11],len;
void work()
{
	if(len==n)
	{
		for(int i=1;i<=n;i++)printf("%d ",num[i]);
		printf("\n");
		return;
	}
	for(int i=1;i<=n;i++)
	{
		if(cnt[i])continue;
		num[++len]=i;
		cnt[i]++;
		work();
		cnt[i]--;
		len--;
	}
}
int main()
{
    scanf("%d",&n);
    work();
    return 0;
}



