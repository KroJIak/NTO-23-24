from collections import deque

def bfs(mergeList, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current not in visited:
            neighbors = mergeList[current]
            for neighbor in neighbors:
                if neighbor == end: return path + [neighbor]
                else: queue.append((neighbor, path + [neighbor]))
            visited.add(current)
    return []

# Пример использования
mergeList = {
    'p_1': ['p_2', 'p_3'],
    'p_2': ['p_1', 'p_3', 'p_4'],
    'p_3': ['p_1', 'p_2', 'p_4'],
    'p_4': ['p_2', 'p_3']
}

start_point = 'p_1'
end_point = 'p_4'

result = bfs(mergeList, start_point, end_point)
print(result)
