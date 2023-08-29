from package_delivery.delivery import trucks
from package_delivery.trackingutil.tracking_util import validate_time_format
from package_delivery.delivery.trucks import high_priority, medium_priority, low_priority
from package_delivery import datastructures as ds
from package_delivery.visualization.visualize import Visualize

trucks_list = [high_priority, medium_priority, low_priority]
has_packages_loaded = False


def load_packages_submenu():
    global has_packages_loaded
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Load packages onto trucks?\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            has_packages_loaded = True
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
    has_started_delivery = False
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Start delivery and see status?\n"
            "[2] See single package status during delivery?\n"
            "[3] See final status of all packages after delivery?\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        if sub_menu == "1":
            has_started_delivery = True
            start_interval = input("Enter start interval (e.g., '8:25 AM', '9:35 AM', '12:03 AM'): ")
            end_interval = input("Enter end interval (e.g., '9:25 AM', '10:25 AM', '1:12 PM'): ")
            if not validate_time_format(start_interval) or not validate_time_format(
                    end_interval):
                continue
            while True:
                trucks.deliver_packages(trucks_list, ds.graph_access, start_interval, end_interval)
                continue_delivery = input("Continue delivery? (Y/N): ")
                if continue_delivery.upper() == "Y":
                    start_interval = input("Enter start interval (e.g., '8:25 AM', '9:35 AM', '12:03 AM'): ")
                    end_interval = input("Enter end interval (e.g., '9:25 AM', '10:25 AM', '1:12 PM'): ")
                    if not validate_time_format(start_interval) or not validate_time_format(
                            end_interval):
                        continue
                else:
                    break
        if sub_menu == "2":
            if not has_started_delivery:
                print("Start delivery first!")
                ui()
            print("Select Truck ID(1-3):")
            truck_choice = int(input())

            if 1 <= truck_choice <= 3:
                selected_truck = None
                for truck in trucks_list:
                    if truck.get_truck_id() == truck_choice:
                        selected_truck = truck
                        break
                if selected_truck:
                    print(f"Selected Truck {selected_truck.truck_id}")
                    print("Package IDs on the truck:")
                    for package in selected_truck.get_packages():
                        print(f"Package ID: {package.package_id}")
                    package_id = int(input("Enter package ID: "))
                    while True:
                        current_time = input("Enter current time (e.g., '8:25 AM', '9:35 AM', '12:03 PM'): ")
                        if not validate_time_format(current_time):
                            continue
                        selected_truck.time_tracker.lookup_single_package_status(package_id, current_time)
                        continue_seeing = input("Continue seeing status with different time? (Y/N): ")
                        if continue_seeing.upper() == "Y":
                            current_time = input("Enter current time (e.g., '8:25 AM', '9:35 AM', '12:03 PM'): ")
                            if not validate_time_format(current_time):
                                continue
                            selected_truck.time_tracker.lookup_single_package_status(package_id, current_time)
                        else:
                            break
            else:
                print("Invalid Truck ID")
        if sub_menu == "3":
            if not has_started_delivery:
                print("Start delivery first!")
                ui()
            print("Final status of all packages:")
            trucks.deliver_packages(trucks_list, ds.graph_access, "8:00 AM", "5:00 PM")
            total_miles = 0
            for truck in trucks_list:
                total_miles += truck.time_tracker.calculate_total_miles_traveled()
            print(f"Total miles traveled: {total_miles}")


def visualize_submenu():
    is_address_added = False
    vis = Visualize()
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Add address\n"
            "[2] Visualize individual package locations\n"
            "[3] Visualize truck routes\n"
            "[4] Visualize all truck routes\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            while True:
                print("Truck1, optimized route:", high_priority.route)
                print("Truck2, optimized route:", medium_priority.route)
                print("Truck3, optimized route:", low_priority.route)
                add_route_coordinates = input("Enter address to add: ")
                vis.add_route_coord(add_route_coordinates)
                continue_adding = input("Continue adding address? (Y/N): ")
                if continue_adding.upper() == "N":
                    break
            is_address_added = True
        elif sub_menu == "2":
            if not is_address_added:
                print("Add address first!")
                continue
            vis.visualize_package_locations()
        elif sub_menu == "3":
            print("Select Truck ID(1-3):")
            truck_choice = int(input())
            if 1 <= truck_choice <= 3:
                vis.get_singe_truck_route(truck_choice)
                vis.visualize_truck_routes()
            else:
                print("Invalid Truck ID")
        elif sub_menu == "4":
            vis.visualize_all_truck_routes(trucks_list)
        else:
            print("Invalid option, please try again")


def ui():
    global has_packages_loaded
    main_menu = input(
        "[0] Exit\n"
        "[1] See all packages\n"
        "[2] See single package from package_ID \n"
        "[3] Load packages onto trucks \n"
        "[4] Start delivery \n"
        "[5] Visualize delivery route \n"
    )
    if main_menu == "0":
        print("Exit")
        (SystemExit())

    elif main_menu == "1":
        print("PACKAGES:\n")
        ds.package_hashmap.print_get_all_packages()
        value = ds.package_hashmap.check_all_packages()
        print("CHECK IF ALL 40 PACKAGES EXIST:", value)
        ui()
    elif main_menu == "2":
        find = "Y"
        while find == "Y":
            try:
                id_input = input("Enter package_id: ")
                id_input_int = int(id_input)
                print(ds.package_hashmap.get_value_from_key(id_input_int))
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
    elif main_menu == "3":
        load_packages_submenu()
        ui()

    elif main_menu == "4":
        if not has_packages_loaded:
            print("Packages must be loaded onto trucks first!")
            ui()
        delivery_submenu()
        ui()

    elif main_menu == "5":
        visualize_submenu()
        ui()
    else:
        print("Invalid option, please try again")


print("ID:003964281")
print("Welcome to Package Delivery System, please select an option: ")
ui()
