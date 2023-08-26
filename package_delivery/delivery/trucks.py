from package_delivery.algorithms.load_nearest_neighbor import load_packages_nearest_neighbor
from package_delivery.algorithms.two_opt_route import two_opt_route
from package_delivery.datastructures.graph import graph_access
from package_delivery.algorithms.dijkstra_algo import dijkstra
from package_delivery.datastructures.hash_map import package_hashmap
from package_delivery.loadutil.load_util import get_left_over_packages
from package_delivery.loadutil.load_util import load_left_over_packages
from package_delivery.loadutil.load_util import track_package_id1
from package_delivery.delivery.time_tracker import TimeTracker

# Each truck can carry a maximum of 16 packages
#
# Three trucks(Truck 1, 2, 3), two drivers available for delivery,
# each driver stays with the same truck until all packages delivered
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


# Initialize an empty list to track left_over packages across trucks not loaded after
# initially loading packages with specific constraints and delivery_deadline functions
left_over1 = []


class Trucks:
    """
    Class to represent the trucks that will be used to deliver packages.

    Attributes:
        packages (list): A list of packages.
        route (list): A list of vertices representing the route.
        distances (list): A list of distances.
        pred_vertex (list): A list of predecessor vertices.
        time_tracker (TimeTracker): A TimeTracker object to extend the functionality of Trucks class
        truck_id (int): The ID of the truck.
    """
    # List of packages, route, distances, predecessor vertices to be loaded onto a Trucks object
    def __init__(self):
        """
        Initialize the truck object
        """
        self.packages = []
        self.route = []
        self.distances = []
        self.pred_vertex = []
        # # Create an instance of TimeTracker class to extend the functionality of Trucks class
        self.time_tracker = TimeTracker()
        # Associate truck ID with Trucks object
        self.truck_id = 0

    def insert_truck_id(self, truck_id):
        """
        Set the truck ID for the current instance.

        Args:
            truck_id (any): The ID of the truck to be set.

        Returns:
            None
        """
        self.truck_id = truck_id

    # Insert packages to list self.packages and address of package to route to
    # list self.route
    def insert_packages(self, package):
        """
        Insert a package into the list of packages and update the routing address.

        Parameters:
            package (Package): The package object to be inserted.

        Returns:
            None
        """
        self.packages.append(package)
        self.route.append(package.address)

    # Return the list of packages from Trucks object
    def get_packages(self):
        """
        Get the packages associated with this object.

        Returns:
            packages (list): A list of packages associated with this object.
        """
        return self.packages

    # Remove package from a Truck object after delivered
    # and remove address from route
    def remove_packages(self, package):
        """
        Remove a package from the list of packages and its corresponding route.

        Parameters:
            package (Package): The package object to be removed.

        Returns:
            None
        """
        self.packages.remove(package)
        self.route.remove(package.address)

    def insert_distances_pred_vertex(self, distance, pred_vertex):
        """
        Add a distance and pred_vertex to the list of distances and pred_vertex.

        Parameters:
            distance (float): The distance to be added.
            pred_vertex (str): The pred_vertex to be added.

        Returns:
            None
        """
        self.distances.append(distance)
        self.pred_vertex.append(pred_vertex)

    def get_distances(self):
        """
        Get the distances.

        Returns:
            list: The list of distances.
        """
        return self.distances

    # Print all-packages list for Trucks object, useful to see what packages are loaded on
    # the trucks that are ordered by priority of deadline to delivery
    def print_packages(self):
        """
        Print the packages in the `self.packages` list.
        """
        for package in self.packages:
            print(package)

    # Print route for Trucks object
    def print_route(self):
        """
        Print the current route.

        This function prints the value of the `route` attribute of the current object.

        Parameters:
            self (Trucks): The current object.

        Returns:
            None
        """
        print(self.route)

    # Return the count of list packages for Trucks object
    def get_package_count(self):
        """
        Calculates the number of packages in the current instance of the class.

        Returns:
            int: The number of packages in the current instance.
        """
        return len(self.get_packages())

    # Set the edge_weight for all packages on truck
    @staticmethod
    def set_edge_weight(truck_obj):
        """
        Set the edge weight for each package in the given truck.

        Args:
            truck_obj (Trucks): The truck object for which to set the edge weights.

        Returns:
            None
        """
        # From hub
        start_vertex = '4001 South 700 East'
        # Calculate edge weight between the package's location and the truck's starting location
        for package in truck_obj.get_packages():
            # Destination address of second package
            dest_vertex = package.address
            if start_vertex in graph_access.edge_weight and dest_vertex in graph_access.edge_weight:
                edge_weight = graph_access.edge_weight[start_vertex][dest_vertex]
                package.edge_weight = edge_weight
            else:
                # Handle the case where the edge weight is not found in the graph
                package.edge_weight = None


# Forty packages, 9 + 16 + 15 respectively? for trucks, maximum number of packages to load
# Start hub = '4001 South 700 East', load all trucks at hub
# priority_queue to pop off packages on trucks until empty?
# Once the first truck is empty driver returns to the hub to get the next truck for deliveries
def load_trucks(truck_high_priority, truck_medium_priority, truck_low_priority, graph, track_package_id):
    # # Define the arguments as a single variable
    # # Load high priority
    # delivery_deadline1 = "9:00 AM"
    # # packages besides 15, 14, 19, 16, 13, 20 share same package.address for some on loaded on truck
    # constraint_list1 = [15, 14, 19, 16, 13, 20, 39, 21]
    # args1 = {
    #     'trucks': truck_high_priority,
    #     'graph': graph,
    #     'delivery_deadline': delivery_deadline1,
    #     'constraints': constraint_list1,
    #     'track_package_id': track_package_id,
    #     # 'track_time': track_time1
    # }
    # load_packages(**args1)
    # Trucks.set_edge_weight(truck_high_priority)
    #
    # # Load medium priority
    # delivery_deadline2 = "10:30 AM"
    # constraint_list2 = "Can only be on truck 2"
    # args2 = {
    #     'trucks': truck_medium_priority,
    #     'graph': graph,
    #     'delivery_deadline': delivery_deadline2,
    #     'constraints': constraint_list2,
    #     'track_package_id': track_package_id,
    # }
    # load_packages(**args2)
    # Trucks.set_edge_weight(truck_medium_priority)
    #
    # # Load low priority
    # delivery_deadline3 = "EOD"
    # constraint_list3 = None
    #
    # args3 = {
    #     'trucks': truck_low_priority,
    #     'graph': graph,
    #     'delivery_deadline': delivery_deadline3,
    #     'constraints': constraint_list3,
    #     'track_package_id': track_package_id,
    # }
    # load_packages(**args3)
    # Trucks.set_edge_weight(truck_low_priority)

    # Load packages onto trucks using the nearest neighbor algorithm
    trucks = [truck_high_priority, truck_medium_priority, truck_low_priority]
    load_packages_nearest_neighbor(trucks, graph, track_package_id)

    # After loading packages to satisfy constraints,
    # Combine the left-over packages from all three priority levels
    left_over1.append(get_left_over_packages(graph_access, track_package_id1))
    # Load left-over packages onto non-full trucks
    load_left_over_packages(high_priority, left_over1, track_package_id1)
    load_left_over_packages(medium_priority, left_over1, track_package_id1)
    load_left_over_packages(low_priority, left_over1, track_package_id1)


# Calculate the shortest route to deliver packages to destination
# and back to hub after applying Dijkstra's algorithm
def _find_shortest_route_to_deliver(truck_obj, graph):
    """
    Find the shortest route for a truck to deliver packages.

    Parameters:
        truck_obj (Truck): The truck object representing the delivery truck.
        graph (Graph): The graph object representing the delivery network.

    Returns:
        int: The total distance traveled by the truck to deliver all the packages.
    """
    # Make a copy of the packages on the truck
    packages_copy = truck_obj.get_packages().copy()
    # Starting location for all trucks, i.e., the hub
    start_vertex1 = truck_obj.route[0]
    # Initialize total_distance traveled by truck to 0
    total_distance = 0
    # Calculate the shortest distances and pred_vertex using Dijkstra's algorithm of the truck's route
    distances1, pred_vertex1 = dijkstra(graph, start_vertex1, truck_obj.route)
    # Use a for loop to iterate over the packages
    for package in packages_copy:
        # Vertex to travel to
        dest_vertex = package.address

        # Insert the calculated distances and pred_vertex into the Trucks object
        truck_obj.insert_distances_pred_vertex(distances1[dest_vertex], pred_vertex1[dest_vertex])
        # Update time during delivery
        time_delivered = truck_obj.time_tracker.update_current_truck_time(distances1[dest_vertex], truck_obj.truck_id)
        # Insert the time_delivered into package
        truck_obj.time_tracker.insert_current_truck_time_to_package(package, time_delivered)
        # Update the time for other packages with the same address
        for other_package, status_info in truck_obj.time_tracker.packages_status.items():
            if (other_package != package and other_package.address == package.address and status_info['status'] !=
                    'DELIVERED'):
                truck_obj.time_tracker.insert_current_truck_time_to_package(other_package, time_delivered)
        # Skip adding the distance if the next package is already at the dest_vertex, share addresses
        if distances1[dest_vertex] != 0:
            total = distances1[dest_vertex]
            total_distance += total

    return total_distance


# Simulate delivering of packages
# Function to deliver packages using the TimeTracker instances inside each truck
def deliver_packages(trucks, graph, start_interval, end_interval):
    """
    Delivers packages using a list of trucks, a graph, and time intervals.

    Parameters:
    - trucks (list): A list of truck objects representing the available trucks.
    - graph (Graph): A graph object representing the delivery locations and distances.
    - start_interval (str): The start time interval for package delivery.
    - end_interval (str): The end time interval for package delivery.

    Returns:
    None
    """
    # Define a mapping of truck objects to their names
    truck_names = {
        high_priority: "HIGH_PRIORITY",
        medium_priority: "MEDIUM_PRIORITY",
        low_priority: "LOW_PRIORITY"
    }
    # Flag to track if truck 1's delivery is completed
    is_delivery_completed = False

    for current_truck in trucks:
        # Current truck time tracker high_priority, medium_priority, low_priority
        time_tracker = current_truck.time_tracker
        # Get the name of the current truck
        truck_name = truck_names[current_truck]
        # Initialize tracking trucks
        time_tracker.insert_current_truck(current_truck.truck_id)
        print("NEW LINE---\n")
        # Check if the current truck is ready for delivery
        if current_truck.time_tracker.is_ready_to_deliver(current_truck):
            # # Only print the route if the current truck is truck1 or truck2
            # if current_truck == high_priority or current_truck == medium_priority:
            #     print(f"{truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", current_truck.route)
            # Only deliver packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                # Call the function two_opt_route to find the optimized route for the current truck
                two_opt_route(current_truck, graph)
                # Call the function to find the shortest route to deliver packages
                total_distance = _find_shortest_route_to_deliver(current_truck, graph)
                # Update miles traveled for the current truck
                time_tracker.update_miles_traveled(total_distance, current_truck.truck_id)

            # Check if the start time is 9:35 AM and update at 10:20 AM
            # If so, update the package with ID 9 to the new address
            if start_interval == '9:35 AM':
                package_to_update = package_hashmap.get_value_from_key(9)  # Get the package object
                new_address = '410 S State St'
                new_city = 'Salt Lake City'
                new_state = 'UT'
                new_zipcode = '84111'
                new_special_notes = 'Address updated from 300 State St to 410 S State St'
                time_tracker.update_package_status(package_to_update, new_address, new_city, new_state, new_zipcode,
                                                   new_special_notes)
                print("PACKAGE UPDATED, Address updated from 300 State St to 410 S State St: #9")

            # Check if truck 1 has completed its delivery
            if current_truck == high_priority and current_truck.time_tracker.is_delivery_completed():
                is_delivery_completed = True

            if current_truck == low_priority:
                if is_delivery_completed and current_truck.time_tracker.is_ready_to_deliver(current_truck):
                    deliver_truck3_packages(current_truck, graph, start_interval, end_interval)
            # Only filter packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                filtered_packages = current_truck.time_tracker.filter_packages_by_time_range(start_interval,
                                                                                             end_interval)
                print("Start time:", start_interval, "End time:", end_interval)
                print("FILTERED_PACKAGES:", filtered_packages)
                print("TRUCK ROUTE:", current_truck.route)
                time_tracker.print_current_truck_miles(current_truck.truck_id)


# After truck 1's delivery is completed, deliver truck 3's packages
def deliver_truck3_packages(truck3, graph, start_interval, end_interval):
    """
    Deliver packages using truck 3 based on the provided parameters.

    Parameters:
        truck3 (Truck): The truck object representing truck 3.
        graph (Graph): The graph object representing the delivery locations.
        start_interval (str): The start time interval for package delivery.
        end_interval (str): The end time interval for package delivery.

    Returns:
        None
    """
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
    total_distance = _find_shortest_route_to_deliver(truck3, graph)
    # Update miles traveled for the current truck
    time_tracker.update_miles_traveled(total_distance, truck3.truck_id)

    filtered_packages = truck3.time_tracker.filter_packages_by_time_range(start_interval, end_interval)
    print("Start time:", start_interval, "End time:", end_interval)
    print("FILTERED_PACKAGES:", filtered_packages)

    time_tracker.print_current_truck_miles(truck3.truck_id)


# Delivered by 9:00am, the constraint of having multiple packages on the same truck delivered together, Truck 1
high_priority = Trucks()
high_priority.insert_truck_id(1)
# Delivered by 10:30am, the constraint of having multiple packages required on, Truck 2
medium_priority = Trucks()
medium_priority.insert_truck_id(2)
# Delivered by EOD, no constraints required for packages EOD will be defined as 5:00pm, Truck 3
low_priority = Trucks()
low_priority.insert_truck_id(3)

# Load trucks
load_trucks(high_priority, medium_priority, low_priority, graph_access, track_package_id1)

# Initialize packages
high_priority.time_tracker.initialize_multiple_package_status(high_priority.get_packages(), 'AT_HUB', 1, 8.0)
medium_priority.time_tracker.initialize_multiple_package_status(medium_priority.get_packages(), 'AT_HUB', 2, 9.05)

# Placeholder for packages that will be delivered by truck 3, Truck 3 will have new time_to_start_delivery
# and current_time attributes to reflect the time it will start delivering packages
low_priority.time_tracker.initialize_multiple_package_status(low_priority.get_packages(), 'AT_HUB', 3, 8.0)

trucks_list = [high_priority, medium_priority, low_priority]
deliver_packages(trucks_list, graph_access, '12:03 PM', '1:12 PM')

# Working on to calculate total miles traveled of all trucks
total_miles_traveled = 0
for truck in trucks_list:
    total_miles_traveled += truck.time_tracker.calculate_total_miles_traveled()
print("Total miles traveled:", total_miles_traveled)
high_priority.time_tracker.lookup_single_package_status(15, '7:00 AM')
