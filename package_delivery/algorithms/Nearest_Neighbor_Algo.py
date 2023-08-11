# Implement the nearest neighbor algorithm, brute force approach, optimize the order of addresses in route in
# starting from the hub, 4001 South 700 East, and ending at the hub
# sort the order of the packages loaded on Trucks object after loading the packages;
# this creates an initial route when calling the 'find_shortest_route_to_deliver'
# function that where we implement dijkstra's algorithm
# This does not affect the process of delivering packages for all the packages
import math


def sort_packages_on_truck(trucks, graph):
    # Start from the hub
    current_vertex = '4001 South 700 East'
    hub_vertex = '4001 South 700 East'
    sorted_packages = []
    sorted_route = [current_vertex]

    # While there are still packages on the truck
    while len(trucks.get_packages()) > 0:
        min_distances = math.inf
        nearest_package = None

        # Find the nearest_package from the current_vertex
        for package in trucks.get_packages():
            dest_vertex = package.address
            # Calculate distance between current_vertex and dest_vertex
            distance = graph.edge_weight[current_vertex][dest_vertex]
            if distance < min_distances:
                min_distances = distance
                nearest_package = package
        # Move to the nearest package and mark it as loaded on the truck and its route
        if nearest_package:
            sorted_packages.append(nearest_package)
            sorted_route.append(nearest_package.address)
            current_vertex = nearest_package.address
            trucks.remove_packages(nearest_package)
    # After all deliveries, return to the hub
    sorted_route.append(hub_vertex)
    trucks.packages = sorted_packages
    trucks.route = sorted_route
    # print()
    # print("SORTED_ROUTE: ", sorted_route)
    # print()
