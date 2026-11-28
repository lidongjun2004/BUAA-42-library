#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
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
char s[10005];
int k,a[10005],len;
int cmp(const void* a,const void* b)
{
   int i=*(int*)a,j=*(int*)b;
   return strcmp(&s[i-1],&s[j-1]);
}
int main()
{
   scanf("%s%d",&s,&k);
   len=strlen(s);
   for(int i=1;i<=len;i++)a[i]=i;
   qsort(a+1,len,sizeof(int),cmp);
   printf("%s",&s[a[k]-1]);
   return 0;
}


