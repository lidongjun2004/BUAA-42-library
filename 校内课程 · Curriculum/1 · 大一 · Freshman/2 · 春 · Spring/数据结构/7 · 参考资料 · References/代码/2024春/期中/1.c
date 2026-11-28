#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 105
int n,lens,lenm;
char str[N],s[N],ans[N];
int main()
{
    scanf("%d",&n);
    scanf("%s",str);
    lenm=lens=strlen(str);
    strcpy(ans,str);
    for(int i=2;i<=n;i++)
    {
    	scanf("%s",s);
    	if(abs(lens-strlen(s))>abs(lens-lenm))
    	{
    		lenm=strlen(s);
    		strcpy(ans,s);
		}
		//printf("%s",s);
	}
	printf("%s %s %d ",str,ans,abs(lens-lenm));
	if(lenm>lens)
	{
		strcpy(s,ans);
		strcpy(ans,str);
		strcpy(str,s);
		int r=lenm;
		lenm=lens;
		lens=r;
	}
	for(int i=0,j=0;i<lens;i++,j++)
	{
		if(str[i]==ans[j])continue;
		while(str[i]!=ans[j])
		{
			printf("%c",str[i]);
			i++;
		}
	}
    return 0;
}
/*
6
computer
cmputer
cutr
ompute
computer
computerist
*/


