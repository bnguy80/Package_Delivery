from datetime import datetime

from package_delivery.data_structures.HashMap import HashMapEntry


class TimeTracker:
    def __init__(self):
        # # Start time at 8:00 AM
        self.overall_current_time = 8.0
        # End time at 5:00 PM
        self.overall_end_time = 17.0
        # Trucks_speed 18mph -> 0.3 miles per minute
        self.truck_speed = 0.3
        # Dictionary to track current_time for each truck
        self.track_truck_current_time = {}
        # # Required time intervals to track status of all packages
        # self.tracking_intervals = [
        #     (8.35, 9.25),
        #     (9.35, 10.25),
        #     (12.03, 13.12)
        # ]
        # Dictionary of packages on truck and their status; AT_HUB, IN_TRANSIT, or DELIVERED
        self.packages_status = {}
        # Dictionary to track miles traveled by each truck
        self.track_miles_traveled = {}

        # Helper function to convert delivery_time to a comparable format

    @staticmethod
    def convert_to_time(delivery_deadline):
        if delivery_deadline == 'EOD':
            return datetime.strptime('5:00 PM', '%I:%M %p')
        else:
            return datetime.strptime(delivery_deadline, '%I:%M %p')

    # Helper function to format time in 24-hour format
    @staticmethod
    def format_time(time):
        hour, minute = divmod(time, 1)
        minute = round(minute * 60)
        return f"{int(hour):02d}:{int(minute):02d}"

    # def is_end_of_day(self):
    #     return self.overall_current_time >= self.end_time

    # Fixed speed of truck to calculate travel time
    def get_truck_speed(self):
        return self.truck_speed

    def insert_current_truck(self, current_truck):
        # Initialize miles_traveled for current truck to 0
        self.track_miles_traveled[current_truck] = 0
        # Set the current time for the current truck based on its truck ID
        if current_truck == 1:
            self.track_truck_current_time[current_truck] = 8.0  # Set truck 1 start time to string 8:00
        elif current_truck == 2:
            self.track_truck_current_time[current_truck] = 9.083333  # Set truck 2 start time to string 9:05
        elif current_truck == 3:
            self.track_truck_current_time[current_truck] = 0  # Set truck 3 start time to 0

    # Get all the trucks
    def get_all_trucks(self):
        """
        Returns a list of all trucks.
        """
        return list(self.track_truck_current_time.keys())

    def remove_current_truck(self, current_truck):
        del self.track_truck_current_time[current_truck]
        del self.track_miles_traveled[current_truck]

    # Get status of all packages
    def get_all_package_status(self):
        return self.packages_status

    # Update package in package_status dictionary

    def update_package_status(self, package, new_address, new_city, new_state, new_zipcode, new_special_notes):
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

            # Update the package status dictionary
            self.packages_status[updated_package] = old_status

            # Remove the old key if necessary
            if updated_package != package:
                del self.packages_status[package]

            return True
        return False

    # See status of all packages during day
    def print_package_status(self):
        print("Package Status:")
        for package, status in self.packages_status.items():
            print(package, self.packages_status[package])

    # Initialize the package status to 'AT_HUB' after loading all on trucks
    # Associate all packages with their truck they are loaded onto
    def initialize_multiple_package_status(self, packages, initial_status, truck_id, time_loaded):
        for package in packages:
            delivery_deadline = self.convert_to_time(package.delivery_deadline)
            formatted_delivery_time = delivery_deadline.strftime('%H:%M')  # Format to 24-hour format
            if package not in self.packages_status:
                self.packages_status[package] = {
                    'status': initial_status,
                    'truck': truck_id,
                    'time_loaded': time_loaded,
                    'delivery_deadline': formatted_delivery_time,
                    'time_to_start_delivery': time_loaded,
                    'time_delivered': None
                }

    # Method to update the time_to_start_delivery for a specific truck for all packages on that truck
    def update_time_to_start_delivery(self, truck_id, new_time):
        for package_id, package_info in self.packages_status.items():
            if package_info['truck'] == truck_id:
                package_info['time_to_start_delivery'] = self.format_time(new_time)

    def get_truck_id_for_package(self, package):
        package_info = self.packages_status.get(package)
        if package_info:
            return package_info.get('truck')
        return None

    # Mark a package as in transit
    def mark_package_in_transit(self, package):
        # Get the delivery address of the package
        destination = package.address
        # Check if there are other packages with the same delivery address
        same_address_packages = [
            pkg for pkg in self.packages_status.keys() if pkg.address == destination
        ]

        # Update the status of all packages with the same address to 'IN_TRANSIT'
        for pkg in same_address_packages:
            self.packages_status[pkg]['status'] = 'IN_TRANSIT'

    def get_single_package_status(self, package):
        return self.packages_status[package]

    # Add time during from one delivery to another to current_time for the current truck
    def increment_current_truck_time(self, time, current_truck):
        self.track_truck_current_time[current_truck] += time

    # Get the current time for the current truck
    def get_current_truck_time(self, current_truck):
        return self.track_truck_current_time[current_truck]

    # Update miles_traveled during delivery for current_truck
    def update_miles_traveled(self, distance, current_truck):
        miles = 0
        miles += distance
        # Update miles traveled for the current truck
        current_miles_traveled = self.track_miles_traveled[current_truck]
        self.track_miles_traveled[current_truck] = current_miles_traveled + miles

    # Print miles traveled by current truck
    def print_miles_traveled(self, current_truck):
        miles_traveled = self.track_miles_traveled[current_truck]
        print("MILES_TRAVELED: ", miles_traveled, " miles")
        print()

    # Calculate the time in minutes: time = distance / speed
    def calculate_travel_time_minutes(self, distance):
        speed = self.get_truck_speed()
        return distance / speed

    # Update current_truck delivery time and insert into delivery_time of package
    def update_current_truck_time(self, distance, current_truck_id):
        # Calculate travel time for each segment of the route for the current truck
        # Add to current_time
        transit_time = self.calculate_travel_time_minutes(distance)
        transit_time_hours = transit_time / 60  # Convert transit_time from minutes to hours

        self.increment_current_truck_time(transit_time_hours, current_truck_id)
        # Float to string for current_time
        formatted_truck_current_time = self.format_time(self.track_truck_current_time[current_truck_id])
        return formatted_truck_current_time

    def insert_current_truck_time_to_package(self, package, time_delivered):

        if package in self.packages_status:
            self.packages_status[package]['time_delivered'] = time_delivered

    # Trucks are ready to deliver packages
    def is_ready_to_deliver(self, current_truck):
        for package, status_info in self.packages_status.items():
            if status_info['truck'] == current_truck.truck_id and status_info['status'] == 'AT_HUB':
                return True
        return False

    # Checks if delivery is completed
    def is_delivery_completed(self):
        max_time_delivered = None
        for status in self.packages_status.values():
            time_delivered = status['time_delivered']
            if time_delivered:
                if max_time_delivered is None or time_delivered > max_time_delivered:
                    max_time_delivered = time_delivered
        return max_time_delivered is not None

    # Initialize package_status of a package to 'IN_TRANSIT' if time_delivered is has not changed
    # from the time_loaded of the package
    def initialize_status_to_in_transit(self, truck_id):
        address_packages = {}
        for package, status_info in self.packages_status.items():
            if status_info['status'] == 'AT_HUB' and status_info['truck'] == truck_id and status_info[
                'time_delivered'] is None:
                status_info['status'] = 'IN_TRANSIT'
                status_info['time_delivered'] = self.format_time(self.track_truck_current_time[truck_id])

                address = package.address
                package_id = package.package_id
                if address not in address_packages:
                    address_packages[address] = [package_id]
                else:
                    address_packages[address].append(package_id)

        for address, package_ids in address_packages.items():
            package_ids_str = ", ".join(str(id) for id in package_ids)
            print(
                f"Package IDs: [{package_ids_str}] - Address: {address} - Status: IN_TRANSIT - Truck: {truck_id}, "
                f"Time_Delivered NOT UPDATED YET: {self.format_time(self.track_truck_current_time[truck_id])}")

    # Update package_status of all packages to 'DELIVERED' after they are delivered
    def update_delivered_delivery(self, truck_id):
        for package, status_info in self.packages_status.items():
            if status_info['status'] == 'IN_TRANSIT' and status_info['truck'] == truck_id:
                status_info['status'] = 'DELIVERED'
                print(
                    f"Package ID: {package.package_id} - Package Address: {package.address} - Status: "
                    f"{status_info}")

    # Print package_status of all packages to 'DELIVERED' after they are delivered
    def print_delivered_status(self, truck_id):
        current_time = self.track_truck_current_time[truck_id]
        formatted_current = TimeTracker.format_time(current_time)
        delivered_packages_by_destination = {}
        for status in self.packages_status.values():
            if status == 'DELIVERED' and status['truck'] == truck_id:
                destination = status.package.address
                package_id = status.package.package_id

                if destination not in delivered_packages_by_destination:
                    delivered_packages_by_destination[destination] = [package_id]
                else:
                    delivered_packages_by_destination[destination].append(package_id)

        print("Packages delivered:")
        for destination, package_ids in delivered_packages_by_destination.items():
            print("Destination:", destination, end=" ")
            print("Package IDs:", package_ids)
        print("DELIVERY_TIME:", formatted_current)

    # Dynamically update status of packages to 'IN_TRANSIT' and 'DELIVERED' as the truck travels
    def filter_packages_by_time_range(self, start_interval, end_interval, ):
        filtered_packages = {}
        packages_to_update = []

        start_time = datetime.strptime(start_interval, '%H:%M').time()
        end_time = datetime.strptime(end_interval, '%H:%M').time()

        for package, status_info in self.packages_status.items():
            time_delivered_str = status_info['time_delivered']
            if time_delivered_str:
                time_delivered = datetime.strptime(time_delivered_str, '%H:%M').time()
                if start_time <= time_delivered <= end_time or time_delivered < start_time:
                    # status_info['status'] = 'DELIVERED'
                    packages_to_update.append(package)
                    filtered_packages[package.package_id] = status_info
                elif time_delivered > end_time:
                    # status_info['status'] = 'IN_TRANSIT'
                    packages_to_update.append(package)
                    filtered_packages[package] = status_info

        # Update the status of the packages outside of the loop
        for package in packages_to_update:
            status_info = self.packages_status[package]
            time_delivered_str = status_info['time_delivered']
            time_delivered = datetime.strptime(time_delivered_str, '%H:%M').time()
            if start_time <= time_delivered <= end_time or time_delivered < start_time:
                status_info['status'] = 'DELIVERED'
                filtered_packages[package.package_id] = status_info
            elif time_delivered > end_time:
                status_info['status'] = 'IN_TRANSIT'
                filtered_packages[package.package_id] = status_info
        print("FILTERED_PACKAGE COUNT:", len(filtered_packages))
        return filtered_packages
