import math


# Load the packages on truck using nearest neighbor algorithm
def load_packages_nearest_neighbor(truck, graph, track_package_id):
    from package_delivery.delivery import Trucks
    current_vertex = '4001 South 700 East'
    remaining_packages = Trucks.get_left_over_packages(graph, track_package_id)
    truck.route = [current_vertex]  # Initialize the route with the hub vertex

    for package in remaining_packages:
        min_distance = math.inf
        nearest_package = None

        dest_vertex = package.address
        distance = graph.edge_weight[current_vertex][dest_vertex]
        if distance < min_distance and can_load_package(truck, package):
            min_distance = distance
            nearest_package = package
        if nearest_package:
            truck.insert_packages(nearest_package)
            current_vertex = nearest_package.address
            remaining_packages.remove(nearest_package)

    # Return to the hub
    truck.route.append('4001 South 700 East')


# Check if the truck can load the package based on constraints
def can_load_package(truck, package):
    delivery_deadline = package.delivery_deadline
    package_id = package.package_id
    # Check if the truck is full
    if truck.get_package_count() >= 16:
        return False
    # Check if the package has a deadline of 9:00 AM
    if delivery_deadline == '9:00 AM':
        if truck.truck_id == 1 and package_id in [15, 14, 19, 16, 13, 20]:
            return True
        else:
            return False

    # Check if the package has a deadline of 10:30 AM
    if delivery_deadline == '10:30 AM':
        if truck.truck_id == 2 and package.special_notes == 'Can only be on truck 2':
            return True
        else:
            return False
    # If the package has a deadline of EOD
    if delivery_deadline == 'EOD':
        return True
