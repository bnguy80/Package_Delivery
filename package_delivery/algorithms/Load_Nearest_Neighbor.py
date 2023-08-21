import math

from package_delivery.delivery.Load_Packages import get_all_packages_to_load
from package_delivery.delivery.Load_Packages import package_has_constraints
from package_delivery.delivery.Load_Packages import can_load_package


# Load the packages on truck using nearest neighbor algorithm
def load_packages_nearest_neighbor(trucks, graph, track_package_id):
    for truck in trucks:
        current_vertex = '4001 South 700 East'
        remaining_packages = get_all_packages_to_load(graph, track_package_id)
        truck.route = [current_vertex]  # Initialize the route with the hub vertex

        # Separate packages that meet constraints from other packages for the current truck
        constrained_packages = []
        # Packages that do not meet constraints for the current truck
        unconstrained_packages = []

        for package in remaining_packages:
            if can_load_package(truck, package):
                constrained_packages.append(package)
            else:
                # Add unconstrained packages to the unconstrained_packages list
                # if they do not have constraints for the current truck
                unconstrained_packages.append(package)

        # Remove unconstrained packages with constraints from the unconstrained_packages list
        unconstrained_packages = [package for package in unconstrained_packages if not package_has_constraints(package)]

        # Combine the constrained_packages and unconstrained_packages lists to form a list of all packages
        # for the current truck
        all_packages = constrained_packages + unconstrained_packages

        while truck.get_package_count() < 14 and len(all_packages) > 0:
            min_distance = math.inf
            nearest_package = None

            for package in all_packages:
                dest_vertex = package.address
                distance = graph.edge_weight[current_vertex][dest_vertex]

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
        print(f"Truck {truck.truck_id} - Route: {truck.route}")

