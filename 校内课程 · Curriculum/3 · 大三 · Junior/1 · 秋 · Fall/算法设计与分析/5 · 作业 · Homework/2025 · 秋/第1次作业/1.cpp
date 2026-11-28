#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10000005
using namespace std;
ll n,a=1,b,c;
ll MOD=998244353; 
int main()
{
	scanf("%lld",&n);
	for(ll i=2;i<=n;i++)
	{
		c=((i-1)%MOD*(a%MOD+b%MOD)%MOD)%MOD;
		a=b;b=c;
	}
	printf("%lld",c%MOD);
    return 0;
}






