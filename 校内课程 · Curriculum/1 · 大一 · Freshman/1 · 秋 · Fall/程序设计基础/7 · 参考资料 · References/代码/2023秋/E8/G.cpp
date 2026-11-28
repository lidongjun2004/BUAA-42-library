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
int n,m;
int col[11],rank[1005],vol[1005][11],a[1005],ans[1005];
char stu[1005][10];
int main()
{
   scanf("%d%d",&n,&m);
   for(int i=1;i<=m;i++)scanf("%d",&col[i]);
   for(int i=1;i<=n;i++)
   {
   	  scanf("%s%d",&stu[i],&rank[i]);
   	  a[rank[i]]=i;
   	  for(int j=1;j<=m;j++)scanf("%d",&vol[i][j]);
   }
   for(int i=1;i<=m;i++)
   {
   	  for(int j=1;j<=n;j++)
   	  {
   	  	 if(ans[a[j]])continue;
		 if(col[vol[a[j]][i]])
   	  	 {
   	  	 	ans[a[j]]=vol[a[j]][i];
   	  	 	col[vol[a[j]][i]]--;
		 }
	  }
   }
   for(int i=1;i<=n;i++)
   {
   	  printf("%s %d\n",stu[a[i]],ans[a[i]]);
   }
   return 0;
}


