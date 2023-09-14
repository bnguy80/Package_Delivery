# Student ID: 003964281

from package_delivery.delivery import trucks
from package_delivery.timeutil.time_util import validate_time_format
from package_delivery.delivery.trucks import high_priority, medium_priority, low_priority
from package_delivery import datastructures as ds

trucks_list = [high_priority, medium_priority, low_priority]
has_packages_loaded = False


def load_packages_submenu():
    global has_packages_loaded
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Load Trucks with Packages?\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            has_packages_loaded = True
            print("Truck1, Number of packages: ", high_priority.get_package_count())
            high_priority.print_packages()
            print("\n")
            print("Truck2, Number of packages: ", medium_priority.get_package_count())
            medium_priority.print_packages()
            print("\n")
            print("Truck3, Number of packages: ", low_priority.get_package_count())
            low_priority.print_packages()
            break


def delivery_submenu():
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Begin Delivery and View Package Status\n"
            "[2] Check Status of a Specific Package During Delivery\n"
            "[3] Review Final Package Delivery Status\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        if sub_menu == "1":
            start_interval = input("Enter start interval (e.g., '8:35 AM', '9:35 AM', '12:03 PM'): ")
            end_interval = input("Enter end interval (e.g., '9:25 AM', '10:25 AM', '1:12 PM'): ")
            if not validate_time_format(start_interval) or not validate_time_format(
                    end_interval):
                continue
            while True:
                print('Start Interval:', start_interval, 'End Interval:', end_interval)
                trucks.deliver_packages(trucks_list, ds.graph_access, start_interval, end_interval)
                trucks.print_truck_delivery_status(trucks_list, start_interval, end_interval)
                trucks.print_all_package_status_delivery(trucks_list, start_interval, end_interval)
                # Reset truck distances after printing when continue_delivery is True
                for truck in trucks_list:
                    truck.distances = []
                continue_delivery = input("Continue delivery? (Y/N): ")
                if continue_delivery.upper() == "Y":
                    start_interval = input("Enter start interval (e.g., '8:35 AM', '9:35 AM', '12:03 PM'): ")
                    end_interval = input("Enter end interval (e.g., '9:25 AM', '10:25 AM', '1:12 PM'): ")
                    if not validate_time_format(start_interval) or not validate_time_format(
                            end_interval):
                        continue
                else:
                    break
        if sub_menu == "2":
            while True:
                print("Select Truck ID(1-3) or type 'exit' to leave:")
                truck_choice = input()

                if truck_choice == 'exit':
                    break

                if truck_choice.isdigit() and 1 <= int(truck_choice) <= 3:
                    selected_truck = None
                    for truck in trucks_list:
                        if truck.truck_id == int(truck_choice):
                            selected_truck = truck
                            break

                    if selected_truck:
                        print(f"Selected Truck {selected_truck.truck_id}")

                        while True:
                            print("Package IDs on the truck:")
                            for package in selected_truck.get_packages():
                                print(f"Package ID: {package.package_id}")

                            package_id = int(input("Enter package ID or '0' to select another truck: "))
                            if package_id == 0:
                                break

                            current_time = input("Enter current time (e.g., '8:35 AM', '9:35 AM', '12:03 PM'): ")
                            while not validate_time_format(current_time):
                                print("Invalid time format. Try again.")
                                current_time = input("Enter current time (e.g., '8:35 AM', '9:35 AM', '12:03 PM'): ")
                            trucks.deliver_packages(trucks_list, ds.graph_access, current_time, current_time)
                            selected_truck.time_tracker.lookup_single_package_status(package_id, current_time)

                            continue_seeing = input("See another package status? (Y/N): ")
                            if continue_seeing.upper() == "N":
                                break
                else:
                    print("Invalid choice. Please select a valid Truck ID.")
        if sub_menu == "3":
            print("Final status of all packages:")
            trucks.deliver_packages(trucks_list, ds.graph_access, "8:00 AM", "5:00 PM")
            trucks.print_truck_delivery_status(trucks_list, "8:00 AM", "5:00 PM")
            start_interval = "8:00 AM"
            end_interval = "5:00 PM"
            trucks.print_all_package_status_delivery(trucks_list, start_interval, end_interval)


def visualize_submenu():
    while True:
        sub_menu = input(
            "[0] Exit\n"
            "[1] Visualize Individual Package Locations\n"
            "[2] Visualize Specific Truck Route\n"
            "[3] Visualize All Truck Routes\n"
        )
        if sub_menu == "0":
            print("Returning to main menu")
            break
        elif sub_menu == "1":
            while True:
                print("Select Truck ID(1-3):")
                truck_choice = int(input())
                if 1 <= truck_choice <= 3:
                    selected_truck = None
                    for truck in trucks_list:
                        if truck.truck_id == truck_choice:
                            selected_truck = truck
                    if selected_truck:
                        print(f"Selected Truck {selected_truck.truck_id}")
                        selected_truck.visualize.visualize_package_locations(selected_truck.truck_id,
                                                                             selected_truck.truck_name)
                        continue_visualizing = input("Continue visualizing? (Y/N): ")
                        if continue_visualizing.upper() == "Y":
                            continue
                        else:
                            break
        elif sub_menu == "2":
            while True:
                print("Select Truck ID(1-3):")
                truck_choice = int(input())
                if 1 <= truck_choice <= 3:
                    selected_truck = None
                    for truck in trucks_list:
                        if truck.truck_id == truck_choice:
                            selected_truck = truck
                    if selected_truck:
                        print(f"Selected Truck {selected_truck.truck_id}")
                        selected_truck.visualize.visualize_truck_route(selected_truck.truck_id,
                                                                       selected_truck.truck_name)
                        continue_visualizing = input("Continue visualizing? (Y/N): ")
                        if continue_visualizing.upper() == "Y":
                            continue
                        else:
                            break
        elif sub_menu == "3":
            high_priority.visualize.visualize_all_truck_routes(trucks_list, high_priority.truck_id)


def ui():
    global has_packages_loaded
    main_menu = input(
        "[0] Exit\n"
        "[1] View All Package Details\n"
        "[2] View Details of a Specific Package (using Package ID) \n"
        "[3] Load Trucks with Packages \n"
        "[4] Run Delivery Simulation \n"
        "[5] Visualize delivery simulation \n"
    )
    if main_menu == "0":
        print("Exit")
        (SystemExit())

    elif main_menu == "1":
        high_priority.time_tracker.print_all_package_status()
        medium_priority.time_tracker.print_all_package_status()
        low_priority.time_tracker.print_all_package_status()
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
