from package_delivery.datastructures.hash_map import HashMapEntry
from package_delivery.trackingutil import tracking_util as util


class TimeTracker:
    """
    Class to track the time for each truck. Componite of Trucks class

    Attributes:
        __TRUCK_SPEED (float): The speed of the truck.
        track_truck_current_time (dict): Dictionary to track current_time for each truck.
        packages_status (dict): Dictionary to track packages_status for each truck.
        track_miles_traveled (dict): Dictionary to track miles traveled for each truck.
    """

    def __init__(self, truck_id):
        """
        Initialize the TimeTracker object

        Parameters:
            truck_id (int): The ID of the truck
        """
        # Trucks_speed 18mph -> 0.3 miles per minute
        self.__TRUCK_SPEED = 0.3
        # Dictionary to track current_time for each truck
        self.track_truck_current_time = {}
        # Dictionary of packages on truck and their status; AT_HUB, IN_TRANSIT, or DELIVERED
        self.packages_status = {}
        # Dictionary to track miles traveled by each truck
        self.track_miles_traveled = {}

        # Initialize miles_traveled for each truck to 0
        self.track_miles_traveled[truck_id] = 0

        # Set the current time for each truck based on its truck ID
        if truck_id == 1:
            self.track_truck_current_time[truck_id] = 8.0  # Set truck 1 start time to string 8:00 AM
        elif truck_id == 2:
            self.track_truck_current_time[truck_id] = 9.083333  # Set truck 2 start time 9:05 AM
        elif truck_id == 3:
            self.track_truck_current_time[truck_id] = 0  # Set truck 3 start time to zero will be updated when start delivery after truck 1

    # Fixed speed of truck to calculate travel time
    def _get_truck_speed(self):
        """
        Get the speed of the truck.
        """
        return self.__TRUCK_SPEED



    # Get the status of all packages
    @property
    def package_status(self):
        """
        Get all package statuses.

        Returns:
            The package status.
        """
        return self.packages_status

    def set_track_truck_current_time(self, truck_id, new_time):
        """
        Sets the current time for a specified truck.

        Parameters:
            truck_id (int): The ID of the truck.
            new_time (datetime): The new current time to set for the truck.

        Raises:
            ValueError: If the current time is not updated.

        Returns:
            None
        """
        if truck_id in self.track_truck_current_time and self.track_truck_current_time[truck_id] != new_time:
            self.track_truck_current_time[truck_id] = new_time
        else:
            raise ValueError("Current time not updated")

    # Lookup single package status by package_id and current_time to determine if package is delivered or in transit
    def lookup_single_package_status(self, package_id, current_time):
        """
        Looks up single the status of a package based on the provided package ID and current time.

        Parameters:
            package_id (int): The ID of the package to look up.
            current_time (str): The current time in the format 'HH:MM'.

        Returns:
            None
        """
        before_load = util.convert_12h_to_24h_datetime('8:00 AM')
        current_time = util.convert_12h_to_24h_datetime(current_time)
        for package, status_info in self.packages_status.items():
            if package.package_id == package_id:
                time_delivered_str = status_info['time_delivered']
                time_delivered = util.convert_time_str_to_datetime(time_delivered_str)
                status_info_copy = status_info.copy()
                if current_time >= time_delivered and current_time >= before_load:
                    status_info_copy['status'] = 'DELIVERED'
                elif time_delivered > current_time >= before_load:
                    status_info_copy['status'] = 'IN_TRANSIT'
                elif current_time < before_load:
                    status_info_copy['status'] = 'AT_HUB'

                print("Package: ", package, " - Package Status: ", status_info_copy['status'],
                      "Package Time Delivered: ", status_info_copy['time_delivered'])
                return

        print("Package not found")

    # Update package in package_status dictionary

    def update_package_status(self, package, new_address, new_city, new_state, new_zipcode, new_special_notes, current_time):
        """
        Updates the status of a package in the package status dictionary.

        Parameters:
        - package (HashMapEntry): The package to update.
        - new_address (str): The new address for the package.
        - new_city (str): The new city for the package.
        - new_state (str): The new state for the package.
        - new_zipcode (str): The new zipcode for the package.
        - new_special_notes (str): The new special notes for the package.

        Returns:
        - bool: True if the package status was successfully updated, False otherwise.
        """

        time = util.convert_12h_to_24h_datetime(current_time)
        target_time = util.convert_12h_to_24h_datetime('9:35 AM')
        if time >= target_time:
            if package in self.packages_status:
                # Get the old status
                old_status = self.packages_status[package]

                # Create the updated package with new information
                updated_package = HashMapEntry(
                    package.package_id,
                    new_address,
                    new_city,
                    new_state,
                    new_zipcode,
                    package.delivery_deadline,
                    package.mass,
                    new_special_notes
                )
                # Remove old package entry
                del self.packages_status[package]
                # Update the package status dictionary
                self.packages_status[updated_package] = old_status

                print("PACKAGE UPDATED, Address updated from 300 State St to 410 S State St: #9")

    # See the status of all packages during the day
    def print_all_package_status(self):
        """
        Print all package statuses.

        This function prints the status of all packages in the `packages_status` dictionary.

        Parameters:
        - self: The current instance of the class.

        Returns:
        - None
        """
        print("Package Status:")
        for package, status in self.packages_status.items():
            print(package, self.packages_status[package])

    # Initialize the package status to 'AT_HUB' after loading all on trucks
    # Associate all packages with their truck they are loaded onto
    def initialize_multiple_package_status(self, packages, initial_status, truck_id, time_loaded):
        """
        Initializes the status of multiple packages.

        Parameters:
            packages (list): A list of packages to initialize the status for.
            initial_status (str): The initial status of the packages.
            truck_id (int): The ID of the truck.
            time_loaded (float): The time when the truck was loaded.

        Returns:
            None
        """
        formatted_time_to_start_delivery = util.float_time_24hr_str(time_loaded)
        for package in packages:
            delivery_deadline = util.convert_12h_to_24h_datetime(package.delivery_deadline)
            formatted_delivery_time = delivery_deadline.strftime('%H:%M')
            if package not in self.packages_status:
                self.packages_status[package] = {
                    'status': initial_status,
                    'truck': truck_id,
                    'time_loaded': time_loaded,  # Keep as float to increment time_delivered
                    'delivery_deadline': formatted_delivery_time,
                    'time_to_start_delivery': formatted_time_to_start_delivery,
                    'time_delivered': None
                }

    # Update the time_to_start_delivery for a specific truck for all packages on that truck
    def update_time_to_start_delivery(self, truck_id, new_time):
        """
        Updates the time to start delivery for all packages assigned to a given truck.

        Parameters:
            truck_id (int): The ID of the truck.
            new_time (float): The new time to start delivery.

        Returns:
            None
        """
        for package_id, package_info in self.packages_status.items():
            if package_info['truck'] == truck_id:
                package_info['time_to_start_delivery'] = util.float_time_24hr_str(new_time)

    def get_single_package_status(self, package):
        return self.packages_status[package]

    # Add time during from one delivery to another to current_time for the current truck
    def increment_current_truck_time(self, time, current_truck):
        """
        Increment the current time of a specific truck.

        Parameters:
            time (float): The amount of time to increment the current time by.
            current_truck (int): The identifier of the truck to update.

        Returns:
            None
        """
        self.track_truck_current_time[current_truck] += time

    # Get the current time for the current truck
    def get_current_truck_time(self, current_truck):
        """
        Retrieves the current time of the specified truck.

        Parameters:
            current_truck (int): The ID of the truck for which to retrieve the current time.

        Returns:
            datetime.datetime: The current time of the specified truck.
        """
        return self.track_truck_current_time[current_truck]

    # Update miles_traveled during delivery for current_truck
    def update_miles_traveled(self, distance, current_truck):
        """
        Update the miles traveled for a specific truck.

        Parameters:
            distance (float): The distance traveled by the truck.
            current_truck (int): The identifier of the current truck.

        Returns:
            None
        """
        miles = 0
        miles += distance
        # Update miles traveled for the current truck
        current_miles_traveled = self.track_miles_traveled[current_truck]
        self.track_miles_traveled[current_truck] = current_miles_traveled + miles

    # Print miles traveled by current truck
    def print_current_truck_miles(self, current_truck):
        """
        Print the number of miles traveled by a specific truck.

        Parameters:
            current_truck (int): The identifier of the truck.

        Returns:
            None
        """
        miles_traveled = self.track_miles_traveled[current_truck]
        print("MILES_TRAVELED: ", miles_traveled, " miles")
        print()

    def calculate_total_miles_traveled(self):
        """
        Calculates the total miles traveled by summing the values in the track_miles_traveled dictionary.

        Parameters:
            self (TimeTracker): The instance of the class.

        Returns:
            float: The total miles traveled.
        """
        return sum(self.track_miles_traveled.values())

    # Calculate the time in minutes: time = distance / speed
    def calculate_travel_time_minutes(self, distance):
        """
        Calculate the travel time in minutes based on the distance and the truck's speed.

        Parameters:
            distance (float): The distance to travel in kilometers.

        Returns:
            float: The travel time in minutes.
        """
        speed = self._get_truck_speed()
        return distance / speed

    # Update current_truck delivery time and insert into delivery_time of package
    def update_current_truck_time(self, distance, current_truck_id):
        """
        Updates the current time of a given truck based on the distance traveled.

        Parameters:
            distance (float): The distance traveled by the truck.
            current_truck_id (int): The ID of the current truck.

        Returns:
            str: The formatted current time of the truck.
        """
        # Calculate travel time for each segment of the route for the current truck
        # Add to current_time
        transit_time = self.calculate_travel_time_minutes(distance)
        transit_time_hours = transit_time / 60  # Convert transit_time from minutes to hours

        self.increment_current_truck_time(transit_time_hours, current_truck_id)
        # Float to string for current_time
        formatted_truck_current_time = util.float_time_24hr_str(self.track_truck_current_time[current_truck_id])
        return formatted_truck_current_time

    def insert_current_truck_time_to_package(self, package, time_delivered):
        """
        Inserts the current truck time to a package.

        Parameters:
            package (any): The package to insert the time for.
            time_delivered (str): The time the package was delivered.

        Returns:
            None
        """

        if package in self.packages_status:
            self.packages_status[package]['time_delivered'] = time_delivered

    # Trucks are ready to deliver packages
    def is_ready_to_deliver(self, current_truck):
        """
        Check if the specified truck is ready to deliver packages.

        Parameters:
            current_truck (Truck): The truck to check if it is ready to deliver.

        Returns:
            bool: True if the truck is ready to deliver, False otherwise.
        """
        for package, status_info in self.packages_status.items():
            if status_info['truck'] == current_truck.truck_id and status_info['status'] == 'AT_HUB':
                return True
        return False

    # Checks if delivery is completed
    def is_delivery_completed(self):
        """
        Checks if the delivery for all packages is completed.

        Returns:
            bool: True if the delivery for all packages is completed, False otherwise.
        """
        max_time_delivered = None
        for status in self.packages_status.values():
            time_delivered = status['time_delivered']
            if time_delivered:
                if max_time_delivered is None or time_delivered > max_time_delivered:
                    max_time_delivered = time_delivered
        return max_time_delivered is not None

    # Dynamically update the status of packages to 'AT_HUB','IN_TRANSIT','DELIVERED' as the truck travels
    # Should not hard-code the package status to 'AT_HUB','IN_TRANSIT' and 'DELIVERED' to avoid errors
    def filter_packages_by_time_range(self, start_interval, end_interval):
        """
        Filter packages by time range.
        """
        filtered_packages = []

        start_time = util.convert_12h_to_24h_datetime(start_interval)
        end_time = util.convert_12h_to_24h_datetime(end_interval)

        if start_time > end_time:
            raise ValueError("Invalid time range")

        for package, status_info in self.packages_status.items():
            time_delivered_str = status_info['time_delivered']
            time_to_start_delivery_str = status_info['time_to_start_delivery']
            try:
                time_delivered = util.convert_time_str_to_datetime(time_delivered_str)
                time_start_delivery = util.convert_time_str_to_datetime(time_to_start_delivery_str)
                if time_start_delivery > start_time and time_start_delivery > end_time:
                    filtered_packages.append([package, status_info])
                elif start_time <= time_delivered <= end_time or time_delivered < start_time:
                    status_info_copy = status_info.copy()
                    status_info_copy['status'] = 'DELIVERED'
                    filtered_packages.append([package, status_info_copy])
                elif time_delivered > end_time > time_start_delivery:
                    status_info_copy1 = status_info.copy()
                    status_info_copy1['status'] = 'IN_TRANSIT'
                    filtered_packages.append([package, status_info_copy1])
            except ValueError as e:
                print(f"Error parsing time for package {package}: {e}, time_delivered: {0}")

        print("FILTERED_PACKAGE COUNT:", len(filtered_packages))
        return filtered_packages
