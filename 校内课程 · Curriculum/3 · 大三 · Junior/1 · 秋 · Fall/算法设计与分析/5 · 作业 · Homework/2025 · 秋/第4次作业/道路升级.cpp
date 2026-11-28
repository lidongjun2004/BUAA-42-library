#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const ll INF = LLONG_MAX / 4;

struct Edge 
{
    int to;
    ll w;
};

int main() 
{

    int N, M, K;
    cin >> N >> M >> K;

    vector<vector<Edge>> adj(N + 1);
    for (int i = 0; i < M; i++) 
    {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        adj[u].push_back(Edge{v, w});
        adj[v].push_back(Edge{u, w});
    }

    vector<vector<ll>> dist(N + 1, vector<ll>(K + 1, INF));

    priority_queue<
        pair<ll, pair<int, int>>,
        vector<pair<ll, pair<int, int>>>,
        greater<pair<ll, pair<int, int>>>
    > pq;

    dist[1][0] = 0;
    pq.push(make_pair(0LL, make_pair(1, 0)));

    while (!pq.empty()) 
    {
        ll d = pq.top().first;
        int u = pq.top().second.first;
        int used = pq.top().second.second;
        pq.pop();

        if (d > dist[u][used]) continue;

        for (size_t i = 0; i < adj[u].size(); i++) 
        {
            int v = adj[u][i].to;
            ll w = adj[u][i].w;

            if (dist[v][used] > d + w) 
            {
                dist[v][used] = d + w;
                pq.push(make_pair(dist[v][used], make_pair(v, used)));
            }

            if (used < K && dist[v][used + 1] > d) 
            {
                dist[v][used + 1] = d;
                pq.push(make_pair(d, make_pair(v, used + 1)));
            }
        }
    }

    ll ans = INF;
    for (int k = 0; k <= K; k++)ans = min(ans, dist[N][k]);

    cout << ans << "\n";
    return 0;
}
