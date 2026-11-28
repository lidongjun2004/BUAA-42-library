#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
int n,ans; 
int main()
{
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		int a;
		cin>>a;
		ans^=a;
	}
	cout<<ans; 
    return 0;
}






