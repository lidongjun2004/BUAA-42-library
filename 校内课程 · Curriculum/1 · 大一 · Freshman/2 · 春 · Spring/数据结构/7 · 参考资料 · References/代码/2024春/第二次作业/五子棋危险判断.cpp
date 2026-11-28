#include<iostream>
#include<cstdio>
#include<cmath>
#include<cstring>
#include<algorithm>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
using namespace std;
int map[30][30]; 
int check(int i,int j)
{
	if(map[i][j]==map[i][j+1]&&map[i][j]==map[i][j+2]&&map[i][j]==map[i][j+3])
		if(!map[i][j-1]||!map[i][j+4])return map[i][j];
	if(map[i][j]==map[i+1][j]&&map[i][j]==map[i+2][j]&&map[i][j]==map[i+3][j])
		if(!map[i-1][j]||!map[i+4][j])return map[i][j];
	if(map[i][j]==map[i+1][j+1]&&map[i][j]==map[i+2][j+2]&&map[i][j]==map[i+3][j+3])
		if(!map[i-1][j-1]||!map[i+4][j+4])return map[i][j];
	return 0;
}
int main()
{
    for(int i=0;i<=19;i++)map[i][0]=1;
    for(int i=0;i<=19;i++)map[0][i]=1;
	for(int i=1;i<=19;i++)
       for(int j=1;j<=19;j++)scanf("%d",&map[i][j]);
    for(int i=1;i<=19;i++)
    {
    	for(int j=1;j<=19;j++)
    	{
    		if(!map[i][j])continue;
    		if(check(i,j))
    		{
    			printf("%d:%d,%d",check(i,j),i,j);
    			return 0;
			}
		}
	}
	printf("No");
    return 0;
}





