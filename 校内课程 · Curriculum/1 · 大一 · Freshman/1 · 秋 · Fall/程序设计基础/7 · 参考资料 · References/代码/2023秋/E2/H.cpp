#include<stdio.h>
#include<math.h>
#include<string.h>
int vis[30000000];
int main()
{
   int n,num;
   char ch;
   scanf("%d",&n);getchar();
   for(int i=1;i<=n;i++)
   {
   	  num=0;
	  scanf("%c",&ch);
	  num=num*100+(int)(ch-96);
	  scanf("%c",&ch);
	  num=num*100+(int)(ch-96);
	  scanf("%c",&ch);
	  num=num*100+(int)(ch-96);
	  scanf("%c",&ch);
	  num=num*100+(int)(ch-96);
	  getchar();
	  if(vis[num]>0)printf("Moca has already memorized this word!\n");
	  else printf("Moca memorized a new word!\n");
	  vis[num]++;
   }
   return 0;
}

