# def ui():
#     main_menu = input(
#         "[0] Exit\n"
#         "[1] Get all vertices and associated packages\n"
#         "[2] Get package from package_ID\n"
#     )
#     if main_menu == "0":
#         print("Exit")
#         (SystemExit())
#
#     if main_menu == "1":
#         print("Address:\n")
#         graph.print_graph_packages_asc()
#         ui()
#     if main_menu == "2":
#         find = "Y"
#         while find == "Y":
#             try:
#                 id_input = input("Enter package_id: ")
#                 id_input_int = int(id_input)
#                 print(package_hashmap.get_value_from_key(id_input_int))
#             except ValueError:
#                 print("Please enter valid package_id")
#             find_again = input("Enter Y to keep searching: ")
#             find_again_upper = find_again.upper()
#             while find_again_upper not in ["Y", "N"]:
#                 print("Please enter either Y or N")
#                 find_again = input("Enter Y to keep searching: ")
#                 find_again_upper = find_again.upper()
#             find = find_again_upper
#         ui()


# ui()
