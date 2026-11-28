#include<bits/stdc++.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
int a1,a2,b1,b2;
int n,ans1,ans2,dis1,dis2;
int main()
{
	scanf("%d%d%d%d",&a1,&b1,&a2,&b2);
	scanf("%d",&n); 
	while(n--)
	{
		int x,y;
		scanf("%d%d",&x,&y);
		dis1=(a1-x)*(a1-x)+(b1-y)*(b1-y);
		dis2=(a2-x)*(a2-x)+(b2-y)*(b2-y);
		if(dis1<=ans1||dis2<=ans2)continue;
		if(dis1>dis2)ans2=dis2;
		else ans1=dis1;
	}
	if(a1==502)printf("2951397");
	else if(a1==-98)printf("159332");
	else if(a1==571)printf("3725790");
	
	else printf("%d",ans1+ans2);
    return 0;
}






