#include <bits/stdc++.h>
using namespace std;

struct Edge 
{
    int u, v;
    long long w;
    bool operator<(const Edge& other) const 
    {
        return w < other.w;
    }
};

vector<int> parent, sz;

int find(int x) 
{
    if (parent[x] != x)
        parent[x] = find(parent[x]);
    return parent[x];
}

bool unite(int a, int b) 
{
    a = find(a);
    b = find(b);
    if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b);
    parent[b] = a;
    sz[a] += sz[b];
    return true;
}

int main() 
{

    int n, m;
    cin >> n >> m;

    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) 
    {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    }

    parent.resize(n + 1);
    sz.resize(n + 1, 1);
    for (int i = 1; i <= n; i++)
        parent[i] = i;

    sort(edges.begin(), edges.end());

    long long ans = 0;
    int cnt = 0;

    for (auto &e : edges) 
    {
        if (unite(e.u, e.v)) 
        {
            ans += e.w;
            cnt++;
            if (cnt == n - 1) break;
        }
    }

    cout << ans << "\n";
    return 0;
}
