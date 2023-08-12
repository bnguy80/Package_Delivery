
from package_delivery.algorithms.Nearest_Neighbor_Algo import sort_packages_on_truck
from package_delivery.algorithms.Two_Opt_Route import two_opt_route
from package_delivery.data_structures.Adjacency_List import graph_access
from package_delivery.algorithms.DijkstraAlgo import dijkstra
from package_delivery.data_structures.HashMap import package_hashmap
from package_delivery.delivery.Tracking import TimeTracker

# Each truck can carry maximum of 16 packages
#
# Three trucks(Truck 1, 2, 3), two drivers available for delivery,
# each driver stays with same truck until all packages delivered
#
# Drivers leave hub no later than 8:00am with truck loaded, can return to hub to get packages
# The delivery and loading times are instantaneous
#
# Time passes while at a delivery or when moving packages to a
# truck at the hub (that time is factored into the calculation of the average speed of the trucks).
#
# There is up to one special note associated with a package.
# The day ends when all 40 packages have been delivered.
# Packages will be loaded manually, for some not in required constraints to decrease total distance traveled


# Initialize empty set to track loaded packages across all trucks to avoid duplicate packages loaded among them
track_package_id1 = set()

# Initialize empty list to track left_over packages across trucks not loaded after
# initially loading packages with specific constraints and delivery_deadline functions
left_over1 = []


class Trucks:
    # List of packages, route, distances, predecessor vertices to be loaded onto Trucks object
    def __init__(self):
        self.packages = []
        self.route = []
        self.distances = []
        self.pred_vertex = []
        # # Create an instance of TimeTracker if it doesn't exist
        self.time_tracker = TimeTracker()
        # Associate truck ID with Trucks object
        self.truck_id = 0

    def insert_truck_id(self, truck_id):
        self.truck_id = truck_id

    # Insert packages to list self.packages and address of package to route to
    # list self.route
    def insert_packages(self, package):
        self.packages.append(package)
        self.route.append(package.address)

    # Return the list of packages from Trucks object
    def get_packages(self):
        return self.packages

    # Remove package from Truck object after delivered
    # and remove address from route
    def remove_packages(self, package):
        self.packages.remove(package)
        self.route.remove(package.address)

    def insert_distances_pred_vertex(self, distance, pred_vertex):
        self.distances.append(distance)
        self.pred_vertex.append(pred_vertex)

    def get_distances(self):
        return self.distances

    # Print all packages list for Trucks object, useful to see what packages are loaded on
    # the trucks that are ordered by priority of deadline to delivery
    def print_packages(self):
        for package in self.packages:
            print(package)

    # Print route for Trucks object
    def print_route(self):
        print(self.route)

    # Return the count of list packages for Trucks object
    def get_package_count(self):
        return len(self.get_packages())

    """For each truck loaded with packages by priority, get the edge_weights for the packages;
        used in conjunction with set_edge_weight for the packages when load_trucks() is called.
        """

    @staticmethod
    def get_edge_weights(truck):
        # Sum up total edge_weight list of package loaded for Trucks object
        total_edge_weight = 0
        # Iterates over the collection of objects stored in the Trucks object
        for packages in truck:
            # Iterate over each package in the list of packages loaded on the current Trucks object
            for package in packages.get_packages():
                # If package has edge_weight than add its value to the 'total_edge_weight'
                if package.edge_weight is not None:
                    total_edge_weight += package.edge_weight
        # Return the calculated 'edge_weight' for the associated packages on the truck
        return total_edge_weight

    # Set the edge_weight for all packages on truck
    @staticmethod
    def set_edge_weight(truck):
        # From hub
        start_vertex = '4001 South 700 East'
        # Calculate edge weight between the package's location and the truck's starting location
        for package in truck.get_packages():
            # Destination address of second package
            dest_vertex = package.address
            if start_vertex in graph_access.edge_weight and dest_vertex in graph_access.edge_weight:
                edge_weight = graph_access.edge_weight[start_vertex][dest_vertex]
                package.edge_weight = edge_weight
            else:
                # Handle the case where the edge weight is not found in the graph
                package.edge_weight = None

    """Get packages from the AdjacencyMatrix.Graph object with the specified delivery_deadline 
       'EOD' and the constraints associated with each individual packages
       This function correctly only accounts for low_priority to loaded packages
       7/24/23: should eventually work with high_priority to load '9:00 AM' package first then work down to 
       'with_constraints' function, 7/25/23: Will now not include high_priority object
    """

    @staticmethod
    def get_package_deadline_constraints_low_asc(graph, delivery_deadline):
        # List that will store the selected packages that meet the specified delivery_deadline
        selected_packages = []
        # Iterate over all vertices and their associated packages in the graph
        # key vertex(address): values(list of associated packages with vertex)
        for vertex, packages in graph.vertices.items():
            # # Breaks out of for loop if this function is provided with constraints
            # if constraints is not None:
            #     print("Constraints is not none")
            #     break
            # Iterate over each package associated with the current vertex
            for package in packages:
                # Checks if package with specified delivery_deadline match
                if delivery_deadline == package.delivery_deadline:
                    duplicate = False
                    # Iterate over each package with delivery_deadline match in selected_packages list
                    for selected_package in selected_packages:
                        # Checks if the current package is already in selected_packages list
                        # duplicate set to True and break out of inner for loop
                        if selected_package.package_id == package.package_id:
                            duplicate = True
                            break
                    # After inner for loop, check if duplicate == False,
                    # i.e. selected_package is not in selected_package list
                    if not duplicate:
                        selected_packages.append(package)
        # Return selected_packages list, with delivery_deadline match and not a duplicate
        return selected_packages

    @staticmethod
    def get_package_deadline_constraints_med_asc(graph, delivery_deadline, constraints):
        # Packages matching the '10:30 AM' delivery_deadline package.address
        constraints_list = [32, 8, 9, 4, 7]
        selected_packages = []
        for vertex, packages in graph.vertices.items():
            for package in packages:
                # Checks if package_id is in the specified constraints list or delivery_deadline match
                if package.special_notes == constraints or package.package_id in constraints_list or package.delivery_deadline == delivery_deadline:
                    duplicate = False
                    for selected_package in selected_packages:
                        if selected_package.package_id == package.package_id:
                            duplicate = True
                            break
                    if not duplicate:
                        selected_packages.append(package)
        return selected_packages

    """Get packages from AdjacencyMatrix.Graph object with specified constraints[15, 14, 19, 16, 13, 20] the 
       packages to be loaded together, will be used for high_priority to keep route length to minimum
    """

    @staticmethod
    def get_package_deadline_constraints_high_asc(graph, constraints, delivery_deadline):
        # List that will store the selected packages that meet the specified delivery_deadline and constraints
        selected_packages = []
        # Iterate over all vertices and their associated packages in the graph
        # key vertex(address): values(list of associated packages with vertex)
        for vertex, packages in graph.vertices.items():
            # Iterate over each package associated with the current vertex
            for package in packages:
                # Checks if package_id is in the specified constraints list or delivery_deadline match
                if package.package_id in constraints or package.delivery_deadline == delivery_deadline:
                    duplicate = False
                    # Iterate over each package with constraints match in the selected_packages list
                    for selected_package in selected_packages:
                        # Checks if current package is already in the selected_packages list
                        # Duplicate set to true and break out of inner for loop
                        if selected_package.package_id == package.package_id:
                            duplicate = True
                            break
                    # After inner for loop, checks if duplicate == False,
                    # append selected_package is not in selected_packaged list already
                    if not duplicate:
                        selected_packages.append(package)
        # Return selected_package list, with constraints matches
        return selected_packages


# 40 packages, 9 + 16 + 15 respectively? for trucks, maximum amount of packages to load
# Start hub = '4001 South 700 East', load all trucks at hub
# priority_queue to pop off packages on trucks until empty?
# Once first truck is empty driver returns to hub to get next truck for deliveries
def load_trucks(truck_high_priority, truck_medium_priority, truck_low_priority, graph, track_package_id):
    # Define the arguments as a single variable
    # Load high priority
    delivery_deadline1 = "9:00 AM"
    # packages besides 15, 14, 19, 16, 13, 20 share same package.address for some on loaded on truck
    constraint_list1 = [15, 14, 19, 16, 13, 20, 39, 21]
    args1 = {
        'trucks': truck_high_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline1,
        'constraints': constraint_list1,
        'track_package_id': track_package_id,
        # 'track_time': track_time1
    }
    load_packages(**args1)
    Trucks.set_edge_weight(truck_high_priority)

    # Load medium priority
    delivery_deadline2 = "10:30 AM"
    constraint_list2 = "Can only be on truck 2"
    args2 = {
        'trucks': truck_medium_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline2,
        'constraints': constraint_list2,
        'track_package_id': track_package_id,
    }
    load_packages(**args2)
    Trucks.set_edge_weight(truck_medium_priority)

    # Load low priority
    delivery_deadline3 = "EOD"
    constraint_list3 = None

    args3 = {
        'trucks': truck_low_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline3,
        'constraints': constraint_list3,
        'track_package_id': track_package_id,
    }
    load_packages(**args3)
    Trucks.set_edge_weight(truck_low_priority)

    # After loading packages to satisfy constraints
    # Combine the left-over packages from all three priority levels
    left_over1.append(left_over_packages(graph_access, track_package_id1))
    # print()
    # print("LEFT_OVER_PACKAGES1 BEFORE FUNCTION LOAD_LEFT_OVER: ", left_over1)
    # Load left-over packages onto non-full trucks
    load_left_over_packages(high_priority, left_over1, track_package_id1)
    load_left_over_packages(medium_priority, left_over1, track_package_id1)
    load_left_over_packages(low_priority, left_over1, track_package_id1)
    # print("NEWLINE ---\n")
    # print("LOAD LEFT OVER PACKAGES: ", left_over1)


# Load packages onto trucks with specific delivery_deadline and constraints required for each truck
def load_packages(trucks, graph, delivery_deadline, constraints, track_package_id):
    if constraints is None and delivery_deadline == "EOD":
        load_package = Trucks.get_package_deadline_constraints_low_asc(graph, delivery_deadline)
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
            load_package = Trucks.get_package_deadline_constraints_high_asc(graph, constraints, delivery_deadline)
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
            load_package = Trucks.get_package_deadline_constraints_med_asc(graph, delivery_deadline, constraints)
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
def left_over_packages(graph, track_package_id):
    left_over = []
    # Convert the set to a list
    track_package_id_list = list(track_package_id)
    for vertex, packages in graph.vertices.items():
        for package in packages:
            if package.package_id not in track_package_id_list:
                left_over.append(package)
    return left_over


# Load the left_over packages onto trucks after loading them with the specific constraints,
# to make sure all 40 packages are on the trucks
def load_left_over_packages(trucks, left_over, track_package_id):
    for package_list in left_over:
        for package_left in package_list:
            # Check if any of the trucks already have the same address package loaded
            # Check if the package_left.address matches the already loaded packages in any of the trucks
            found_in_truck = False
            for package in trucks.get_packages():
                if package_left.address == package.address:
                    found_in_truck = True
                    break
            # If the package_left.address match is found in any trucks, load it onto the non-full trucks
            if found_in_truck:
                for package in trucks.get_packages():
                    # same_address_packages = [p for p in trucks.get_packages() if p.address == package.address]
                    if len(trucks.get_packages()) < 16:
                        trucks.insert_packages(package_left)
                        track_package_id.add(package_left.package_id)
                        break


# Calculate the shortest route to deliver packages to destination
# and back to hub after applying Dijkstra's algorithm
def find_shortest_route_to_deliver(truck, graph):
    # Make a copy of the packages on the truck
    packages_copy = truck.get_packages().copy()
    # Starting location for all trucks, i.e. the hub
    start_vertex1 = truck.route[0]
    # Initialize total_distance traveled by truck to 0
    total_distance = 0
    # Will make a copy of the pred_vertex to be able to use to find last package.address
    # and add route distance back to the hub
    pred_vertex_copy = []
    # Use a while loop to iterate over the packages
    # while packages_copy is not empty
    while packages_copy:
        # Remove the first package from the truck
        package = packages_copy.pop(0)
        # Vertex to travel to
        dest_vertex = package.address
        # Calculate the shortest distances and pred_vertex using Dijkstra's algorithm
        distances1, pred_vertex1 = dijkstra(graph, start_vertex1, truck.route)
        # Make a copy of pred_vertex list to use for to find route back to hub
        pred_vertex_copy.append(pred_vertex1.copy())
        # Insert the calculated distances and pred_vertex into the Trucks object
        truck.insert_distances_pred_vertex(distances1[dest_vertex], pred_vertex1[dest_vertex])
        # Update time during delivery
        time_delivered = truck.time_tracker.update_current_truck_time(distances1[dest_vertex], truck.truck_id)
        # Insert the time_delivered into package
        truck.time_tracker.insert_current_truck_time_to_package(package, time_delivered)
        # Update the time for other packages with the same address
        for other_package, status_info in truck.time_tracker.packages_status.items():
            if other_package != package and other_package.address == package.address and status_info[
                'status'] != 'DELIVERED':
                truck.time_tracker.insert_current_truck_time_to_package(other_package, time_delivered)
        # Skip adding the distance if the next package is already at the dest_vertex, share addresses
        if distances1[dest_vertex] != 0:
            total = distances1[dest_vertex]
            total_distance += total
        # Update start_vertex1 to the dest_vertex1 for the next iteration
        start_vertex1 = dest_vertex

    return total_distance


# Initialize loading trucks, package status to 'AT_HUB', package order, optimal route, and tracking of trucks
# def initialize_optimized_trucks(truck1, truck2, truck3, graph, track_package_id):
#     # Load all packages onto trucks
#     load_trucks(truck1, truck2, truck3, graph, track_package_id)
#     print("Trucks: truck1 Loaded Packages: ", truck1.get_packages(), "Count: ", len(truck1.get_packages()))
#     print("NEW LINE---\n")
#     print("Trucks: truck2 Loaded Packages: ", truck2.get_packages(), "Count: ", len(truck2.get_packages()))
#     print("NEW LINE---\n")
#     print("Trucks: truck3 Loaded Packages: ", truck3.get_packages(), "Count: ", len(truck3.get_packages()))
#     # Sort packages on trucks with nearest neighbor algorithm
#     sort_packages_on_truck(truck1, graph)
#     sort_packages_on_truck(truck2, graph)
#     sort_packages_on_truck(truck3, graph)
#     # Find optimal route using two-opt algorithm
#     two_opt_route(truck1, graph)
#     two_opt_route(truck2, graph)
#     two_opt_route(truck3, graph)
#     # Initialize all packages loaded onto trucks status to 'AT_HUB'
#     truck1_packages = truck1.get_packages()
#     truck2_packages = truck2.get_packages()
#     truck3_packages = truck3.get_packages()
#     truck1.time_tracker.initialize_multiple_package_status(truck1_packages, 'AT_HUB', truck1.truck_id, 8.0)
#     truck2.time_tracker.initialize_multiple_package_status(truck2_packages, 'AT_HUB', truck2.truck_id, 9.05)
#     truck3.time_tracker.initialize_multiple_package_status(truck3_packages, 'AT_HUB', truck3.truck_id, 8.0)
#     # Initialize tracking of trucks and packages
#     truck1.time_tracker.insert_current_truck(truck1.truck_id)
#     truck2.time_tracker.insert_current_truck(truck2.truck_id)
#     truck3.time_tracker.insert_current_truck(truck3.truck_id)


# Simulate delivering of packages
# Function to deliver packages using the TimeTracker instances inside each truck
def deliver_packages(trucks, graph, start_interval, end_interval):
    # Define a mapping of truck objects to their names
    truck_names = {
        high_priority: "HIGH_PRIORITY",
        medium_priority: "MEDIUM_PRIORITY",
        low_priority: "LOW_PRIORITY"
    }
    # Flag to track if truck 1's delivery is completed
    truck1_delivery_completed = False

    for current_truck in trucks:
        # Current truck time tracker high_priority, medium_priority, low_priority
        time_tracker = current_truck.time_tracker
        # Get the name of the current truck
        truck_name = truck_names[current_truck]
        # Initialize the time for the current truck
        time_tracker.insert_current_truck(current_truck.truck_id)
        print("NEW LINE---\n")
        # Check if current truck is ready for delivery
        if current_truck.time_tracker.is_ready_to_deliver(current_truck):
            # # Only print the route if the current truck is truck1 or truck2
            # if current_truck == high_priority or current_truck == medium_priority:
            #     print(f"{truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", current_truck.route)
            # Only deliver packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                # Call the function two_opt_route to find the optimized route for the current truck
                two_opt_route(current_truck, graph)
                # Call the function to find the shortest route to deliver packages
                total_distance = find_shortest_route_to_deliver(current_truck, graph)
                # Update miles traveled for the current truck
                time_tracker.update_miles_traveled(total_distance, current_truck.truck_id)

            # Check if the start time is 9:35 AM and update at 10:20 AM
            # If so, update the package with ID 9 to the new address
            if start_interval == '9:35':
                package_to_update = package_hashmap.get_value_from_key(9)  # Get the package object
                new_address = '410 S State St'
                new_city = 'Salt Lake City'
                new_state = 'UT'
                new_zipcode = '84111'
                new_special_notes = 'Address updated from 300 State St to 410 S State St'
                time_tracker.update_package_status(package_to_update, new_address, new_city, new_state, new_zipcode,
                                                   new_special_notes)
                print("PACKAGE UPDATED, Address updated from 300 State St to 410 S State St:")

            # Check if truck 1 has completed its delivery
            if current_truck == high_priority and current_truck.time_tracker.is_delivery_completed():
                truck1_delivery_completed = True

            if current_truck == low_priority:
                if truck1_delivery_completed and current_truck.time_tracker.is_ready_to_deliver(current_truck):
                    deliver_truck3_packages(current_truck, graph, start_interval, end_interval)
            # Only filter packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                filtered_packages = current_truck.time_tracker.filter_packages_by_time_range(start_interval,
                                                                                             end_interval)
                print("Start time:", start_interval, "End time:", end_interval)
                print("FILTERED_PACKAGES:", filtered_packages)
                print("TRUCK ROUTE:", current_truck.route)
                time_tracker.print_miles_traveled(current_truck.truck_id)


# After truck 1's delivery is completed, deliver truck 3's packages
def deliver_truck3_packages(truck3, graph, start_interval, end_interval):
    truck_name = "LOW_PRIORITY"
    time_tracker = truck3.time_tracker

    # Calculate start time for truck 3 based on truck 1's return time
    current_time_truck1 = high_priority.time_tracker.get_current_truck_time(high_priority.truck_id)
    truck3_start_time = current_time_truck1

    # Update truck 3's time to account for delivering packages after truck1
    # and update time_to_start_delivery
    time_tracker.track_truck_current_time[truck3.truck_id] = truck3_start_time
    time_tracker.update_time_to_start_delivery(truck3.truck_id, truck3_start_time)

    print("Truck 3: Starting deliveries.")
    # print(f"{truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", truck3.route)
    # Call the function two_opt_route to find the optimized route for truck 3
    two_opt_route(truck3, graph)
    # Call the function to find the shortest route to deliver packages
    total_distance = find_shortest_route_to_deliver(truck3, graph)
    # Update miles traveled for the current truck
    time_tracker.update_miles_traveled(total_distance, truck3.truck_id)

    filtered_packages = truck3.time_tracker.filter_packages_by_time_range(start_interval, end_interval)
    print("Start time:", start_interval, "End time:", end_interval)
    print("FILTERED_PACKAGES:", filtered_packages)

    time_tracker.print_miles_traveled(truck3.truck_id)


# Delivered by 9:00am, constraint of having multiple packages on same truck delivered together, Truck 1
high_priority = Trucks()
high_priority.insert_truck_id(1)
# Delivered by 10:30am, constraint of having multiple packages required on, Truck 2
medium_priority = Trucks()
medium_priority.insert_truck_id(2)
# Delivered by EOD, no constraints required for packages EOD will be defined as 5:00pm, Truck 3
low_priority = Trucks()
low_priority.insert_truck_id(3)

# Load trucks
load_trucks(high_priority, medium_priority, low_priority, graph_access, track_package_id1)
# Initialize tracking trucks
# high_priority.time_tracker.insert_current_truck(high_priority.truck_id)
# medium_priority.time_tracker.insert_current_truck(medium_priority.truck_id)
# low_priority.time_tracker.insert_current_truck(low_priority.truck_id)
# Initialize packages
high_priority.time_tracker.initialize_multiple_package_status(high_priority.get_packages(), 'AT_HUB', 1, 8.0)
medium_priority.time_tracker.initialize_multiple_package_status(medium_priority.get_packages(), 'AT_HUB', 2, 9.05)

# Placeholder for packages that will be delivered by truck 3, Truck 3 will have new time_to_start_delivery
# and current_time attributes to reflect the time it will start delivering packages
low_priority.time_tracker.initialize_multiple_package_status(low_priority.get_packages(), 'AT_HUB', 3, 8.0)

# Sort packages on trucks
sort_packages_on_truck(high_priority, graph_access)
sort_packages_on_truck(medium_priority, graph_access)
sort_packages_on_truck(low_priority, graph_access)

truck_list = [high_priority, medium_priority, low_priority]
deliver_packages(truck_list, graph_access, '8:35', '9:25')
deliver_packages(truck_list, graph_access, '9:35', '10:25')
deliver_packages(truck_list, graph_access, '12:03', '1:12')

# for package, status_info in filtered_packages:
#     print(f"Package ID: {package.package_id} - Address: {package.address} - Status: {status_info}")
# print("HIGH_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", high_priority.get_package_count())
# print()
# high_priority.print_packages()
# print("---NEW LINE---\n")
#
# print("MEDIUM_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", medium_priority.get_package_count())
# print()
# medium_priority.print_packages()
# print("---NEW LINE---\n")
#
# print("LOW_PRIORITY WITHOUT CONSTRAINTS: ", "COUNT: ", low_priority.get_package_count())
# print()
# low_priority.print_packages()
#
#
# sort_packages_on_truck(high_priority, graph_access)
# sort_packages_on_truck(medium_priority, graph_access)
# sort_packages_on_truck(low_priority, graph_access)
#
# # Find optimal route using two-opt algorithm
# two_opt_route(high_priority, graph_access)
# two_opt_route(medium_priority, graph_access)
# two_opt_route(low_priority, graph_access)
#
#
# Initialize packages loaded onto truck status to 'AT_HUB'
# high_loaded_packages = high_priority.get_packages()
# medium_loaded_packages = medium_priority.get_packages()
# low_loaded_packages = low_priority.get_packages()
# high_priority.time_tracker.initialize_multiple_package_status(high_loaded_packages, 'AT_HUB', 1, 8.0)
# medium_priority.time_tracker.initialize_multiple_package_status(medium_loaded_packages, 'AT_HUB', 2, 9.05)
# low_priority.time_tracker.initialize_multiple_package_status(low_loaded_packages, 'AT_HUB', 3, 8.0)


# print('---NEW LINE---\n')
# print("HIGH_PRIORITY", high_priority.time_tracker.print_package_status())
# print()
# print("MEDIUM_PRIORITY", medium_priority.time_tracker.print_package_status())
# print()
# print("LOW_PRIORITY", low_priority.time_tracker.print_package_status())
# print("---NEW LINE---\n")
# initialize_optimized_trucks(high_priority, medium_priority, low_priority, graph_access, track_package_id1)

# Simulate package delivery
# trucks_list = [high_priority, medium_priority, low_priority]
# deliver_packages(trucks_list, graph_access)
# print("HIGH_PRIORITY", high_priority.time_tracker.print_package_status())

# # Print the packages delivered and the time upon completion
# print("HIGH_PRIORITY")
# high_priority.time_tracker.print_package_status()
# print()
# high_priority.time_tracker.print_delivery_status(high_priority)
#
# print()
# print("MEDIUM_PRIORITY")
# medium_priority.time_tracker.print_delivery_status(medium_priority)
# print()
# print("LOW_PRIORITY")
# low_priority.time_tracker.print_delivery_status(low_priority)


# # Trucks unoptimized route starting at hub '4001 South 700 East'
# high_priority_unoptimized = high_priority.route.copy()
# high_priority_unoptimized.insert(0, '4001 South 700 East')
# medium_priority_unoptimized = medium_priority.route.copy()
# medium_priority_unoptimized.insert(0, '4001 South 700 East')
# low_priority_unoptimized = low_priority.route.copy()
# low_priority_unoptimized.insert(0, '4001 South 700 East')

# print("HIGH_PRIORITY_UNOPTIMIZED ROUTE", high_priority_unoptimized)
# print()
# print("MEDIUM_PRIORITY_UNOPTIMIZED ROUTE", medium_priority_unoptimized)
# print()
# print("LOW_PRIORITY_UNOPTIMIZED ROUTE", low_priority_unoptimized)


# print("\nNEW LINE---\n")
# print("HIGH_PRIORITY EDGE_WEIGHT: ", Trucks.get_edge_weights([high_priority]))
# print("MEDIUM_PRIORITY EDGE_WEIGHT: ", Trucks.get_edge_weights([medium_priority]))
# print("LOW_PRIORITY EDGE_WEIGHT: ", Trucks.get_edge_weights([low_priority]))

# print("\nNEW LINE---\n")

# high_load = find_shortest_route_to_deliver(high_priority, graph_access)
# print("HIGH_PRIORITY ROUTE BEFORE: ", high_priority.route)
# print()
# print("HIGH_SHORTEST_ROUTE AFTER DIJKSTRA TOTAL_DISTANCE: ", high_load)
# print("\n")

# HIGH PRIORITY TRUCK
# print("HIGH_OPTIMIZED_ROUTE: ", high_priority.route)

# print("HIGH_PRIORITY TWO_OPT_ROUTE: ", high_priority.route)
# high_load_two_opt = find_shortest_route_to_deliver(high_priority, graph_access)
# print("HIGH_PRIORITY AFTER TWO_OPT_ROUTE TOTAL_DISTANCE: ", high_load_two_opt)
# print("\n")

# MEDIUM PRIORITY TRUCK
# medium_load = find_shortest_route_to_deliver(medium_priority, graph_access)
# print("MEDIUM_PRIORITY ROUTE BEFORE: ", medium_priority.route)
# print()
# print("MEDIUM_SHORTEST_ROUTE AFTER DIJKSTRA TOTAL_DISTANCE: ", medium_load)
# print("\n")

# print("MEDIUM_PRIORITY TWO_OPT_ROUTE: ", medium_priority.route)
# medium_load_two_opt = find_shortest_route_to_deliver(medium_priority, graph_access)
# print("MEDIUM_PRIORITY AFTER TWO_OPT_ROUTE TOTAL_DISTANCE: ", medium_load_two_opt)
# print("\n")

# LOW PRIORITY TRUCK
# low_load = find_shortest_route_to_deliver(low_priority, graph_access)
# print("LOW_PRIORITY ROUTE BEFORE", low_priority.route)
# print()
# print("LOW_SHORTEST_ROUTE AFTER DIJKSTRA TOTAL_DISTANCE: ", low_load)
# print("\n")

# print("LOW_PRIORITY TWO_OPT_ROUTE: ", low_priority.route)
# low_load_two_opt = find_shortest_route_to_deliver(low_priority, graph_access)
# print("LOW_PRIORITY AFTER TWO_OPT_ROUTE TOTAL_DISTANCE: ", low_load_two_opt)
# print("\n")

# left_over2 = left_over_packages(graph_access, track_package_id1)
# print("LEFT_OVER2: ", left_over2)
# print("\n")

# print("HIGH_PRIORITY STATUS")
# high_priority.time_tracker.print_package_status()
# print()
#
# print("MEDIUM_PRIORITY STATUS")
# medium_priority.time_tracker.print_package_status()
# print()
#
# print("LOW_PRIORITY STATUS")
# low_priority.time_tracker.print_package_status()
# print()
