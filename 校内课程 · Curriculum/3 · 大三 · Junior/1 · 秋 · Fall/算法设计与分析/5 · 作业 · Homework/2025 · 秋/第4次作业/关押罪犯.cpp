#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int u, v;
    long long w;
};

const int MAXN = 200000 + 5;

int fa[MAXN];
int parity[MAXN];
int find(int x) 
{
    if (fa[x] == x) return x;
    int root = find(fa[x]);
    parity[x] ^= parity[fa[x]];
    return fa[x] = root;
}

int main() 
{

    int N, M;
    cin >> N >> M;

    vector<Edge> edges(M);
    for (int i = 0; i < M; i++) 
    {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    sort(edges.begin(), edges.end(),
         [](const Edge &a, const Edge &b) 
         {
             return a.w > b.w;
         });

    for (int i = 1; i <= N; i++) 
    {
        fa[i] = i;
        parity[i] = 0;
    }

    for (auto &e : edges) 
    {
        int u = e.u, v = e.v;
        long long w = e.w;

        int fu = find(u);
        int fv = find(v);

        if (fu == fv) 
        {
            if (parity[u] == parity[v]) 
            {
                cout << w << "\n";
                return 0;
            }
        } 
        else
        {

            fa[fu] = fv;
            parity[fu] = parity[u] ^ parity[v] ^ 1;
        }
    }

    cout << 0 << "\n";
    return 0;
}
