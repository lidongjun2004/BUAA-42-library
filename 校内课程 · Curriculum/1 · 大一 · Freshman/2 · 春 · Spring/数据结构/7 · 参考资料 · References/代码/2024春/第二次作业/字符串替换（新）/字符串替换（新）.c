#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 10005
char a[N],b[N],s[N],o[N];
int lens,lena,lenb;
void small(char *p)
{
	for(int i=0;i<strlen(p);i++)
	{
		if(p[i]>='A'&&p[i]<='Z')p[i]+=32;
	}
}
int check(int x)
{
	for(int i=x,j=0;j<lena;i++,j++)
	{
		if(s[i]!=a[j])return 0;
	}
	return 1;
}
int main()
{
    FILE *in,*out;
    in=fopen("filein.txt","r");
    out=fopen("fileout.txt","w");
    gets(a);gets(b);
    lena=strlen(a);
    lenb=strlen(b);
    small(a);
	while(NULL!=fgets(s,N,in))
    {
		lens=strlen(s);
		strcpy(o,s);
		small(s);
        for(int i=0;i<lens;i++)
   	    {
   	   	    if(check(i))
   	   	    {
   	   	  	   	fprintf(out,"%s",b);
   	   	  	   	i+=lena-1;
	 	    }
	 	    else
	 	    {
	 	    	fprintf(out,"%c",o[i]);
			}
	    }
    }
    fclose(in);
    fclose(out);
    return 0;
}



