from package_delivery.data_structures import HashMap
from package_delivery.delivery import Trucks
from package_delivery.delivery.Tracking import TimeTracker
from package_delivery.delivery.Trucks import high_priority, medium_priority, low_priority
from package_delivery.data_structures.Graph import graph_access

from package_delivery.data_structures.HashMap import package_hashmap

trucks_list = [high_priority, medium_priority, low_priority]
packages_loaded = False


def load_packages_submenu():
    global packages_loaded
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Load packages onto trucks?\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            packages_loaded = True
            print("Truck1, optimized route:", high_priority.route)
            high_priority.time_tracker.print_all_package_status()
            print("Truck1, Number of packages: ", high_priority.get_package_count())
            high_priority.print_packages()
            print("\n")
            print("Truck2, optimized route:", medium_priority.route)
            medium_priority.time_tracker.print_all_package_status()
            print("Truck2, Number of packages: ", medium_priority.get_package_count())
            medium_priority.print_packages()
            print("\n")
            print("Truck3, optimized route:", low_priority.route)
            low_priority.time_tracker.print_all_package_status()
            print("Truck3, Number of packages: ", low_priority.get_package_count())
            low_priority.print_packages()
            break


def delivery_submenu():
    started_delivery = False
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Start delivery and see status?\n"
            "[2] See single package status during delivery?\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        if sub_menu == "1":
            started_delivery = True
            start_interval = input("Enter start interval (e.g., '8:25', '9:35', '12:03'): ")
            end_interval = input("Enter end interval (e.g., '9:25', '10:25', '1:12'): ")
            if not TimeTracker.validate_time_format(start_interval) or not TimeTracker.validate_time_format(
                    end_interval):
                continue
            while True:
                Trucks.deliver_packages(trucks_list, graph_access, start_interval, end_interval)
                continue_delivery = input("Continue delivery? (Y/N): ")
                if continue_delivery.upper() == "Y":
                    start_interval = input("Enter start interval (e.g., '8:25', '9:35', '12:03'): ")
                    end_interval = input("Enter end interval (e.g., '9:25', '10:25', '1:12'): ")
                    if not TimeTracker.validate_time_format(start_interval) or not TimeTracker.validate_time_format(
                            end_interval):
                        continue
                else:
                    break
        if sub_menu == "2":
            if not started_delivery:
                print("Start delivery first!")
                ui()
            print("Select Truck ID(1-3):")
            truck_choice = int(input())

            if 1 <= truck_choice <= 3:
                selected_truck = None
                for truck in trucks_list:
                    if truck.truck_id == truck_choice:
                        selected_truck = truck
                        break
                if selected_truck:
                    print(f"Selected Truck {selected_truck.truck_id}")
                    print("Package IDs on the truck:")
                    for package in selected_truck.get_packages():
                        print(f"Package ID: {package.package_id}")
                    package_id = int(input("Enter package ID: "))
                    while True:
                        current_time = input("Enter current time (e.g., '8:25', '9:35', '12:03'): ")
                        if not TimeTracker.validate_time_format(current_time):
                            continue
                        selected_truck.time_tracker.lookup_package_status(package_id, current_time)
                        continue_seeing = input("Continue seeing status with different time? (Y/N): ")
                        if continue_seeing.upper() == "Y":
                            current_time = input("Enter current time (e.g., '8:25', '9:35', '12:03'): ")
                            if not TimeTracker.validate_time_format(current_time):
                                continue
                            selected_truck.time_tracker.lookup_package_status(package_id, current_time)
                        else:
                            break
            else:
                print("Invalid Truck ID")


def ui():
    global packages_loaded
    main_menu = input(
        "[0] Exit\n"
        "[1] See all packages\n"
        "[2] See single package from package_ID \n"
        "[3] Load packages onto trucks \n"
        "[4] Start delivery \n"
    )
    if main_menu == "0":
        print("Exit")
        (SystemExit())

    if main_menu == "1":
        print("PACKAGES:\n")
        package_hashmap.print_get_all_packages()
        value = HashMap.check_all_packages(package_hashmap)
        print("CHECK IF ALL 40 PACKAGES EXIST:", value)
        ui()
    if main_menu == "2":
        find = "Y"
        while find == "Y":
            try:
                id_input = input("Enter package_id: ")
                id_input_int = int(id_input)
                print(package_hashmap.get_value_from_key(id_input_int))
            except ValueError:
                print("Please enter valid package_id")
            find_again = input("Enter Y to keep searching: ")
            find_again_upper = find_again.upper()
            while find_again_upper not in ["Y", "N"]:
                print("Please enter either Y or N")
                find_again = input("Enter Y to keep searching: ")
                find_again_upper = find_again.upper()
            find = find_again_upper
        ui()
    if main_menu == "3":
        load_packages_submenu()
        ui()

    if main_menu == "4":
        if not packages_loaded:
            print("Packages must be loaded onto trucks first!")
            ui()
        delivery_submenu()
        ui()


print("ID:003964281")
print("Welcome to Package Delivery System, please select an option: ")
ui()
