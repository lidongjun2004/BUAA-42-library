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
int a[10][10],b[10][10],T,r[10],l[10],g[10];
void work()
{
   for(int i=1;i<10;i++)
      for(int j=1;j<10;j++)scanf("%d",&a[i][j]);
   for(int i=1;i<10;i++)
      for(int j=1;j<10;j++)scanf("%d",&b[i][j]);
   for(int i=1;i<10;i++)
   {
	  for(int j=1;j<10;j++)r[j]=0;
	  for(int j=1;j<10;j++)
   	  {
   	  	 if(a[i][j]&&a[i][j]!=b[i][j])
   	  	 {
   	  	 	printf("Moca is so careless!\n");
   	  	 	return;
		 }
		 if(r[b[i][j]])
		 {
		 	printf("Moca is so careless!\n");
   	  	 	return;
		 }
		 r[b[i][j]]=1;
	  }
   }
   for(int i=1;i<10;i++)
   {
   	  for(int j=1;j<10;j++)l[j]=0;
   	  for(int j=1;j<10;j++)
   	  {
		 if(l[b[j][i]])
		 {
		 	printf("Moca is so careless!\n");
   	  	 	return;
		 }
		 l[b[j][i]]=1;
	  }
   }
   for(int i=1;i<=7;i+=3)
   {
	  for(int j=1;j<=7;j+=3)
   	  {
   	  	 for(int k=1;k<10;k++)g[k]=0;
   	  	 for(int ii=i;ii<=i+2;ii++)
   	  	    for(int jj=j;jj<=j+2;jj++)
   	  	    {
   	  	       if(g[b[ii][jj]])
		       {
		          printf("Moca is so careless!\n");
   	  	 	      return;
		       }
		       g[b[ii][jj]]=1;
			}
	  }
   }
   printf("Moca finish this sudoku perfectly!\n");
}
int main()
{
   scanf("%d",&T);
   while(T--)work();
   return 0;
}


