#include <stdio.h>
#include <string.h>
int main() 
{
	int n;
	scanf("%d",&n);
	while(n--)
	{
		int m,a,b;
		scanf("%d%d%d",&m,&a,&b);
		int l=m-a,r=m-a/4+a%4;
		if(l<0) l=(l%3+3)%3;
		int ok=0;
		if(l<=20) 
		{
			for (int i=l;i<=20&&i<=r;i+=3)
			{
				if(i==1)
				{
					if (b==2||b==3||b==5||b==6)
					{puts("Yes");ok=1;break;}
				} else if (2*i<=b&&6*i>=b)
					{puts("Yes");ok=1;break;}
			}
			if(r<=20&&!ok) {puts("No");continue;}
		}
		if(ok) continue;
		if(l<=20) l=21;
		if(l>r) {puts("No");continue;}
		int L=2*l,R=6*r;
		if(L<=b&&b<=R) puts("Yes");
		else puts("No");
	}
	return 0;
}
