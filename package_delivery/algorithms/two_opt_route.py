def two_opt_swap(route, i, j):
    """
    Reverses the order of vertices between indices i and j in the given route.

    Args:
        route (list): A list of vertices representing a route.
        i (int): The starting index of the vertices to be reversed.
        j (int): The ending index of the vertices to be reversed.

    Returns:
        list: A new list of vertices with the order of vertices between indices i and j reversed.
    """
    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
    return new_route


def calculate_route_distance(route, graph):
    """
    Calculates the total distance of a given route on a graph.

    Parameters:
    route (list): A list representing the vertices of the route.
    graph (Graph): An object representing the graph of locations and distances between them.

    Returns:
    int: The total distance of the route.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        from_vertex = route[i]
        to_vertex = route[i + 1]
        total_distance += graph.get_edge_weight[from_vertex][to_vertex]
    return total_distance


# Remove repeated vertices in the route list to optimize the route for the truck
def remove_repeated_vertices(route):
    """
    Remove repeated vertices from a given route.

    Args:
        route (list): A list of vertices representing a route.

    Returns:
        list: A copy of the route list with repeated vertices removed.
    """
    # Create a new list with first vertex from the current route
    unique_route = [route[0]]
    for vertex in route:
        # If the current vertex is different from the last vertex added to the unique route,
        # then add the current vertex to the unique route list
        if vertex != unique_route[-1]:
            unique_route.append(vertex)
    return unique_route.copy()


# Implement the two-opt algorithm, brute force approach, optimize the order of addresses in route in
# conjunction to utilizing dijkstra's algorithm
# Used to further decrease the total_distance traveled by the three trucks after the nearest neighbor algorithm
# Starts at the hub, 4001 South 700 East, and ends at the hub
def two_opt_route(trucks, graph):
    """
    Optimize the route even further after nearest-neighbor algorithm of trucks using the 2-opt algorithm.

    Args:
        trucks (Truck): The trucks to optimize.
        graph (Graph): The graph representing the locations and distances.

    Returns:
        None
    """
    # Only unique address on the route list (excluding hub)
    unique_route = [vertex for vertex in remove_repeated_vertices(trucks.route) if vertex != '4001 South 700 East']
    # Initialize the unique_route to the current_route
    current_route = ['4001 South 700 East'] + unique_route + ['4001 South 700 East']
    # Will be the best-optimized route
    best_route = current_route
    improvement = True
    # Continue to optimize until no further improvements are made
    while improvement:
        improvement = False
        # Calculate distance of current_route
        best_distance = calculate_route_distance(current_route, graph)
        # Iterate through each vertex in the route except the first and last
        for i in range(1, len(current_route) - 2):
            for j in range(i + 1, len(current_route) - 1):

                new_route = two_opt_swap(current_route, i, j)
                # Calculate distance of new_route
                new_distance = calculate_route_distance(new_route, graph)
                # If new_distance is improvement of current best_route then update
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improvement = True
        # Set current_route to best_route in this iteration
        current_route = best_route
    # Update the truck's route with the optimized route
    trucks.route = best_route
    # Optimize the order of packages to reflect the optimized route
    optimized_packages = []
    for address in current_route:
        for package in trucks.get_packages():
            if package.address == address:
                optimized_packages.append(package)
                break
    trucks.packages = optimized_packages
