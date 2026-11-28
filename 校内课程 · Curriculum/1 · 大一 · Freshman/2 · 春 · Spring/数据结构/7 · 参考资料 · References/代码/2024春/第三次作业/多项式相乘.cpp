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
	ll xi;
	ll mi;
}term;
term a[N],b[N],ans[N];
ll in1,in2=1,numa,numb;
void checkin()
{
	for(int i=1;i<=numa;i++)printf("%lld %lld ",a[i].xi,a[i].mi);
	printf("\n");
	for(int i=1;i<=numb;i++)printf("%lld %lld ",b[i].xi,b[i].mi);
	printf("\n");
}
int main()
{
    while(in2)
    {
    	scanf("%lld%lld",&in1,&in2);
        a[++numa].xi=in1;
        a[numa].mi=in2;
	}
	in2=1;
	while(in2)
    {
    	scanf("%lld%lld",&in1,&in2);
        b[++numb].xi=in1;
        b[numb].mi=in2;
	}
	checkin();
    return 0;
}



