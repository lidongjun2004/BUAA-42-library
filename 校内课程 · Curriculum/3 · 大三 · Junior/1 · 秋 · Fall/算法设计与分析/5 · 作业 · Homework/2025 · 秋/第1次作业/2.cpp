#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10000005
using namespace std;
ll h[N],a,ans,cnt,max_num,num;
int main()
{
	while(scanf("%lld",&a)!=EOF)
	{
		h[a]++;
		if(a>max_num)max_num=a;
		num++;
	}
	for(int i=0;i<=max_num;i++)
	{
		if(h[i]>cnt)
		{
			cnt=h[i];
			ans=i;
		}
	}
	printf("%lld",ans);
    return 0;
}






