#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 100005
int map[30][30]; 
int check(int i,int j)
{
	if(map[i][j]==map[i][j+1]&&map[i][j]==map[i][j+2]&&map[i][j]==map[i][j+3])
		if(map[i][j-1]==0||map[i][j+4]==0)return map[i][j];
	if(map[i][j]==map[i+1][j]&&map[i][j]==map[i+2][j]&&map[i][j]==map[i+3][j])
		if(map[i-1][j]==0||map[i+4][j]==0)return map[i][j];
	if(map[i][j]==map[i+1][j+1]&&map[i][j]==map[i+2][j+2]&&map[i][j]==map[i+3][j+3])
		if(map[i-1][j-1]==0||map[i+4][j+4]==0)return map[i][j];
	if(i>=4)
	    if(map[i][j]==map[i+1][j-1]&&map[i][j]==map[i+2][j-2]&&map[i][j]==map[i+3][j-3])
		    if(map[i-1][j+1]==0||map[i+4][j-4]==0)return map[i][j];
	return 0;
}
int main()
{
    for(int i=0;i<=19;i++)map[i][0]=3;
    for(int i=0;i<=19;i++)map[0][i]=3;
	for(int i=1;i<=19;i++)
       for(int j=1;j<=19;j++)scanf("%d",&map[i][j]);
    for(int i=1;i<=19;i++)
    {
    	for(int j=1;j<=19;j++)
    	{
    		int flag=check(i,j);
    		if(flag)
    		{
    			printf("%d:%d,%d",flag,i,j);
    			return 0;
			}
		}
	}
	printf("No");
    return 0;
}





