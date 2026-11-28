#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (ll)1e18;

struct Edge 
{
    int to;
    ll cap;
    int rev;
};

struct Dinic 
{
    int n;
    vector<vector<Edge>> g;
    vector<int> level, it;

    Dinic(int n) : n(n), g(n), level(n), it(n) {}

    void addEdge(int u, int v, ll cap) 
    {
        g[u].push_back({v, cap, (int)g[v].size()});
        g[v].push_back({u, 0, (int)g[u].size() - 1});
    }

    bool bfs(int s, int t) 
    {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        while (!q.empty()) 
        {
            int u = q.front(); q.pop();
            for (auto &e : g[u]) 
            {
                if (e.cap > 0 && level[e.to] < 0) 
                {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[t] >= 0;
    }

    ll dfs(int u, int t, ll f) 
    {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)g[u].size(); i++) 
        {
            auto &e = g[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) 
            {
                ll ret = dfs(e.to, t, min(f, e.cap));
                if (ret > 0) 
                {
                    e.cap -= ret;
                    g[e.to][e.rev].cap += ret;
                    return ret;
                }
            }
        }
        return 0;
    }

    ll maxFlow(int s, int t) 
    {
        ll flow = 0;
        while (bfs(s, t)) 
        {
            fill(it.begin(), it.end(), 0);
            while (ll f = dfs(s, t, INF)) 
            {
                flow += f;
            }
        }
        return flow;
    }
};

int main() 
{

    int m, n;
    cin >> m >> n;

    vector<vector<ll>> a(m, vector<ll>(n));
    ll total = 0;
    for (int i = 0; i < m; i++)
    {
        for (int j = 0; j < n; j++) 
        {
            cin >> a[i][j];
            total += a[i][j];
        }
    }

    int S = m * n;
    int T = m * n + 1;
    Dinic dinic(m * n + 2);

    auto id = [&](int i, int j) 
    {
        return i * n + j;
    };

    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};

    for (int i = 0; i < m; i++) 
    {
        for (int j = 0; j < n; j++) 
        {
            int u = id(i, j);
            if ((i + j) % 2 == 0) 
            {
                dinic.addEdge(S, u, a[i][j]);
                for (int d = 0; d < 4; d++) 
                {
                    int ni = i + dx[d], nj = j + dy[d];
                    if (ni >= 0 && ni < m && nj >= 0 && nj < n) 
                    {
                        int v = id(ni, nj);
                        dinic.addEdge(u, v, INF);
                    }
                }
            } 
            else 
            {
                dinic.addEdge(u, T, a[i][j]);
            }
        }
    }

    ll minCover = dinic.maxFlow(S, T);
    cout << total - minCover << "\n";

    return 0;
}
