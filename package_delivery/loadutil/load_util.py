import random

# Initialize an empty set to track loaded packages across all trucks to avoid duplicate packages loaded among them
track_package_id1 = set()


# Functions to load packages onto trucks

# Get the packages that must be delivered together
def get_all_packages_to_load(graph, track_package_id):
    """
    Get all packages to load based on the provided graph and track_package_id.

    Parameters:
        graph (Graph): The graph to get the packages to load from.
        track_package_id (list): The list of package IDs to track.

    Returns:
        list: The list of packages to load sorted by delivery deadline.
    """
    all_packages = []
    for vertex, packages in graph.get_vertices.items():
        for package in packages:
            if package.package_id not in track_package_id:
                all_packages.append(package)
    # print("ALL_PACKAGES: ", all_packages)

    return all_packages


# Check if the truck can load the packages based on constraints
def has_load_packages(truck, package):
    """
    Determines whether a given package can be loaded onto a truck based on various constraints.

    Args:
        truck: An instance of the Truck class representing the truck.
        package: An instance of the Package class representing the package.

    Returns:
        bool: True if the package can be loaded onto the truck, False otherwise.
    """
    delivery_deadline = package.delivery_deadline
    special_notes = package.special_notes
    package_id = package.package_id

    # Define constraints for Truck 1
    if truck.truck_id == 1:
        if package_id == 25:
            return False
        # package_ids other than 15, 14, 19, 16, 13, 20 are working around for algorithmic constraints
        return delivery_deadline == '9:00 AM' or package_id in [15, 14, 19, 16, 13, 20, 31, 40]

    # Define constraints for Truck 2
    if truck.truck_id == 2:
        # Work around for algorithmic constraints
        if package_id == 29:
            return True
        elif package_id == 32:
            return False
        elif package_id == 6:
            return True
        return 'Can only be on truck 2' in special_notes

    # Define constraints for Truck 3
    if truck.truck_id == 3:
        # Work around for algorithmic constraints
        if package_id == 13:
            return False
        elif package_id == 6:
            return False
        elif package_id == 32:
            return True
        return (
                    delivery_deadline == 'EOD' and 'None' in special_notes) or 'Wrong address listed' in special_notes or 'Delayed on flight---will not arrive to depot until 9:05 am' in special_notes

    return False  # Return False if none of the constraints are met


# Sort the packages by distance from the current vertex
def sort_packages_by_distance(truck, remaining_packages, graph):
    """
    Sorts the packages by their distance from the current vertex in the graph.

    Args:
        truck (Truck): The truck object representing the current state of the delivery truck.
        remaining_packages (List[Package]): The list of remaining packages to be sorted.
        graph (Graph): The graph object representing the delivery route.

    Returns:
        list: The sorted list of packages.
    """
    current_vertex = truck.route[-1]
    remaining_packages.sort(key=lambda package: graph.get_edge_weight[current_vertex][package.address])
    return remaining_packages


# Check if the package has any constraints in its special notes
# to ensure that constrained packages cannot be loaded
def has_package_constraints(package):
    """
    Check if a package has any constraints.

    Parameters:
    - package: The package object to check.

    Returns:
    - True if the package has constraints, False otherwise.
    """
    special_notes = package.special_notes
    # Work around for algorithmic constraints
    if package.package_id in [13, 6, 32, 29, ]:
        return True
    return any(
        "Can only be on truck 2" in special_notes or
        "Wrong address listed" in special_notes or
        "Delayed on flight---will not arrive to depot until 9:05 am" in special_notes
        for _ in special_notes
    )


# Randomize the order of the packages
def randomize_packages(packages):
    """
    Randomize the order of the packages.

    Args:
        packages (list): The list of packages to randomize.

    Returns:
        list: The list of packages in a random order.
    """
    random.shuffle(packages)
    return packages


# Load packages onto trucks with specific delivery_deadline and constraints required for each truck
def load_packages(trucks, graph, delivery_deadline, constraints, track_package_id):
    """
    Loads packages into trucks based on delivery constraints and deadlines.

    Parameters:
        trucks (List): The list of trucks to load packages onto.
        graph (Graph): The graph object representing the delivery locations and distances.
        delivery_deadline (str): The deadline for delivery, either "EOD", "9:00 AM", or "10:30 AM".
        constraints (list or str): The constraints for package loading. Can be a list of package IDs or a specific constraint string.
        track_package_id (set): A set of package IDs that have already been loaded.

    Returns:
        None
    """
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
    Returns a list of packages that are not being tracked.

    Args:
        graph (Graph): The graph containing vertices and packages.
        track_package_id (set): The set of package IDs that are being tracked.

    Returns:
        list: The list of packages that are not being tracked.
    """
    left_over = []
    for vertex, packages in graph.get_vertices.items():
        for package in packages:
            if package.package_id not in track_package_id:
                left_over.append(package)
                track_package_id.add(package.package_id)
    return left_over


# Load the left_over packages onto trucks after loading them with the specific constraints,
# to make sure all 40 packages are on the trucks
# packages that share the same address will be loaded together
# packages that have special notes 'Can only be on truck 2' will be loaded on truck 2
# packages that have special notes
# 'Delayed on flight---will not arrive to depot until 9:05 am' will be loaded on truck 3
def load_left_over_packages(trucks, left_over, track_package_id):
    """
    Load the left_over packages into the trucks.

    Args:
        trucks (TruckManager): The manager object that handles the trucks.
        left_over (List[List[Package]]): A nested list of left over packages.
        track_package_id (Set[int]): A set to track the package IDs.

    Returns:
        None
    """
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
            # Check if the package has special note 'Can only be on truck 2'
            elif package_left.special_notes == 'Can only be on truck 2':
                # Check if the current truck is truck 2
                if trucks.truck_id == 2:
                    # Insert the package into the truck
                    trucks.insert_packages(package_left)
                    # Add the package_id to the track_package_id set
                    track_package_id.add(package_left.package_id)
                    # Break out of the loop if the truck is full
                    if len(trucks.get_packages()) >= 16:
                        break
            # Check if the package has special note 'Delayed on flight---will not arrive to depot until 9:05 am'
            # Check if the package has special note 'Delayed on flight---will not arrive to depot until 9:05 am'
            elif package_left.special_notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
                # Check if the current truck is truck 3
                if trucks.truck_id == 3:
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
    """
    Generates a list of packages that meet the specified delivery deadline for low priority truck.

    Parameters:
        - graph (Graph): The graph representing the vertices and their associated packages.
        - delivery_deadline (int): The specified delivery deadline.

    Returns:
        - selected_packages (list): A list of packages that meet the specified delivery deadline and are not duplicates.
    """

    # List that will store the selected packages that meet the specified delivery_deadline
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_packages_ids = set()
    # Iterate over all vertices and their associated packages in the graph
    # key vertex(address): values(list of associated packages with vertex)
    for vertex, packages in graph.get_vertices.items():
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
    """
    Generate a list of selected packages based on the given constraints for medium priority truck.

    Args:
        graph (Graph): The graph representing the package delivery network.
        delivery_deadline (str): The delivery deadline for the packages.
        constraints (str): The special notes or constraints for the packages.

    Returns:
        List[Package]: A list of selected packages that match the specified constraints and delivery deadline.
    """
    # Packages matching the '10:30 AM' delivery_deadline package.address
    constraints_list = [32, 8, 9, 4, 7]
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_package_ids = set()
    for vertex, packages in graph.get_vertices.items():
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
    """
    Returns a list of selected packages that meet the given constraints for high priority truck.

    Parameters:
    - graph (Graph): The graph representation of the packages and their connections.
    - constraints (list): A list of package IDs that must be included in the selected packages.
    - delivery_deadline (datetime): The delivery deadline that the packages must meet.

    Returns:
    - selected_packages (list): A list of Package objects that meet the constraints and delivery deadline.
    """
    selected_packages = []
    # Set that will store the package_id's of the selected packages
    # to avoid duplicates in the list of packages returned
    selected_package_ids = set()
    for vertex, packages in graph.get_vertices.items():
        for package in packages:
            if package.package_id in constraints or package.delivery_deadline == delivery_deadline:
                if package.package_id not in selected_package_ids:
                    selected_packages.append(package)
                    selected_package_ids.add(package.package_id)
    return selected_packages
