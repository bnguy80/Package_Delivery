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
    for truck in trucks:
        current_vertex = '4001 South 700 East'
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

        # Remove unconstrained packages with constraints of the current truck from the unconstrained_packages list
        unconstrained_packages = [package for package in unconstrained_packages if not util.has_package_constraints(package)]

        # Combine the constrained_packages and unconstrained_packages lists to form a list of all packages
        # for the current truck
        all_packages = constrained_packages + unconstrained_packages

        # Keep count to 14 packages per truck to make sure all packages are loaded
        # without any errors
        while truck.get_package_count() < 14 and len(all_packages) > 0:
            min_distance = math.inf
            nearest_package = None

            for package in all_packages:
                dest_vertex = package.address
                distance = graph.get_edge_weight[current_vertex][dest_vertex]

                if distance < min_distance:
                    min_distance = distance
                    nearest_package = package

            if nearest_package is not None:
                # Load the nearest package if it meets the constraints
                current_vertex = nearest_package.address
                truck.insert_packages(nearest_package)
                track_package_id.add(nearest_package.package_id)
                all_packages.remove(nearest_package)
            else:
                print(f"No suitable package found for truck {truck.truck_id}")

        # Return to the hub
        truck.route.append('4001 South 700 East')
        truck.visualize.update_address(truck.route, truck.truck_id)
