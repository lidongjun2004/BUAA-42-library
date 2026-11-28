#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
char str[2005];
int dp[1005][1005];
int main()
{
	scanf("%s",str);
	char *comma=strchr(str,',');
	int len1=comma-str;
	int len2=strlen(str)-len1-1;
	char s1[1005],s2[1005];
	strncpy(s1,str,len1);
	strncpy(s2,str+len1+1,len2);
	s1[len1]=0;s2[len2]=0;
	for(int i=1;i<=len1;i++)
	{
		for(int j=1;j<=len2;j++)
		{
			if(s1[i-1]==s2[j-1])dp[i][j]=dp[i-1][j-1]+1;
			else dp[i][j]=max(dp[i-1][j],dp[i][j-1]);
		}
	}
	printf("%d",dp[len1][len2]);
    return 0;
}






