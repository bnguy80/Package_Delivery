# Implement the nearest neighbor algorithm, brute force approach, optimize the order of addresses in route
# Starting from the hub, 4001 South 700 East, and ending at the hub
# sort the order of the packages loaded on Trucks object after loading the packages;
# this creates an initial route when calling the 'two_opt_route' function
# to further decrease the total_distance traveled by the three trucks after nearest neighbor algorithm
# This does not affect the process of delivering packages for all the packages
import math


# Find the nearest package to the current vertex on the truck and return it as a package object
def find_nearest_package(truck, current_vertex, graph):
    # Initialize the minimum distance to infinity and the nearest package to None
    min_distance = math.inf
    nearest_package = None
    # For each package on the truck find the nearest package to the current vertex
    for package in truck.get_packages():
        dest_vertex = package.address
        # Calculate the distance between the current vertex and the destination vertex by looking up the distance in
        # the graph object using the current vertex and destination vertex as keys
        distance = graph.edge_weight[current_vertex][dest_vertex]
        # If the distance is less than the minimum distance, update the minimum distance and nearest package
        if distance < min_distance:
            min_distance = distance
            nearest_package = package

    return nearest_package


# Sort the packages on the truck using the nearest neighbor algorithm and update the truck's route with the sorted route
def sort_packages_on_truck(trucks, graph):
    # Start from the hub
    hub_vertex = '4001 South 700 East'
    current_vertex = hub_vertex
    sorted_packages = []
    # Initialize the sorted route with the hub vertex
    sorted_route = [current_vertex]

    # While there are still packages on the truck
    while len(trucks.get_packages()) > 0:
        # Find the nearest package to the current vertex
        nearest_package = find_nearest_package(trucks, current_vertex, graph)

        # Move to the nearest package and mark it as loaded on the truck and its route
        if nearest_package:
            # Add the nearest package to the sorted packages list and its address to the sorted route list
            sorted_packages.append(nearest_package)
            sorted_route.append(nearest_package.address)
            # Update the current vertex to the nearest package's address
            current_vertex = nearest_package.address
            # Remove the nearest package from the truck and its route list of packages and addresses respectively
            trucks.remove_packages(nearest_package)
    # After all deliveries, return to the hub
    sorted_route.append(hub_vertex)
    trucks.packages = sorted_packages
    trucks.route = sorted_route
    print()
    print("SORTED_ROUTE: ", sorted_route)
    print()
