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
char s[2005],s1[2005],s2[2005];
int len;
int main()
{
   scanf("%s",&s);
   len=strlen(s);
   for(int i=0;i<len;i++)
   {
   	  s1[2*i]=s[i];
   	  s2[2*i+1]=s[i];
   }
   len*=2;
   for(int i=0;i<len;i++)
   {
   	  if(s1[i]=='0')s1[i]='o';
   	  if(s2[i]=='0')s2[i]='o';
   }
   for(int i=0;i<len;i+=2)
   {
      s1[i+1]=219-s1[len-i-2];
      s2[i]=219-s2[len-i-1];
   }
   for(int i=0;i<len/2;i++)
   {
   	  if(s1[i]<s2[i])
   	  {
		 for(int j=0;j<len/2;j++)printf("%c",s1[j]);
		 break;
	  }
   	     
   	  if(s1[i]>s2[i])
   	  {
		 for(int j=0;j<len/2;j++)printf("%c",s2[j]);
		 break;
	  }
   }
   return 0;
}


