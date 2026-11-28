#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define eps 1e-6
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
int id[100005],time[100005],n=1;
double score[100005];
char name[100005][10];
int cmp(const void* a,const void* b)
{
   int i=*(int*)a,j=*(int*)b;
   if(score[i]-score[j]>eps)return -1;
   if(score[i]-score[j]<-eps)return 1;
   if(time[i]>time[j])return 1;
   if(time[i]<time[j])return -1;
}
int main()
{
   while(scanf("%s",&name[n])!=EOF)
   {
   	  getchar();
	  id[n]=n;
	  n++;
   }
   n--;
   qsort(id+1,n,sizeof(int),cmp);
   for(int i=1;i<=n;i++)printf("%10s %8.2f %10d\n",name[id[i]],score[id[i]],time[id[i]]);
   return 0;
}
