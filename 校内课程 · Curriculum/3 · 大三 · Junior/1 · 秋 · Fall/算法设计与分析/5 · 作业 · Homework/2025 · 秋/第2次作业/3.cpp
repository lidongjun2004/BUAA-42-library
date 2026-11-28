#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 2005
using namespace std;
int n,m,x;
int dp[N][N],a[N][N],ans; 
int main()
{
	char c=',';
	while(c==',')
	{
		scanf("%c",&c);
		n++;
		while(c!=','&&c!='\r'&&c!='\n')
		{
			if(c=='0'||c=='1')a[n][++x]=c-48;
			scanf("%c",&c);
		}
		m=x;
		x=0;
	}
	for(int i=1;i<=n;i++)
	{
		for(int j=1;j<=m;j++)
		{
			if(!a[i][j])continue;
			dp[i][j]=min(min(dp[i-1][j],dp[i][j-1]),dp[i-1][j-1])+1;
			ans=max(ans,dp[i][j]);
		}
	}
	printf("%d",ans*ans);
    return 0;
}






