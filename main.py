from package_delivery.delivery import Trucks
from package_delivery.delivery.Trucks import high_priority, medium_priority, low_priority
from package_delivery.data_structures.AdjacencyMatrix import graph_access
from package_delivery.data_structures import HashMap
from package_delivery.data_structures.HashMap import package_hashmap

trucks_list = [high_priority, medium_priority, low_priority]


def load_packages_submenu():
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Load packages onto trucks\n"
            "[2] Sort packages and optimize route\n"

        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            print("Truck1, Number of packages: ", high_priority.get_package_count())
            high_priority.print_packages()
            print("\n")
            print("Truck2, Number of packages: ", medium_priority.get_package_count())
            medium_priority.print_packages()
            print("\n")
            print("Truck3, Number of packages: ", low_priority.get_package_count())
            # low_priority.print_packages()
            # # Initialize all packages loaded onto trucks status to 'AT_HUB'
            # high_packages = high_priority.get_packages()
            # medium_packages = medium_priority.get_packages()
            # low_packages = low_priority.get_packages()
            # high_priority.time_tracker.initialize_multiple_package_status(high_packages, 'AT_HUB', 1, 8.0)
            # medium_priority.time_tracker.initialize_multiple_package_status(medium_packages, 'AT_HUB', 2, 9.05)
            # low_priority.time_tracker.initialize_multiple_package_status(low_packages, 'AT_HUB', 3, 8.0)
            # # Initialize tracking of trucks and packages
            # high_priority.time_tracker.insert_current_truck(high_priority.truck_id)
            # medium_priority.time_tracker.insert_current_truck(medium_priority.truck_id)
            # low_priority.time_tracker.insert_current_truck(low_priority.truck_id)
            print("\n")
        elif sub_menu == "2":
            # Trucks.sort_packages_on_truck(high_priority, graph_access)
            # Trucks.sort_packages_on_truck(medium_priority, graph_access)
            # Trucks.sort_packages_on_truck(low_priority, graph_access)
            # Trucks.two_opt_route(high_priority, graph_access)
            # Trucks.two_opt_route(medium_priority, graph_access)
            # Trucks.two_opt_route(low_priority, graph_access)
            print("Truck1, optimized route:", high_priority.route)
            high_priority.time_tracker.print_package_status()
            print("Truck2, optimized route:", medium_priority.route)
            medium_priority.time_tracker.print_package_status()
            print("Truck3, optimized route:", low_priority.route)
            low_priority.time_tracker.print_package_status()
            break


def delivery_submenu():

    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Start delivery and see status\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        if sub_menu == "1":
            start_interval = input("Enter start interval (e.g., '9:35'): ")
            end_interval = input("Enter end interval (e.g., '10:25'): ")
            Trucks.deliver_packages(trucks_list, graph_access, start_interval, end_interval)



def ui():
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
        delivery_submenu()
        ui()


print("Welcome to Package Delivery System")
ui()
