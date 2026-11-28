#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int max(int a,int b){
   if(a>b)return a;
   return b;
}
int min(int a,int b){
   if(a<b)return a;
   return b;
}
int gcd(int a,int b){
   if(b==0)return a;
   return gcd(b,a%b);
}
void swap(void *a,void *b,int data_type_size){
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
int main()
{
   char *language[] = {"FORTRAN", "BASIC", "PASCAL", "JAVA", "C"};
   printf("%s",*(language+2));
   return 0;
}



