import heapq

def manhattan(state, goal, size):
    distance = 0
    for i in range(len(state)):
        if state[i] == 0:
            continue
        xi, yi = divmod(i, size)
        xg, yg = divmod(goal.index(state[i]), size)
        distance += abs(xi - xg) + abs(yi - yg)
    return distance

def is_solvable(puzzle, size):
    inv_count = 0
    puzzle_no_zero = [x for x in puzzle if x != 0]
    for i in range(len(puzzle_no_zero)):
        for j in range(i+1, len(puzzle_no_zero)):
            if puzzle_no_zero[i] > puzzle_no_zero[j]:
                inv_count += 1
    if size % 2 == 1:
        return inv_count % 2 == 0
    else:
        row = puzzle.index(0) // size
        return (inv_count + row) % 2 == 1

def get_neighbors(state, size):
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, size)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            ni = nx * size + ny
            new_state = list(state)
            new_state[zero_index], new_state[ni] = new_state[ni], new_state[zero_index]
            neighbors.append(tuple(new_state))
    return neighbors

def a_star(start, goal, size):
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal, size), 0, start, []))
    visited = set()
    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            return path + [current]
        for neighbor in get_neighbors(current, size):
            if neighbor not in visited:
                heapq.heappush(open_set, (
                    g + 1 + manhattan(neighbor, goal, size),
                    g + 1,
                    neighbor,
                    path + [current]
                ))
    return None
