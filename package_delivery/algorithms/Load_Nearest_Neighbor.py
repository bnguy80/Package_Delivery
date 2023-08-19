import math

from package_delivery.delivery.Load_Packages import get_randomized_packages_to_load


# Load the packages on truck using nearest neighbor algorithm
def load_packages_nearest_neighbor(trucks, graph, track_package_id):
    for truck in trucks:
        current_vertex = '4001 South 700 East'
        remaining_packages = get_randomized_packages_to_load(graph, track_package_id)
        truck.route = [current_vertex]  # Initialize the route with the hub vertex

        # print(f"Truck {truck.truck_id} - Initial remaining packages:", len(remaining_packages))

        while remaining_packages and truck.get_package_count() < 16:
            min_distance = math.inf
            nearest_package = None
            package_loaded = False  # Flag to track if a package was loaded in this iteration

            for package in remaining_packages:
                dest_vertex = package.address
                distance = graph.edge_weight[current_vertex][dest_vertex]

                if distance < min_distance and can_load_package(truck, package):
                    min_distance = distance
                    nearest_package = package
                    package_loaded = True

            # Load the nearest package if it can be loaded on the truck and remove it from the remaining packages
            if package_loaded:
                current_vertex = nearest_package.address
                truck.insert_packages(nearest_package)
                track_package_id.add(nearest_package.package_id)
                remaining_packages.remove(nearest_package)
            else:
                break  # Exit the loop if no more packages can be loaded

            # print(f"Truck {truck.truck_id} - Remaining packages:", len(remaining_packages))

        # Return to the hub
        truck.route.append('4001 South 700 East')
        print(f"Truck {truck.truck_id} - Route: {truck.route}")


# Check if the truck can load the package based on constraints
def can_load_package(truck, package):
    delivery_deadline = package.delivery_deadline
    special_notes = package.special_notes
    package_id = package.package_id
    package_address = package.address
    # Check if the truck is full
    if truck.get_package_count() >= 16:
        return False

    # Check if the package has a deadline of 9:00 AM
    elif delivery_deadline == '9:00 AM' or package_id in [15, 14, 19, 16, 13, 20]:
        if truck.truck_id == 1:
            return True
        return False

    # Check if the package has a deadline of 10:30 AM
    elif delivery_deadline == '10:30AM' or special_notes == 'Can only be on truck 2':
        if truck.truck_id == 2:
            return True
        return False

    # If the package has a deadline of EOD
    elif delivery_deadline == 'EOD' or special_notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
        if truck.truck_id == 3:
            return True

    return True  # Return True for cases where the package can be loaded on any truck



