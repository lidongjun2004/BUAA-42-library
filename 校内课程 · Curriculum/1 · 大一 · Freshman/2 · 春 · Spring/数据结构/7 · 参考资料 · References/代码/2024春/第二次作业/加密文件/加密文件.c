#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10005
char word[55],code[27],ch;
int hash[27],len;
void uncopy()
{
    for(int i=0;i<strlen(word);i++)
    {
   	    if(!hash[word[i]-96])
   	    {
   	    	code[len++]=word[i];
   	    	hash[word[i]-96]=1;
	    }
    }
    for(int i=26;i>=1;i--)
    {
    	if(!hash[i])code[len++]=i+96;
	}
}
int main()
{
    FILE *in=fopen("encrypt.txt","r"),*out=fopen("output.txt","w");
    scanf("%s",word);
    uncopy();
//    printf("%d\n%s",len,code);
    while((ch=fgetc(in))!=EOF)
    {
    	if(ch>='a'&&ch<='z')fprintf(out,"%c",code[ch-97]);
    	else fprintf(out,"%c",ch);
	}
    fclose(in);
    fclose(out);
    return 0;
}



