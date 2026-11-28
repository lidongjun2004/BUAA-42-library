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
unsigned int b,ans;
int a,num,flag[40],cnt;
int main()
{
   scanf("%d%u",&a,&b);
   unsigned int b1=b;
   while(b1)
   {
   	  
	  if(b1&1)
	  {
	     num++;
	     flag[cnt]=1;
	  }
   	  b1=b1>>1;
   	  cnt++;
   }
   if(num>a)
   {
   	  for(int i=0;i<32;i++)
   	  {
   	  	 if(num>a)
   	  	 {
   	  	 	if(flag[i])
			{
			   num--;
			   flag[i]=0;
			}
		 }
         if(flag[i])ans+=1<<i;
      }
      printf("%u",ans);
   }
   else if(num==a)
   {
   	  printf("%u",b);
   }
   else if(num<a)
   {
   	  for(int i=0;i<32;i++)
   	  {
   	  	 if(!flag[i])
   	  	 {
   	  	 	if(num<a)
			{
			   num++;
			   flag[i]=1;
			} 
		 }
		 if(flag[i])
		 {
		 	ans+=1<<i;
		 }
	  }
	  printf("%u",ans);
   }
   return 0;
}


