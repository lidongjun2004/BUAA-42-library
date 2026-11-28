#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() 
{
    int n;
    cin >> n;

    vector<int> parent(n + 1, 0);
    for (int i = 2; i <= n; i++)cin >> parent[i];

    vector<ll> V(n + 1);
    for (int i = 1; i <= n; i++)cin >> V[i];

    vector<vector<int>> tree(n + 1);
    for (int i = 2; i <= n; i++)tree[parent[i]].push_back(i);

    vector<int> depth(n + 1, 0);
    vector<vector<int>> layers;

    queue<int> q;
    q.push(1);
    depth[1] = 0;

    while (!q.empty()) 
    {
        int u = q.front(); q.pop();
        if ((int)layers.size() <= depth[u])layers.resize(depth[u] + 1);
        layers[depth[u]].push_back(u);

        for (int v : tree[u]) 
        {
            depth[v] = depth[u] + 1;
            q.push(v);
        }
    }

    unordered_map<int, ll> dp_prev, dp_cur;
    ll dp_prev_none = 0;

    for (int d = 0; d < (int)layers.size(); d++) 
    {
        dp_cur.clear();

        ll max1 = dp_prev_none, max2 = LLONG_MIN;
        int id1 = -1;

        for (auto &[u, val] : dp_prev) 
        {
            if (val > max1) 
            {
                max2 = max1;
                max1 = val;
                id1 = u;
            } 
            else if (val > max2)max2 = val;
        }

        ll dp_cur_none = max1;

        for (int v : layers[d]) 
        {
            ll best_prev;
            int p = parent[v];
            if (id1 != -1 && p == id1)
                best_prev = max(dp_prev_none, max2);
            else
                best_prev = max(dp_prev_none, max1);

            dp_cur[v] = best_prev + V[v];
        }

        dp_prev = move(dp_cur);
        dp_prev_none = dp_cur_none;
    }

    ll ans = dp_prev_none;
    for (auto &[u, val] : dp_prev)ans = max(ans, val);

    cout << ans << "\n";
    return 0;
}
