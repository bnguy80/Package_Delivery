# Get all packages to load on truck in order of nearest neighbor algorithm
import random


def get_randomized_packages_to_load(graph, track_package_id):
    all_packages = []
    for vertex, packages in graph.vertices.items():
        for package in packages:
            if package.package_id not in track_package_id:
                all_packages.append(package)
    random.shuffle(all_packages)  # Shuffle the list of packages randomly
    # print("ALL_PACKAGES: ", all_packages)
    return all_packages


def sort_packages_by_distance(truck, remaining_packages, graph):
    current_vertex = truck.route[-1]
    remaining_packages.sort(key=lambda package: graph.edge_weight[current_vertex][package.address])


# Load packages onto trucks with specific delivery_deadline and constraints required for each truck
def load_packages(trucks, graph, delivery_deadline, constraints, track_package_id):
    if constraints is None and delivery_deadline == "EOD":
        load_package = get_package_deadline_constraints_low_asc(graph, delivery_deadline)
        if len(trucks.get_packages()) < 16:
            if load_package is not None:
                if isinstance(load_package, list):
                    for package in load_package:
                        if len(trucks.get_packages()) >= 16:
                            break
                        else:
                            if package.package_id not in track_package_id:
                                if len(trucks.get_packages()) < 16:
                                    trucks.insert_packages(package)
                                    track_package_id.add(package.package_id)
                else:
                    trucks.insert_packages(load_package)
        #     print("LOW_PRIORITY LOAD_PACKAGES WITHOUT CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
        #     print()
        # trucks.print_packages()

    # truck_high_priority should be loaded with:
    # package_id=15 9:00 AM,
    # package_id=14 10:30 AM,
    # package_id=19 EOD,
    # package_id=16 10:30 AM,
    # package_id=13 10:30 AM,
    # package_id=20 10:30 AM
    else:
        if constraints == [15, 14, 19, 16, 13, 20, 39, 21] or delivery_deadline == "9:00 AM":
            load_package = get_package_deadline_constraints_high_asc(graph, constraints, delivery_deadline)
            if len(trucks.get_packages()) < 16:
                if load_package is not None:
                    if isinstance(load_package, list):
                        for package in load_package:
                            if len(trucks.get_packages()) >= 16:
                                break
                            else:
                                if package.package_id not in track_package_id:
                                    if len(trucks.get_packages()) < 16:
                                        trucks.insert_packages(package)
                                        track_package_id.add(package.package_id)
                    else:
                        trucks.insert_packages(load_package)
            # print("HIGH_PRIORITY LOAD_PACKAGES WITH CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
            # print()
            # trucks.print_packages()
            # print("---NEW LINE---\n")
        elif constraints == "Can only be on truck 2" or delivery_deadline == "10:30 AM":
            load_package = get_package_deadline_constraints_med_asc(graph, delivery_deadline, constraints)
            if len(trucks.get_packages()) < 16:
                if load_package is not None:
                    if isinstance(load_package, list):
                        for package in load_package:
                            if len(trucks.get_packages()) >= 16:
                                break
                            else:
                                if package.package_id not in track_package_id:
                                    if len(trucks.get_packages()) < 16:
                                        trucks.insert_packages(package)
                                        track_package_id.add(package.package_id)
                    else:
                        trucks.insert_packages(load_package)
            # print("MEDIUM_PRIORITY LOAD_PACKAGES WITH CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
            # print()
            # trucks.print_packages()
            # print("---NEW LINE---\n")
    # if truck_high_priority is not None:
    #     load_package = Trucks.get_package_deadline_constraints_high_asc(**args2)
    #     trucks.insert_packages(load_package)
    # print("WITH CONSTRAINTS Trucks.get_package_deadline_constraints_high_asc(**args3) : ")
    # trucks.print_packages()


# Packages not loaded on all three Trucks object because packages < 16 on Trucks object
# and will remain currently at hub, package_id add to the track_package_id set()
# when loading packages, get left_over from non-present package.pacakge_id's
def get_left_over_packages(graph, track_package_id):
    """
    Returns a list of packages that are not tracked.

    Args:
        graph (Graph): The graph containing vertices and packages.
        track_package_id (set): The set of package IDs that are being tracked.

    Returns:
        list: The list of packages that are not being tracked.
    """
    left_over = []
    for vertex, packages in graph.vertices.items():
        for package in packages:
            if package.package_id not in track_package_id:
                left_over.append(package)
                track_package_id.add(package.package_id)

    return left_over


# Load the left_over packages onto trucks after loading them with the specific constraints,
# to make sure all 40 packages are on the trucks
def load_left_over_packages(trucks, left_over, track_package_id):
    """
    Load left over packages into the trucks.

    Args:
        trucks (Truck): The trucks object.
        left_over (list): The list of left over packages.
        track_package_id (set): The set of package IDs to track.

    Returns:
        None
    """
    # Create a dictionary of truck packages
    truck_packages = {package.address: package for package in trucks.get_packages()}

    # Flatten the left_over list
    flattened_list = [package for sublist in left_over for package in sublist]

    # Iterate over the flattened list
    for package_left in flattened_list:
        # Check if the number of packages in the truck is less than 16
        if len(trucks.get_packages()) < 16:
            # Check if the package address is in the truck_packages dictionary
            if package_left.address in truck_packages:
                # Insert the package into the truck
                trucks.insert_packages(package_left)
                # Add the package_id to the track_package_id set
                track_package_id.add(package_left.package_id)
                # Break out of the loop if the truck is full
                if len(trucks.get_packages()) >= 16:
                    break

    """Get packages from the AdjacencyMatrix.Graph object with the specified delivery_deadline 
       'EOD' and the constraints associated with each individual packages
       This function correctly only accounts for low_priority to loaded packages
       7/24/23: should eventually work with high_priority to load '9:00 AM' package first then work down to 
       'with_constraints' function, 7/25/23: Will now not include high_priority object
    """


def get_package_deadline_constraints_low_asc(graph, delivery_deadline):
    # List that will store the selected packages that meet the specified delivery_deadline
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_packages_ids = set()
    # Iterate over all vertices and their associated packages in the graph
    # key vertex(address): values(list of associated packages with vertex)
    for vertex, packages in graph.vertices.items():
        # Iterate over each package associated with the current vertex
        for package in packages:
            # Checks if package with specified delivery_deadline match
            if delivery_deadline == package.delivery_deadline:
                # Checks if the current package is already in selected_packages list
                # duplicate set to True and break out of inner for loop
                if package.package_id not in selected_packages_ids:
                    selected_packages.append(package)
                    selected_packages_ids.add(package.package_id)
    # Return selected_packages list, with delivery_deadline match and not a duplicate
    return selected_packages


def get_package_deadline_constraints_med_asc(graph, delivery_deadline, constraints):
    # Packages matching the '10:30 AM' delivery_deadline package.address
    constraints_list = [32, 8, 9, 4, 7]
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_package_ids = set()
    for vertex, packages in graph.vertices.items():
        for package in packages:
            # Checks if package_id is in the specified constraints list or delivery_deadline match
            if package.special_notes == constraints or package.package_id in constraints_list or package.delivery_deadline == delivery_deadline:
                if package.package_id not in selected_package_ids:
                    selected_packages.append(package)
                    selected_package_ids.add(package.package_id)
    return selected_packages


"""Get packages from AdjacencyMatrix.Graph object with specified constraints[15, 14, 19, 16, 13, 20] the 
   packages to be loaded together, will be used for high_priority to keep route length to minimum
"""


def get_package_deadline_constraints_high_asc(graph, constraints, delivery_deadline):
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_package_ids = set()
    for vertex, packages in graph.vertices.items():
        for package in packages:
            if package.package_id in constraints or package.delivery_deadline == delivery_deadline:
                if package.package_id not in selected_package_ids:
                    selected_packages.append(package)
                    selected_package_ids.add(package.package_id)
    return selected_packages
