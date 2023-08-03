import math

from AdjacencyMatrix import graph_access
from DijkstraAlgo import dijkstra
from Tracking import TimeTracker

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


# Calculate the shortest routes for all vertices in the graph before loading the trucks
# dijkstra(graph_access, '4001 South 700 East')


class Trucks:
    # List of packages, route, distances, predecessor vertices to be loaded onto Trucks object
    def __init__(self):
        self.packages = []
        self.route = []
        self.distances = []
        self.pred_vertex = []
        # # Create an instance of TimeTracker if it doesn't exist
        self.time_tracker = TimeTracker()

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
        print(self.packages)

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


# 40 packages, 16 + 16 + 8 respectively? for trucks, maximum amount of packages to load
# Start hub = '4001 South 700 East', load all trucks at hub
# priority_queue to pop off packages on trucks until empty?
# Once first truck is empty driver returns to hub to get next truck for deliveries
def load_trucks(truck_high_priority, truck_medium_priority, truck_low_priority, graph, track_package_id):
    # Set the edge_weight for all packages on truck
    def set_edge_weight(truck):
        # From hub
        start_vertex = '4001 South 700 East'
        # Calculate edge weight between the package's location and the truck's starting location
        for package in truck.get_packages():
            # Destination address of second package
            dest_vertex = package.address
            if start_vertex in graph.edge_weight and dest_vertex in graph.edge_weight:
                edge_weight = graph.edge_weight[start_vertex][dest_vertex]
                package.edge_weight = edge_weight
            else:
                # Handle the case where the edge weight is not found in the graph
                package.edge_weight = None

    # Define the arguments as a single variable
    # Load high priority
    delivery_deadline1 = "9:00 AM"
    # packages besides 15, 14, 19, 16, 13, 20 share same package.address for some on loaded on truck
    constraint_list1 = [15, 14, 19, 16, 13, 20, 39, 21]
    # Track status of packages and trucks from start of day to end of day
    track_time1 = truck_high_priority.time_tracker
    args1 = {
        'trucks': truck_high_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline1,
        'constraints': constraint_list1,
        'track_package_id': track_package_id,
        'track_time': track_time1
    }
    load_packages(**args1)
    set_edge_weight(truck_high_priority)

    # Load medium priority
    delivery_deadline2 = "10:30 AM"
    constraint_list2 = "Can only be on truck 2"
    track_time2 = truck_medium_priority.time_tracker
    args2 = {
        'trucks': truck_medium_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline2,
        'constraints': constraint_list2,
        'track_package_id': track_package_id,
        'track_time': track_time2
    }
    load_packages(**args2)
    set_edge_weight(truck_medium_priority)

    # Load low priority
    delivery_deadline3 = "EOD"
    constraint_list3 = None
    track_time3 = truck_low_priority.time_tracker

    args3 = {
        'trucks': truck_low_priority,
        'graph': graph,
        'delivery_deadline': delivery_deadline3,
        'constraints': constraint_list3,
        'track_package_id': track_package_id,
        'track_time': track_time3
    }
    load_packages(**args3)
    set_edge_weight(truck_low_priority)

    # After loading packages to satisfy constraints
    # Combine the left-over packages from all three priority levels
    left_over1.append(left_over_packages(graph_access, track_package_id1))
    # print()
    # print("LEFT_OVER_PACKAGES1 BEFORE FUNCTION LOAD_LEFT_OVER: ", left_over1)
    # Load left-over packages onto non-full trucks
    load_left_over_packages(high_priority, left_over1, track_package_id1, track_time1)
    load_left_over_packages(medium_priority, left_over1, track_package_id1, track_time2)
    load_left_over_packages(low_priority, left_over1, track_package_id1, track_time3)
    # print("NEWLINE ---\n")


# Load packages onto trucks with specific delivery_deadline and constraints required for each truck
def load_packages(trucks, graph, delivery_deadline, constraints, track_package_id, track_time):
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
                                    # track_time.insert_package_status(package, 'AT_HUB')
                else:
                    trucks.insert_packages(load_package)
        #     print("LOW_PRIORITY WITHOUT CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
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
                                        # track_time.insert_package_status(package, 'AT_HUB')
                    else:
                        trucks.insert_packages(load_package)
            # print("HIGH_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
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
                                        # track_time.insert_package_status(package, 'AT_HUB')
                    else:
                        trucks.insert_packages(load_package)
            # print("MEDIUM_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", len(trucks.get_packages()))
            # print()
            # trucks.print_packages()
            # print("---NEW LINE---\n")
    # if truck_high_priority is not None:
    #     load_package = Trucks.get_package_deadline_constraints_high_asc(**args2)
    #     trucks.insert_packages(load_package)
    # print("WITH CONSTRAINTS Trucks.get_package_deadline_constraints_high_asc(**args3) : ")
    # trucks.print_packages()


# Implement the nearest neighbor algorithm,
# sort the order of the packages loaded on Trucks object after loading the packages;
# this is to reduce the total_distance traveled when calling the 'find_shortest_route_to_deliver'
# function that where we implement dijkstra's algorithm
def sort_packages_on_truck(trucks, graph):
    # Start from the hub
    current_vertex = '4001 South 700 East'
    sorted_packages = []
    sorted_route = []

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
        sorted_packages.append(nearest_package)
        sorted_route.append(nearest_package.address)
        current_vertex = nearest_package.address
        trucks.remove_packages(nearest_package)
    trucks.packages = sorted_packages
    trucks.route = sorted_route
    # print()
    # print("SORTED_PACKAGES: ", sorted_packages)
    # print()


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
def load_left_over_packages(trucks, left_over, track_package_id, track_time):
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


# Core algorithm, implementing dijkstra's algorithm, calculate the shortest route to deliver packages to destination
# and back to hub. After loading all packages and left_over packages, and sorting packages,
# utilize dijkstra's algorithm to find the shortest route distance to deliver all packages
# def find_shortest_route_to_deliver(trucks, graph):
#     global optimized_route, pred_vertex1
#     # Starting location for all trucks
#     start_vertex1 = '4001 South 700 East'
#     # Initialize total_distance traveled by truck to 0
#     total_distance = 0
#     loaded_packages = trucks.get_packages()
#     for package in trucks.get_packages():
#         dest_vertex = package.address
#         print("DEST_VERTEX: ", dest_vertex)
#         distances1, pred_vertex1 = dijkstra(graph, start_vertex1, loaded_packages)
#         trucks.insert_distances_pred_vertex(distances1[dest_vertex], pred_vertex1[dest_vertex])
#         # Skip adding the distance if the next package is already at the dest_vertex
#         if distances1[dest_vertex] != 0:
#             total = distances1[dest_vertex]
#             total_distance += total
#         # Update start_vertex1 to the dest_vertex1 for the next iteration
#             start_vertex1 = dest_vertex
#     optimized_route = find_efficient_route(pred_vertex1, start_vertex1, '4001 South 700 East')
#     # Calculate the distance of the optimized route back to the hub
#     for i in range(len(optimized_route) - 1):
#         from_vertex = optimized_route[i]
#         to_vertex = optimized_route[i+1]
#         total = graph_access.edge_weight[from_vertex][to_vertex]
#         total_distance += total
#     print("OPTIMIZED_ROUTE BACK TO HUB: ", optimized_route)
#     print("\n")
#     total_distance = round(total_distance, 2)
#
#     return total_distance
# Calculate the shortest route to deliver packages to destination
# and back to hub after applying Dijkstra's algorithm
def find_shortest_route_to_deliver(truck, graph):
    # Starting location for all trucks, i.e. the hub
    start_vertex1 = '4001 South 700 East'
    # Initialize total_distance traveled by truck to 0
    total_distance = 0
    # Will make a copy of the pred_vertex to be able to use to find last package.address
    # and add route distance back to the hub
    pred_vertex_copy = []
    
    # Use a while loop to iterate over the packages
    while truck.get_packages():
        # Remove the first package from the truck
        package = truck.get_packages().pop(0)
        
        # Vertex to travel to
        dest_vertex = package.address
        # Calculate the shortest distances and pred_vertex using Dijkstra's algorithm
        distances1, pred_vertex1 = dijkstra(graph, start_vertex1)
        # Make a copy of pred_vertex list to use for to find route back to hub
        pred_vertex_copy.append(pred_vertex1.copy())
        # Insert the calculated distances and pred_vertex into the Trucks object
        truck.insert_distances_pred_vertex(distances1[dest_vertex], pred_vertex1[dest_vertex])
        # Update time during delivery
        truck.time_tracker.update_current_truck_time(distances1[dest_vertex], truck)
        # Skip adding the distance if the next package is already at the dest_vertex, share addresses
        if distances1[dest_vertex] != 0:
            total = distances1[dest_vertex]
            total_distance += total
        # Mark package as 'DELIVERED'
        truck.time_tracker.mark_package_delivered(package)
        # Update start_vertex1 to the dest_vertex1 for the next iteration
        start_vertex1 = dest_vertex
        # Debug print, pred_vertex and dest_vertex pair for the current destination
        # print(f"Pred Vertex: {pred_vertex1[dest_vertex]}, Destination: {dest_vertex}")
    
    # Route of last package back to hub
    optimized_route_back_to_hub = find_optimized_route_back_to_hub(pred_vertex_copy, start_vertex1,
                                                                   '4001 South 700 East')
    # Calculate the distance of the optimized route back to the hub
    for i in range(len(optimized_route_back_to_hub)):
        from_vertex = optimized_route_back_to_hub[i]
        distances1, _ = dijkstra(graph_access, from_vertex)
        total = distances1[from_vertex]
        total_distance += total

    total_distance = round(total_distance, 2)
    # truck.time_tracker.print_package_status()

    return total_distance


# Simulate delivering of packages
# Function to deliver packages using the TimeTracker instances inside each truck
def deliver_packages(trucks, graph):
    # Define a mapping of truck objects to their names
    truck_names = {
        high_priority: "HIGH_PRIORITY",
        medium_priority: "MEDIUM_PRIORITY",
        low_priority: "LOW_PRIORITY"
    }
    for current_truck in trucks:
        # Current truck time tracker high_priority, medium_priority, low_priority
        time_tracker = current_truck.time_tracker
        # Get the name of the current truck
        truck_name = truck_names[current_truck]
        # Call the function to find the shortest route to deliver packages
        print(f"{truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", current_truck.route)
        optimized_route_back_to_hub = find_optimized_route_back_to_hub(
            current_truck.pred_vertex, current_truck.route[-1], '4001 South 700 East'
        )
        print("BACK_TO_HUB:", optimized_route_back_to_hub)
        total_distance = find_shortest_route_to_deliver(current_truck, graph)
        # Update miles traveled for the current truck
        time_tracker.update_miles_traveled(total_distance, current_truck)
        time_tracker.print_delivery_status(current_truck)
        time_tracker.print_miles_traveled(current_truck)


def two_opt_swap(route, i, j):
    new_route = route[:i] + list(reversed(route[i:j + 1])) + route[j + 1:]
    return new_route


def calculate_route_distance(route, graph):
    total_distance = 0
    for i in range(len(route) - 1):
        from_vertex = route[i]
        to_vertex = route[i + 1]
        total_distance += graph.edge_weight[from_vertex][to_vertex]
    return total_distance


# Remove repeated vertices in the route list
def remove_repeated_vertices(route):
    # Create new list with first vertex from current route
    unique_route = [route[0]]
    for vertex in route:
        # If the current vertex is different from the last vertex added to the unique route,
        # then add the current vertex to the unique route list
        if vertex != unique_route[-1]:
            unique_route.append(vertex)
    return unique_route


# Implement the two-opt algorithm, optimize the order of addresses in route in
# conjunction to utilizing dijkstra's algorithm
# Used to further decrease the total_distance traveled by the three trucks after nearest neighbor algorithm
def two_opt_route(trucks, graph):
    # Only unique address on the route list
    unique_route = remove_repeated_vertices(trucks.route)
    # Initialize the unique_route to the current_route
    current_route = unique_route
    # Will be best optimized route
    best_route = current_route
    improvement = True
    # Continue to optimize until no further improvements are made
    while improvement:
        improvement = False
        # Iterate through each vertex in the route except the first and last
        for i in range(1, len(current_route) - 1):
            for j in range(i + 1, len(current_route)):
                # Create new route
                new_route = two_opt_swap(current_route, i, j)
                # Calculate distance of new_route
                new_distance = calculate_route_distance(new_route, graph)
                # If new_distance is improvement of current best_route then update
                if new_distance < calculate_route_distance(best_route, graph):
                    best_route = new_route
                    improvement = True
        # Set current_route to best_route in this iteration
        current_route = best_route

    # Update the truck's route with the optimized route
    trucks.route = best_route

    # Optimize the order of packages to reflect the optimized route
    optimized_packages = []
    for address in current_route:
        for package in trucks.get_packages():
            if package.address == address:
                optimized_packages.append(package)
                break
    trucks.packages = optimized_packages


# Find route back to hub from last package.address delivered
def find_optimized_route_back_to_hub(pred_list, destination_vertex, hub_vertex):
    efficient_route = []
    current_vertex = destination_vertex
    while current_vertex != hub_vertex:
        efficient_route.append(current_vertex)
        # No route to start_vertex, terminate the loop
        if current_vertex not in pred_list:
            break
        current_vertex = pred_list[current_vertex]
    # In case the last element of pred_vertex is None, don't include it in the route
    if efficient_route and efficient_route[-1] is None:
        efficient_route.pop()
    efficient_route.append(hub_vertex)
    return efficient_route


# Delivered by 9:00am, constraint of having multiple packages on same truck delivered together, Truck 1
high_priority = Trucks()
# Delivered by 10:30am, constraint of having multiple packages required on, Truck 2
medium_priority = Trucks()
# Delivered by EOD, no constraints required for packages EOD will be defined as 5:00pm, Truck 3
low_priority = Trucks()

# Load trucks
load_trucks(high_priority, medium_priority, low_priority, graph_access, track_package_id1)

# Initialize packages loaded onto truck status to 'AT_HUB'
high_loaded_packages = high_priority.get_packages()
medium_loaded_packages = medium_priority.get_packages()
low_loaded_packages = low_priority.get_packages()
high_priority.time_tracker.initialize_multiple_package_status(high_loaded_packages, 'AT_HUB')
medium_priority.time_tracker.initialize_multiple_package_status(medium_loaded_packages, 'AT_HUB')
low_priority.time_tracker.initialize_multiple_package_status(low_loaded_packages, 'AT_HUB')

# Initialize tracking trucks
high_priority.time_tracker.insert_current_truck(high_priority)
medium_priority.time_tracker.insert_current_truck(medium_priority)
low_priority.time_tracker.insert_current_truck(low_priority)

# Sort the packages with nearest neighbor algorithm loaded on trucks
sort_packages_on_truck(high_priority, graph_access)
sort_packages_on_truck(medium_priority, graph_access)
sort_packages_on_truck(low_priority, graph_access)

# Find optimal route using two-opt algorithm
two_opt_route(high_priority, graph_access)
two_opt_route(medium_priority, graph_access)
two_opt_route(low_priority, graph_access)

# Simulate package delivery
trucks_list = [high_priority, medium_priority, low_priority]
deliver_packages(trucks_list, graph_access)

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
# print("HIGH_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", len(high_priority.get_packages()))
# print()
# high_priority.print_packages()
# print("---NEW LINE---\n")
#
# print("MEDIUM_PRIORITY WITH CONSTRAINTS: ", "COUNT: ", len(medium_priority.get_packages()))
# print()
# medium_priority.print_packages()
# print("---NEW LINE---\n")
#
# print("LOW_PRIORITY WITHOUT CONSTRAINTS: ", "COUNT: ", len(low_priority.get_packages()))
# print()
# low_priority.print_packages()


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
# print("HIGH_PRIORITY_COUNT", high_priority.get_package_count())
# print("MEDIUM_PRIORITY_COUNT", medium_priority.get_package_count())
# print("LOW_PRIORITY_COUNT", low_priority.get_package_count())

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
