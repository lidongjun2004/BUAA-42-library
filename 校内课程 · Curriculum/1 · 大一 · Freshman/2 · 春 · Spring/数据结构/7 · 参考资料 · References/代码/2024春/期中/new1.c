#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
char s[105];
int main()
{
    gets(s);
    for(int i=0;i<strlen(s);i++)
    {
    	if(s[i]==s[i+1]-1&&s[i]==s[i+2]-2)
    	{
    		printf("%c-",s[i]);
    		i=i+2;
    		while(s[i]==s[i+1]-1)i++;
    		printf("%c",s[i]);
		}
		else printf("%c",s[i]);
	}
    return 0;
}



