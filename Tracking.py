from datetime import datetime, timedelta


class TimeTracker:
    def __init__(self):
        # # Start time at 8:00 AM
        # self.overall_current_time = 8.0
        # End time at 5:00 PM
        self.end_time = 17.0
        # Trucks_speed 18mph -> 0.3 miles per minute
        self.truck_speed = 0.3
        # Dictionary to track current_time for each truck
        self.track_truck_current_time = {}
        # Required time intervals to track status of all packages
        self.tracking_intervals = [
            (8.35, 9.25),
            (9.35, 10.25),
            (12.03, 13.12)
        ]
        # Dictionary of packages on truck and their status; AT_HUB, IN_TRANSIT, or DELIVERED
        self.packages_status = {}
        # Dictionary to track miles traveled by each truck
        self.track_miles_traveled = {}

    # Fixed speed of truck to calculate travel time
    def get_truck_speed(self):
        return self.truck_speed

    def insert_current_truck(self, current_truck):
        # Initialize miles_traveled for current truck to 0
        self.track_miles_traveled[current_truck] = 0
        # Initialize the current time for the current truck to the start time
        self.track_truck_current_time[current_truck] = 8.0

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

    # See status of all packages during day
    def print_package_status(self):
        print("Package Status:")
        for package, status in self.packages_status.items():
            print(f"Package: {package}, Status: {status}")

    # Initialize the package status to 'AT_HUB' after loading all on trucks
    def initialize_multiple_package_status(self, packages, initial_status):
        for package in packages:
            if package not in self.packages_status:
                self.packages_status[package] = initial_status

    # # During delivery update package status
    # def update_package_status(self):
    #     for package, status in self.packages_status.items():
    #         if status == 'IN_TRANSIT':
    #             if self.current_time >= package.delivery_time:
    #                 self.mark_package_delivered(package)

    # Mark a package as in transit
    def mark_package_in_transit(self, package):
        # Get the delivery address of the package
        destination = package.address
        # Check if there are other packages with the same delivery address
        same_address_packages = [
            pkg for pkg in self.packages_status.keys() if pkg.address == destination
        ]

        # Update the status of all packages with the same address to 'DELIVERED'
        for pkg in same_address_packages:
            self.packages_status[pkg] = 'IN_TRANSIT'

    # Mark a package as delivered
    def mark_package_delivered(self, package):
        # Get the delivery address of the package
        destination = package.address
        # Check if there are other packages with the same delivery address
        same_address_packages = [
            pkg for pkg in self.packages_status.keys() if pkg.address == destination
        ]

        # Update the status of all packages with the same address to 'DELIVERED'
        for pkg in same_address_packages:
            self.packages_status[pkg] = 'DELIVERED'

    def get_single_package_status(self, package):
        return self.packages_status[package]

    # def is_end_of_day(self):
    #     return self.overall_current_time >= self.end_time

    # Compare the time while current_truck is delivering packages
    # Update and print status of all packages in the time intervals
    # def is_tracking_time(self):
    #     for start, end in self.tracking_intervals:
    #         start_hour, start_minute = divmod(start, 1)
    #         end_hour, end_minute = divmod(end, 1)
    #         for current_truck, current_time in self.track_truck_current_time.items():
    #             current_hour, current_minute = divmod(self.track_truck_current_time[current_truck], 1)
    #             if (
    #                     start_hour <= current_hour < end_hour or
    #                     (start_hour == current_hour and start_minute <= current_minute) or
    #                     (end_hour == current_hour and current_minute < end_minute)
    #             ):
    #                 # Update package status during tracking intervals
    #                 package_status_updated = False
    #                 for package, status in self.packages_status.items():
    #                     if status == 'AT_HUB' and package.delivery_time <= current_time:
    #                         self.mark_package_delivered(package)
    #                         package_status_updated = True
    #                 if package_status_updated:
    #                     print(f"Truck {current_truck} - Current Time Interval: {start:.2f} - {end:.2f}")
    #                     self.print_package_status()
    #                     print()

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

    # Update current_truck delivery time
    def update_current_truck_time(self, distance, current_truck):
        # Calculate travel time for each segment of the route for the current truck
        # Add to current_time
        transit_time = self.calculate_travel_time_minutes(distance)
        transit_time_hours = transit_time / 60  # Convert transit_time from minutes to hours
        self.increment_current_truck_time(transit_time_hours, current_truck)

    def print_delivery_status(self, current_truck):
        current_time = self.track_truck_current_time[current_truck]
        formatted_current = TimeTracker.format_time(current_time)
        delivered_packages_by_destination = {}
        for package, status in self.packages_status.items():
            if status == 'DELIVERED':
                destination = package.address
                package_id = package.package_id

                if destination not in delivered_packages_by_destination:
                    delivered_packages_by_destination[destination] = [package_id]
                else:
                    delivered_packages_by_destination[destination].append(package_id)

        print("Packages delivered:")
        for destination, package_ids in delivered_packages_by_destination.items():
            print("Destination:", destination, end=" ")
            print("Package IDs:", package_ids)
        print("DELIVERY_TIME:", formatted_current)

    # Calculate the time in minutes: time = distance / speed
    def calculate_travel_time_minutes(self, distance):
        speed = self.get_truck_speed()
        return distance / speed
