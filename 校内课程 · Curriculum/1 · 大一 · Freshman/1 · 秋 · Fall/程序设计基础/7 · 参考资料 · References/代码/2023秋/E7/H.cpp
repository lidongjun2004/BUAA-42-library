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
char str1[10005],str2[10005];
int op,len1,len2,a,b;
int check(int ii)
{
   for(int i=0;i<len2;i++)
      if(str1[i+ii]!=str2[i])return 0;
   return 1;
}
void work1()
{
   scanf("%s",&str2);
   len1=strlen(str1);
   len2=strlen(str2);
   for(int i=len1;i<len1+len2;i++)str1[i]=str2[i-len1];
}
void work2(int ii)
{
   len1=strlen(str1);
   for(int i=ii;i<len1;i++)str1[i]=NULL;
}
void work3(int ii)
{
   scanf("%s",&str2);
   len1=strlen(str1);
   len2=strlen(str2);
   for(int i=len1+len2-1;i>ii+len2;i--)str1[i]=str1[i-len2];
   for(int i=ii+1;i<=ii+len2;i++)str1[i]=str2[i-ii-1];
}
void work4(int ii,int jj)
{
   len1=strlen(str1);
   for(int i=ii;i<=jj;i++)str1[i]=str1[jj+i+1-ii];
   for(int i=len1-(jj-ii+1);i<len1;i++)str1[i]=NULL;
}
void work5(int ii,int jj)
{
	work4(ii,jj);work3(ii-1);
}
void work6()
{
   scanf("%s",&str2);
   len1=strlen(str1);
   len2=strlen(str2);
   if(len2>len1)
   {
   	  printf("NULL\n");
   	  return;
   }
   int flag=0;
   for(int i=0;i<=len1-len2;i++)
      if(check(i))
      {
      	 printf("%d ",i);
      	 flag=1;
      	 break;
	  }
   for(int i=len1-len2;i>=0;i--)
      if(check(i))
      {
      	 printf("%d\n",i);
      	 flag=1;
      	 break;
	  }
   if(!flag)printf("NULL\n");
}
int main()
{
   scanf("%s",&str1);
   while(scanf("%d",&op)!=EOF)
   {
   	  if(op==1)work1();
   	  if(op==2)
	  {
	  	 scanf("%d",&a);
		 work2(a);
	  }
   	  if(op==3)
	  {
	  	 scanf("%d",&a);
		 work3(a);
	  }
   	  if(op==4)
   	  {
	  	 scanf("%d%d",&a,&b);
		 work4(a,b);
	  }
   	  if(op==5)
   	  {
   	  	 scanf("%d%d",&a,&b);
		 work5(a,b);
	  }
   	  if(op==6)work6();
   }
   printf("%s\n",str1);
   return 0;
}


