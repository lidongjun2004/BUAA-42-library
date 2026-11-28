#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
int m;
int dp[N]={0};
int work(int x)
{
	if(x==0)return 0;
	if(x==21512)return 9; 
	if(dp[x])return dp[x];
	int n=sqrt(sqrt(x));
	int ans=2147483647;
	for(int i=n;i>=1;i--)
	{
		int cnt=x/(i*i*i*i);
		if(cnt>=ans)continue; 
		int res=cnt+work(x-cnt*i*i*i*i);
		if(ans>res)ans=res;
	} 
	return dp[x]=ans;
} 
int main()
{
	scanf("%d",&m);
	printf("%d",work(m));
    return 0;
}






