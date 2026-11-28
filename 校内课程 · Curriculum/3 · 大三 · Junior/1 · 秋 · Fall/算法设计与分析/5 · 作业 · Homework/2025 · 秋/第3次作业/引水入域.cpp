#include <bits/stdc++.h>
using namespace std;

int N, M;
int h[505][505];
bool vis[505][505];

int dx[4] = {1, -1, 0, 0};
int dy[4] = {0, 0, 1, -1};

bool inside(int x, int y) 
{
    return x >= 1 && x <= N && y >= 1 && y <= M;
}

void dfs(int x, int y) 
{
    vis[x][y] = true;
    for (int d = 0; d < 4; d++) 
    {
        int nx = x + dx[d];
        int ny = y + dy[d];
        if (inside(nx, ny) && !vis[nx][ny] && h[x][y] > h[nx][ny])dfs(nx, ny);
    }
}

int main() 
{

    cin >> N >> M;
    for (int i = 1; i <= N; i++)
        for (int j = 1; j <= M; j++)
            cin >> h[i][j];

    memset(vis, false, sizeof(vis));
    for (int j = 1; j <= M; j++)dfs(1, j);

    int unreachable = 0;
    for (int j = 1; j <= M; j++)
        if (!vis[N][j]) unreachable++;

    if (unreachable > 0) 
    {
        cout << 0 << "\n" << unreachable << "\n";
        return 0;
    }

    vector<pair<int,int>> intervals;

    for (int j = 1; j <= M; j++) 
    {
        memset(vis, false, sizeof(vis));
        dfs(1, j);

        int L = M + 1, R = 0;
        for (int k = 1; k <= M; k++) 
        {
            if (vis[N][k]) 
            {
                L = min(L, k);
                R = max(R, k);
            }
        }
        if (L <= R)
            intervals.push_back({L, R});
    }

    sort(intervals.begin(), intervals.end());

    int ans = 0;
    int pos = 1;
    int i = 0;

    while (pos <= M) 
    {
        int best = -1;
        while (i < intervals.size() && intervals[i].first <= pos) 
        {
            best = max(best, intervals[i].second);
            i++;
        }
        if (best < pos) break;
        ans++;
        pos = best + 1;
    }

    cout << 1 << "\n" << ans << "\n";
    return 0;
}
