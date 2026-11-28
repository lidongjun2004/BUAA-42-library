#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
int n,a[N],ans;
int main()
{
	int x;
	while(scanf("%d",&a[++n])!=EOF)
	{
		for(int i=1;i<n;i++)
		{
			if(a[i]>a[n]*3)ans++; 
		}
	}
	printf("%d",ans);
    return 0;
}






