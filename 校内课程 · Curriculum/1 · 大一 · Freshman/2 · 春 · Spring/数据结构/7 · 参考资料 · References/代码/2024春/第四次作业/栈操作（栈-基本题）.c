#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 105
int stack[N],top,op,data;
int main()
{
    while(1)
    {
    	scanf("%d",&op);
    	if(op==1)
    	{
    		scanf("%d",&data);
    		if(top==100)printf("error ");
			else stack[++top]=data;
		}
		if(op==0)
		{
			if(top==0)printf("error ");
			else printf("%d ",stack[top--]);
		}
		if(op==-1)break;
	}
    return 0;
}



