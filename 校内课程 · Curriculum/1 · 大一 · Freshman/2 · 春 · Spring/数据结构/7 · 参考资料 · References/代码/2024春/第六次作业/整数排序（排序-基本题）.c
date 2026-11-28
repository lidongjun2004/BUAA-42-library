/*
20 3
38 356 98 -102 126 46 65 -9 100 0 21 2 90 8 18 12 78 16 189 23
*/
#include<stdio.h>
#include<math.h>
#include<string.h>
#include<stdlib.h>
#define ll long long
#define uint unsigned int
#define ull unsigned long long
#define N 1000005
int n,op,cnt;
int a[105],b[105];
void sort1()
{
    for(int i=1;i<n;i++)
	{
        int k=i;
        for(int j=i+1;j<=n;j++)
		{
            if(a[j]<a[k])k=j;
            cnt++;
        }

        if(k!=i)
		{
            int t=a[k];
            a[k]=a[i];
            a[i]=t;
        }
    }
}
void sort2()
{
    int flag=1;
    for(int i=n;i>1&&flag==1;i--)
	{
        flag=0;
        for(int j=1;j<i;j++)
		{
            if(a[j]>a[j+1])
			{
                int t=a[j];
                a[j]=a[j+1];
                a[j+1]=t;
                flag=1;
            }
            cnt++;
        }
    }
}
void adjust(int k[],int i,int n)
{
    int j,temp;
    temp=k[i];
    j=2*i+1;
    while(j<n)
	{
		cnt++;
        if(j<n-1&&k[j]<k[j+1])j++;
        if(temp>=k[j])break;
        k[(j-1)/2]=k[j];
        j=2*j+1;
    }
    k[(j-1)/2]=temp;
}
void sort3(int a[])
{
    for(int i=n/2-1;i>=0;i--)adjust(a,i,n);
    for(int i=n-1;i>=1;i--)
	{
        int t=a[i];
        a[i]=a[0];
        a[0]=t;
        adjust(a,0,i);
    }
}
void merge(int x[],int tmp[],int left,int leftend,int rightend)
{     
    int i=left,j=leftend+1,q=left;
    while(i<=leftend&&j<=rightend)
    {
    	cnt++;
        if(x[i]<=x[j])tmp[q++]=x[i++];
        else tmp[q++]=x[j++];
    }
    while(i<=leftend)tmp[q++]=x[i++];
    while(j<=rightend)tmp[q++]=x[j++];
    for(i=left;i<=rightend;i++)x[i]=tmp[i];
}
void sort4(int a[],int s,int e,int b[])
{
    if(s<e)
	{
        int m=s+(e-s)/2;
        sort4(a,s,m,b);
        sort4(a,m+1,e,b);
        merge(a,b,s,m,e);
    }
}
void swap(int *p,int *q)
{
	int t=*p;
	*p=*q;
	*q=t;
}
void quickSort(int k[],int left,int right)
{     
    int i,last;
    if(left<right)
	{
        last=left; 
        for(i=left+1;i<=right;i++)
        {
        	cnt++;
        	if(k[i]<k[left])
                swap(&k[++last],&k[i]); 
		}
            
        swap(&k[left],&k[last]);
        quickSort(k,left,last-1); 
        quickSort(k,last+1,right);   
    }
}
int main()
{
    scanf("%d%d",&n,&op);
    for(int i=1;i<=n;i++)scanf("%d",&a[i]);
    
    if(op==1)sort1();
    if(op==2)sort2();
    if(op==3)sort3(a+1);
    if(op==4)sort4(a,1,n,b);
    if(op==5)quickSort(a,1,n);
    for(int i=1;i<=n;i++)printf("%d ",a[i]);
    printf("\n%d",cnt);
    return 0;
}



