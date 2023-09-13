from package_delivery import algorithms as algo
from package_delivery import datastructures as ds
from package_delivery.delivery.logistics.fuel_tracker import FuelTracker
from package_delivery.delivery.logistics.time_tracker import TimeTracker
from package_delivery.loadutil import load_util as util
from package_delivery.visualization.visualize import Visualize

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
        filtered_packages (list): A list of packages that have been filtered by time.
        route (list): A list of vertices representing the route from finding the shortest path.
        distances (list): A list of distances calculated from finding the shortest path.
        pred_vertex (list): A list of predecessor vertices from finding the shortest path.
        time_tracker (TimeTracker): A TimeTracker object to track status of packages.
        visualize (Visualize): A Visualize object to visualize delivery.
        fuel_tracker (FuelTracker): A FuelTracker object to track fuel consumption during delivery.
        __truck_id (int): The ID of the truck.
        __truck_name (str): The name of the truck.
    """

    # All the necessary attributes to represent a truck
    def __init__(self, truck_id, truck_name):
        """
        Initialize the truck object
        """
        self.packages = []
        self.filtered_packages = []
        self.route = []
        self.distances = []
        self.pred_vertex = []
        # Associate truck ID with Trucks object
        self.__truck_id = truck_id
        self.__truck_name = truck_name
        # Composite class relationship, Trucks object 'has a' TimeTracker object relationship to track the status of
        # packages
        self.time_tracker = TimeTracker(self.__truck_id)
        # Composite class relationship, Trucks object 'has a' Visualize object relationship to visualize a delivery
        # Modified singleton design pattern to manage the visual state of each truck
        self.visualize = Visualize(self.__truck_id)
        # Composite class relationship, Trucks object 'has a' FuelTracker object relationship to track a fuel
        # Singleton design pattern to manage the data state of each truck
        self.fuel_tracker = FuelTracker(self.__truck_id)

    @property
    def truck_id(self):
        """
        Get the truck ID.

        Returns:
            int: The truck ID.
        """
        return self.__truck_id

    @property
    def truck_name(self):
        """
        Gets the name of the truck.

        Returns:
            str: The name of the truck.
        """
        return self.__truck_name

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

    def insert_filtered_packages(self, packages):
        """
        Insert a list of packages into the list of filtered packages.
        """
        self.filtered_packages.extend(packages)

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

    def reset_distance(self):
        """
        Reset the distance list.

        This function sets the `distances` attribute of the object to an empty list.

        Parameters:
        - None

        Returns:
        - None
        """
        self.distances = []

    # Print all-packages list for Trucks object, useful to see what packages are loaded on
    # the trucks that are ordered by priority of deadline to delivery
    def print_packages(self):
        """
        Print the packages in the `self.packages` list.
        """
        for package in self.packages:
            print(package)

    def print_filtered_packages(self):
        """
        Print the filtered packages in the `self.filtered_packages` list during delivery.
        """
        for package in self.filtered_packages:
            print(package)

    def get_filtered_packages(self):
        """
        Get the filtered packages.
        """
        return self.filtered_packages

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
        Get the number of packages in the truck.

        Returns:
            int: The number of packages in the current instance.
        """
        return len(self.packages)


# Forty packages, 9 + 16 + 15 respectively? for trucks, maximum number of packages to load
# Start hub = '4001 South 700 East', load all trucks at hub
# priority_queue to pop off packages on trucks until empty?
# Once the first truck is empty driver returns to the hub to get the next truck for deliveries
def load_trucks(truck_high_priority, truck_medium_priority, truck_low_priority, graph, track_package_id):
    """
    Load trucks with packages using the nearest neighbor algorithm.

    Parameters:
        truck_high_priority (Truck): The high-priority truck to load packages onto.
        truck_medium_priority (Truck): The medium-priority truck to load packages onto.
        truck_low_priority (Truck): The low-priority truck to load packages onto.
        graph (Graph): The graph representing the delivery network.
        track_package_id (int): The ID of the package to track.

    Returns:
        None
    """

    # Load packages onto trucks using the nearest neighbor algorithm
    trucks = [truck_high_priority, truck_medium_priority, truck_low_priority]
    algo.load_packages_nearest_neighbor(trucks, graph, track_package_id)

    # After loading packages to satisfy constraints,
    # Combine the left-over packages from all three priority levels
    left_over1.append(util.get_left_over_packages(ds.graph_access, util.track_package_id1))
    # Load left-over packages onto non-full trucks
    util.load_left_over_packages(high_priority, left_over1, util.track_package_id1)
    util.load_left_over_packages(medium_priority, left_over1, util.track_package_id1)
    util.load_left_over_packages(low_priority, left_over1, util.track_package_id1)
    for truck in trucks:
        truck.visualize.populate_address(truck.truck_id, truck.route)


# Calculate the shortest route to deliver packages to destination
# and back to hub after applying Dijkstra's algorithm
def _find_shortest_route_to_deliver(truck, graph):
    """
    Find the shortest route for a truck to deliver packages.

    Parameters:
        truck (Truck): The truck object representing the delivery truck.
        graph (Graph): The graph object representing the delivery network.

    Returns:
        int: The total distance traveled by the truck to deliver all the packages.
    """
    # Make a copy of the packages on the truck
    packages_copy = truck.get_packages().copy()
    # Starting location for all trucks, i.e., the hub
    start_vertex1 = truck.route[0]
    # Initialize total_distance traveled by truck to 0
    total_distance = 0
    # Calculate the shortest distances and pred_vertex using Dijkstra's algorithm of the truck's route
    distances1, pred_vertex1 = algo.dijkstra(graph, start_vertex1, truck.route)
    # Use a for loop to iterate over the packages
    for package in packages_copy:
        # Vertex to travel to
        dest_vertex = package.address

        # Insert the calculated distances and pred_vertex into the Trucks object
        truck.insert_distances_pred_vertex(distances1[dest_vertex], pred_vertex1[dest_vertex])
        # Update time during delivery
        time_delivered = truck.time_tracker.update_current_truck_time(distances1[dest_vertex])
        # Insert the time_delivered into package
        truck.time_tracker.insert_current_truck_time_to_package(package, time_delivered)
        # Update the time for other packages with the same address
        for other_package, status_info in truck.time_tracker.get_package_status.items():
            if (other_package != package and other_package.address == package.address and status_info['status'] !=
                    'DELIVERED'):
                truck.time_tracker.insert_current_truck_time_to_package(other_package, time_delivered)
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
    # Flag to track if truck 1's delivery is completed
    is_delivery_completed = False
    distances = {}
    for current_truck in trucks:
        distances[current_truck.truck_id] = 0
        # Current truck time tracker high_priority, medium_priority, low_priority
        time_tracker = current_truck.time_tracker
        # Reset filtered packages for the current truck for each run of the function
        current_truck.filtered_packages = []
        # Reset time for the current truck for each run of the function
        time_tracker.reset_truck_current_time(current_truck.truck_id)
        # Reset distance for the current truck for each run of the function
        current_truck.reset_distance()
        # Reset miles traveled for the current truck for each run of the function
        time_tracker.track_miles_traveled[current_truck.truck_id] = 0
        # Get the name of the current truck
        truck_name = current_truck.truck_name
        # print("NEW LINE---\n")
        # Check if the current truck is ready for delivery
        if current_truck.time_tracker.is_ready_to_deliver(current_truck):
            # # Only print the route if the current truck is truck1 or truck2
            # if current_truck == high_priority or current_truck == medium_priority:
            #     print(f"{truck.get_truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", current_truck.route())
            # Only deliver packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                # Call the function two_opt_route to find the optimized route for the current truck
                algo.two_opt_route(current_truck, graph)
                # Call the function to find the shortest route to deliver packages
                total_distance = _find_shortest_route_to_deliver(current_truck, graph)
                # Update miles traveled for the current truck
                time_tracker.update_miles_traveled(total_distance)
                # Update fuel level for the current truck
                current_truck.fuel_tracker.update_fuel_level(current_truck.truck_id, current_truck.time_tracker)

            # Check if truck 1 has completed its delivery
            if current_truck == high_priority and current_truck.time_tracker.is_delivery_completed():
                is_delivery_completed = True

            if current_truck == low_priority:
                if is_delivery_completed and current_truck.time_tracker.is_ready_to_deliver(current_truck):
                    deliver_truck3_packages(current_truck, graph, start_interval, end_interval)
            # Only filter packages if the current truck is truck1 or truck2
            if current_truck == high_priority or current_truck == medium_priority:
                filtered_packages = current_truck.time_tracker.get_filtered_packages_by_time_range(start_interval,
                                                                                                   end_interval)
                current_truck.insert_filtered_packages(filtered_packages)
                print("Start time:", start_interval, "End time:", end_interval)
                print('Truck:', truck_name)
                print(f"Packages on truck {current_truck.truck_id}:", len(current_truck.filtered_packages))
                current_truck.print_filtered_packages()
                print("TRUCK ROUTE TRAVELED FROM HUB:", current_truck.route)
                distances[current_truck.truck_id] = sum(current_truck.get_distances())
                print(f'Total Distance Travelled: {distances[current_truck.truck_id]} \n')


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
    distances = 0
    truck_name = truck3.truck_name
    time_tracker = truck3.time_tracker
    # Calculate start time for truck 3 based on truck 1's return time
    current_time_truck1 = high_priority.time_tracker.get_current_truck_time()
    truck3_start_time = current_time_truck1

    # Update truck 3's time to account for delivering packages after truck1
    # and update time_to_start_delivery
    time_tracker.set_track_truck_current_time(truck3_start_time)
    time_tracker.update_time_to_start_delivery(truck3_start_time)

    # print(f"{truck.get_truck_name}, OPTIMIZED_DELIVERY_ROUTE: ", truck3.route)
    # Call the function two_opt_route to find the optimized route for truck 3
    algo.two_opt_route(truck3, graph)
    # Call the function to find the shortest route to deliver packages
    total_distance = _find_shortest_route_to_deliver(truck3, graph)
    # Update miles traveled for the current truck
    time_tracker.update_miles_traveled(total_distance)
    # Update fuel level for the current truck
    truck3.fuel_tracker.update_fuel_level(truck3.truck_id, truck3.time_tracker)

    # Check if the time is over 10: 20 AM
    # If so, update the package with ID 9 to the new address
    package_to_update = ds.package_hashmap.get_value_from_key(9)  # Get the package object
    new_address = '410 S State St'
    new_city = 'Salt Lake City'
    new_state = 'UT'
    new_zipcode = '84111'
    new_special_notes = 'Address updated from 300 State St to 410 S State St'
    time_tracker.update_package_status(package_to_update, new_address, new_city, new_state, new_zipcode,
                                       new_special_notes, end_interval)
    filtered_packages = truck3.time_tracker.get_filtered_packages_by_time_range(start_interval, end_interval)
    truck3.insert_filtered_packages(filtered_packages)
    print("Start time:", start_interval, "End time:", end_interval)
    print('Truck:', truck_name)
    print(f"Packages on truck {truck3.truck_id}:", len(truck3.filtered_packages))
    truck3.print_filtered_packages()
    print("TRUCK ROUTE TRAVELED FROM HUB:", truck3.route)
    distances += sum(truck3.get_distances())
    print(f'Total Distance Travelled: {distances} miles \n')


def print_all_package_status_delivery(truck_list, start_interval, end_interval):
    all_packages = []
    distances = 0
    for truck in truck_list:
        all_packages.extend(truck.get_filtered_packages())
        distances += sum(truck.get_distances())
    print("Start time:", start_interval, "End time:", end_interval)
    print('Total Number of Packages:', len(all_packages))
    print('All Packages:', all_packages)
    print(f'Total Distance Travelled: {distances} miles \n')


# Delivered by 9:00am, the constraint of having multiple packages on the same truck delivered together, Truck 1
high_priority = Trucks(truck_id=1, truck_name="HIGH_PRIORITY")
# Delivered by 10:30am, the constraint of having multiple packages required on, Truck 2
medium_priority = Trucks(truck_id=2, truck_name="MEDIUM_PRIORITY")
# Delivered by EOD, no constraints required for packages EOD will be defined as 5:00pm, Truck 3
low_priority = Trucks(truck_id=3, truck_name="LOW_PRIORITY")

# Load trucks
load_trucks(high_priority, medium_priority, low_priority, ds.graph_access, util.track_package_id1)

# Initialize packages
high_priority.time_tracker.initialize_multiple_package_status(high_priority.get_packages(), 'AT_HUB')
# Converted to '9:05 AM'
medium_priority.time_tracker.initialize_multiple_package_status(medium_priority.get_packages(), 'AT_HUB')

# Placeholder for packages that will be delivered by truck 3, Truck 3 will have new time_to_start_delivery
# and current_time attributes to reflect the time it will start delivering packages
low_priority.time_tracker.initialize_multiple_package_status(low_priority.get_packages(), 'AT_HUB')

# trucks_list = [high_priority, medium_priority, low_priority]
# deliver_packages(trucks_list, ds.graph_access, '8:00 AM', '5:00 PM')
# print_all_package_status_delivery(trucks_list, '8:00 AM', '5:00 PM')
# high_priority.visualize.visualize_truck_route(high_priority.truck_id, high_priority.truck_name)
