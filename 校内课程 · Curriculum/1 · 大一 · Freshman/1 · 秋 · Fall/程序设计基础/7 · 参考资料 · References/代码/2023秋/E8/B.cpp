#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
int max(int a,int b)
{
   if(a>b)return a;
   return b;
}
int min(int a,int b)
{
   if(a<b)return a;
   return b;
}
int gcd(int a,int b)
{
   if(b==0)return a;
   return gcd(b,a%b);
}
void swap(void *a,void *b,int data_type_size)
{
   unsigned char *p=(unsigned char *)a;
   unsigned char *q=(unsigned char *)b;
   unsigned char temp;
   while(data_type_size--)
   {
      temp=*p;
      *p=*q;
      *q=temp;
      p++;
      q++;
   }
}
void sort(int *arr,int left,int right)
{
   if(left>right)return;
   int tmp=arr[left];
   int i=left;
   int j=right;
   while(i!=j)
   {
      while(arr[j]>=tmp&&j>i)j--;
      while(arr[i]<=tmp&&j>i)i++;
      if(j>i)
      {
         int t=arr[i];
         arr[i]=arr[j];
         arr[j]=t;
      }
   }
   arr[left]=arr[i];
   arr[i]=tmp;
   sort(arr,left,i-1);
   sort(arr,i+1,right);
}
int T,sx,sy,ex,ey,x,y,len,sum,flag;
char s[1005];
int main()
{
   scanf("%d",&T);
   while(T--)
   {
   	  scanf("%d%d%d%d",&sx,&sy,&ex,&ey);
   	  x=ex-sx;
   	  y=ey-sy;sum=0;flag=1;
	  scanf("%s",&s);
	  len=strlen(s);
	  for(int i=0;i<len;i++)
	  {
	  	 if(s[i]=='N'&&y>0){sum++;y--;}
	  	 if(s[i]=='W'&&x<0){sum++;x++;}
	  	 if(s[i]=='S'&&y<0){sum++;y++;}
	  	 if(s[i]=='E'&&x>0){sum++;x--;}
	  	 if(x==0&&y==0)
	  	 {
	  	 	printf("%d\n",sum);
	  	 	
			   flag=0;break;
	  	 	
		 }
	  }
	  if(flag)printf("We want to live in Gensokyo forever...\n");
   }
   return 0;
}


