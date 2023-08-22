# Implement the nearest neighbor algorithm, brute force approach, optimize the order of addresses in route
# Starting from the hub, 4001 South 700 East, and ending at the hub
# sort the order of the packages loaded on Trucks object after loading the packages;
# this creates an initial route when calling the 'two_opt_route' function
# to further decrease the total_distance traveled by the three trucks after nearest neighbor algorithm
# This does not affect the process of delivering packages for all the packages
import math


# 8/22/23 no longer needed as load_packages_nearest_neighbor() is used instead of sort_packages_on_truck()
# to load packages onto trucks which uses the nearest neighbor algorithm and sorts the packages on the truck

# Sort the packages on the truck using the nearest neighbor algorithm and update the truck's route with the sorted route
def sort_packages_on_truck(trucks, graph):
    """
    Sorts the packages on the trucks based on the shortest distance to their destinations.

    Args:
        trucks (Truck): An instance of the Truck class representing the trucks carrying the packages.
        graph (Graph): An instance of the Graph class representing the graph of distances between locations.

    Returns:
        None
    """
    # Start from the hub
    hub_vertex = '4001 South 700 East'
    current_vertex = hub_vertex
    sorted_packages = []
    # Initialize the sorted route with the hub vertex
    sorted_route = [current_vertex]

    # Get the packages on the truck
    packages = trucks.get_packages()

    # While there are still packages on the truck
    while len(packages) > 0:
        # Initialize the minimum distance to infinity and the nearest package to None
        min_distance = math.inf
        nearest_package = None
        # For each package on the truck find the nearest package to the current vertex by calculating the distance
        # between the current vertex and the destination vertex of the package
        for package in packages:
            dest_vertex = package.address
            # Calculate the distance between the current vertex and the destination vertex by looking up the distance in
            # the graph object using the current vertex and destination vertex as keys
            distance = graph.edge_weight[current_vertex][dest_vertex]
            # If the distance is less than the minimum distance, update the minimum distance and nearest package
            if distance < min_distance:
                min_distance = distance
                nearest_package = package

        # Move to the nearest package and mark it as loaded on the truck and its route
        if nearest_package:
            # Add the nearest package to the sorted packages list and its address to the sorted route list
            sorted_packages.append(nearest_package)
            sorted_route.append(nearest_package.address)
            # Update the current vertex to the nearest package's address
            current_vertex = nearest_package.address
            # Remove the nearest package from the packages variable
            packages.remove(nearest_package)

    # After all deliveries, return to the hub
    sorted_route.append(hub_vertex)
    trucks.packages = sorted_packages
    trucks.route = sorted_route
    # print()
    # print("SORTED_ROUTE: ", sorted_route)
    # print()
