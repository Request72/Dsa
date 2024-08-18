import random

def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # return to the starting point
    return total_distance

def swap_two_cities(route, i, j):
    new_route = route[:]
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def hill_climbing_tsp(distance_matrix):
    n = len(distance_matrix)
    current_route = list(range(n))
    random.shuffle(current_route)
    
    current_distance = calculate_total_distance(current_route, distance_matrix)
    
    while True:
        best_route = current_route[:]
        best_distance = current_distance
        
        for i in range(n):
            for j in range(i + 1, n):
                neighbor_route = swap_two_cities(current_route, i, j)
                neighbor_distance = calculate_total_distance(neighbor_route, distance_matrix)
                
                if neighbor_distance < best_distance:
                    best_route = neighbor_route
                    best_distance = neighbor_distance
        
        if best_distance < current_distance:
            current_route = best_route
            current_distance = best_distance
        else:
            break
    
    return current_route, current_distance

# Example usage
distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

best_route, best_distance = hill_climbing_tsp(distance_matrix)
print("Best route:", best_route)
print("Total distance:", best_distance)
