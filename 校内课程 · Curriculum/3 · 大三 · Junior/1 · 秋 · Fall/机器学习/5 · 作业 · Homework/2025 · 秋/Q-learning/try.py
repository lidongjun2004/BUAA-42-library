import numpy as np

states = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
n_states = len(states)

R = np.array([
    [-1, -1, -1, -1,  0, -1, -1, -1],  
    [-1, -1,  0, -1, -1,  0, -1, -1],  
    [-1,  0, -1,100, -1, -1,  0, -1],  
    [-1, -1,  0, -1, -1, -1, -1, -1],  
    [ 0, -1, -1, -1, -1,  0, -1, -1],  
    [-1,  0, -1, -1,  0, -1,  0, -1],  
    [-1, -1,  0, -1, -1,  0, -1,  0],  
    [-1, -1, -1, -1, -1, -1,  0, -1]   
])

Q = np.zeros((n_states, n_states))

alpha = 0.8    
gamma = 0.95  
n_episodes = 1000

for episode in range(n_episodes):
    current_state = np.random.randint(0, n_states)
    while current_state == 3:
        current_state = np.random.randint(0, n_states)
    
    while True:
        possible_actions = np.where(R[current_state, :] >= 0)[0]
        if len(possible_actions) == 0:
            break 
        
        action = possible_actions[np.random.randint(0, len(possible_actions))]
        
        Q[current_state, action] += alpha * (
            R[current_state, action] + gamma * np.max(Q[action, :]) - Q[current_state, action]
        )
        
        current_state = action
        
        if current_state == 3:
            break

print("=== 训练后的Q矩阵 ===")
print("=" * 70)

# 创建更美观的Q矩阵显示
header = "     " + " ".join([f"{state:>8}" for state in states])
print(header)
print("    " + "-" * (len(states) * 9 + 1))

for i, state in enumerate(states):
    row_str = f"{state} | "
    for j in range(n_states):
        if Q[i, j] == 0:
            row_str += "    -    "
        else:
            row_str += f"{Q[i, j]:>8.2f}"
        if j < n_states - 1:
            row_str += " "
    print(row_str)

print("\n=== 从各房间到D的导航路径 ===")
for i in range(n_states):
    if i == 3:
        print(f"从 {states[i]} 出发：['D']（已在目标）")
    else:
        path = []
        current = i
        path.append(states[current])
        
        visited = set()
        visited.add(current)
        
        while current != 3 and len(visited) <= n_states:
            next_state = np.argmax(Q[current, :])
            if next_state in visited:  # 防止循环
                break
            path.append(states[next_state])
            visited.add(next_state)
            current = next_state
            
        print(f"从 {states[i]} 出发：{path}")

print("\n=== 各状态的最佳动作 ===")
for i in range(n_states):
    if i == 3:
        print(f"{states[i]}: 目标状态")
    else:
        best_action_idx = np.argmax(Q[i, :])
        if Q[i, best_action_idx] > 0:
            print(f"{states[i]} -> {states[best_action_idx]} (Q值: {Q[i, best_action_idx]:.2f})")
        else:
            print(f"{states[i]}: 无有效路径")