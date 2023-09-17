import math

from package_delivery.loadutil import load_util as util


# Load the packages on truck using the nearest neighbor algorithm
def load_packages_nearest_neighbor(trucks, graph, track_package_id):
    """
    Loads packages into the trucks using a nearest neighbor algorithm.

    Parameters:
    - trucks (list): A list of truck objects representing the available trucks.
    - graph (Graph): An object representing the graph of locations and distances.
    - track_package_id (set): A set of package IDs that have been tracked.

    Returns:
    None
    """
    MAX_PACKAGE_COUNT = 15

    for truck in trucks:
        # Start from the hub
        current_vertex = '4001 South 700 East'
        # Remaining packages for each truck after loading the previous truck
        remaining_packages = util.get_all_packages_to_load(graph, track_package_id)
        truck.route = [current_vertex]  # Initialize the route with the hub vertex

        # Separate packages that meet constraints from other packages for the current truck
        constrained_packages = []
        # Packages that do not meet constraints for the current truck
        unconstrained_packages = []

        for package in remaining_packages:
            if util.has_load_packages(truck, package):
                constrained_packages.append(package)
            else:
                # Add unconstrained packages to the unconstrained_packages list
                # if they do not have constraints for the current truck
                unconstrained_packages.append(package)

        # print(truck.truck_name, 'unconstrained_packages', unconstrained_packages, '\n')
        # print(truck.truck_name, 'constrained_packages', constrained_packages, '\n')

        # # Load constrained packages first to satisfy constraints
        if truck.truck_id == 1 or truck.truck_id == 2:
            for package in constrained_packages.copy():
                current_vertex = package.address
                truck.insert_packages(package)
                track_package_id.add(package.package_id)
                constrained_packages.remove(package)
                # To make debugging easier
                # print(f"Debug: Successfully loaded Package {package.package_id} onto {truck.truck_name}.")

        # Remove unconstrained packages with constraints of the current truck from the unconstrained_packages list
        unconstrained_packages = [package for package in unconstrained_packages if
                                  not util.has_package_constraints(package)]

        all_packages_for_truck = constrained_packages + unconstrained_packages

        while truck.get_package_count() < MAX_PACKAGE_COUNT:
            min_distance = math.inf
            nearest_package = None

            for package in all_packages_for_truck:
                dest_vertex = package.address
                distance = graph.get_edge_weight[current_vertex][dest_vertex]

                if distance < min_distance:
                    min_distance = distance
                    nearest_package = package

            # Load the nearest package if it meets the lowest distance
            if nearest_package is not None:
                current_vertex = nearest_package.address
                truck.insert_packages(nearest_package)
                track_package_id.add(nearest_package.package_id)
                all_packages_for_truck.remove(nearest_package)
            else:
                # Break out of the while loop if there are no more packages to load
                break
        # Update addresses so visualization works and add hub back to route
        truck.route.append('4001 South 700 East')
        truck.visualize.update_address(truck.route, truck.truck_id)
