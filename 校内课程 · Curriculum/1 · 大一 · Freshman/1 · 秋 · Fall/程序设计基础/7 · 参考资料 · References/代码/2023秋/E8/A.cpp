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
int h,h1,h2; 
int main()
{
   scanf("%d",&h);
   h1=h*2/3;
   h2=h/3;
   for(int i=1;i<=h1;i++)
   {
   	  for(int j=1;j<=h1-i;j++)
   	  {
   	  	 printf(" ");
	  }
	  for(int j=1;j<=2*i-1;j++)printf("*");
	  printf("\n");
   }
   for(int i=1;i<=h2;i++)
   {
   	  for(int j=1;j<=h1-(h2/4)-1;j++)printf(" ");
   	  for(int j=1;j<=(h2/4)*2+1;j++)printf("|");
   	  printf("\n");
   }
   return 0;
}


