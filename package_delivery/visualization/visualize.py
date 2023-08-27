import matplotlib.pyplot as plt

from package_delivery.delivery.trucks import high_priority, low_priority, medium_priority


class Visualize:
    def __init__(self):
        self.image_path = None
        self.route = {}
        # All coordinates (x, y) dictionary; visualize a Picture1.jpg dimensions 672x756
        self.ALL_COORDINATES = {
            '4001 South 700 East': (397, 457),
            '195 W Oakland Ave': (309, 316),
            '2530 S 500 E': (372, 320),
            '233 Canyon Rd': (344, 57),
            '380 W 2880 S': (290, 351),
            '410 S State St': (336, 122),
            '3060 Lester St': (171, 369),
            '300 State St': (335, 111),
            '600 E 900 South': (413, 139),
            '2600 Taylorsville Blvd': (110, 593),
            '3575 W Valley Central Station bus Loop': (67, 478),
            '2010 W 500 S': (131, 129),
            '4580 S 2300 E': (550, 517),
            '3148 S 1100 W': (216, 376),
            '1488 4800 S': (184, 547),
            '177 W Price Ave': (310, 424),
            '3595 Main St': (330, 420),
            '6351 South 900 East': (422, 678),
            '5100 South 2700 West': (102, 572),
            '5025 State St': (339, 557),
            '5383 South 900 East #104': (413, 594),
            '1060 Dalton Ave S': (213, 186),
            '2835 Main St': (327, 345),
            '1330 2100 S': (469, 288),
            '3365 S 900 W': (239, 397),
            '2300 Parkway Blvd': (130, 325),
            '4300 S 1300 E': (447, 490)
        }

    def load_image(self, filename):
        """
        Load a visualization from a given file.

        Parameters:
            filename (str): The path to the visualization file.

        Returns:
            None
        """
        self.image_path = filename

    def add_route_coord(self, address):
        """
        Adds a route coordinate to the `route` dictionary.

        Args:
            address (str): The address of the route coordinate.

        Returns:
            None

        Raises:
            None
        """
        if address in self.ALL_COORDINATES:
            self.route[address] = self.ALL_COORDINATES[address]
        else:
            print("Invalid address: ", {address})

    def get_singe_truck_route(self, truck_id):
        """
        Get the route for a single truck.

        Parameters:
            truck_id (int): The ID of the truck.

        Returns:
            None
        """
        truck = None
        if truck_id == 1:
            truck = high_priority
        elif truck_id == 2:
            truck = medium_priority
        elif truck_id == 3:
            truck = low_priority
        if truck is not None:
            print(f"Fetching routes for truck {truck_id}...")  # Debug line
            for route in truck.route:
                print(f"Adding route address: {route}")  # Debug line
                self.add_route_coord(route)
        else:
            print(f"Invalid truck ID: {truck_id}")  # Debug line

    def get_all_trucks_routes(self, trucks_list):
        for truck in trucks_list:
            for route in truck.route:
                self.add_route_coord(route)

    # visualize package locations
    def visualize_package_locations(self):
        """
        Visualize the package locations.

        This function reads a file specified by `self.image_path`
        and displays the visualization using the `imshow` function from the `matplotlib.pyplot` library.
        It then overlays markers on the visualization to represent the package locations.
        The coordinates of the package locations are obtained from the `self.route` dictionary.
        Each package location is represented by a marker with the shape of a circle.

        Parameters:
        - None

        Returns:
        - None
        """
        # Read the file
        image = plt.imread(self.image_path)
        # Create a figure with the original dimensions
        fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        # Display the visualization with SciView
        ax.imshow(image)
        # Overlay markers on the visualization
        for (x, y) in self.route.values():
            ax.scatter(x, y, marker='o', color='red', s=50)  # Adjust marker properties

        # Set axis limits and turn off axes
        ax.set_xlim(0, image.shape[1])
        ax.set_ylim(image.shape[0], 0)
        ax.axis('off')  # Turn off axes
        # Display the visualization with markers using SciView
        plt.show()

        # Clears the route for the next visualization
        self.route = {}

    def visualize_truck_routes(self):
        """
        Visualizes the truck routes on an image.

        The function reads an image from the specified path and displays it using matplotlib. Then it extracts the
        coordinates from the `self.route` dictionary and splits them into x and y coordinates for plotting. If the
        route starts and ends at the same point, it is already closed. Otherwise, it explicitly closes the route. It
        then plots the points and the route on the image using matplotlib. Finally, it sets the x and y limits of the
        plot, turns off the axis, and displays the image.

        Parameters:
        - None

        Returns:
        - None
        """
        image = plt.imread(self.image_path)
        fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        ax.imshow(image)

        # Extract the coordinates from the `self.route` dictionary
        # and split them into x and y coordinates for plotting
        x, y = zip(*self.route.values())

        # If the route starts and ends at the same point, it'll already be closed.
        # But if not, we can close it explicitly.
        if x[0] != x[-1] or y[0] != y[-1]:
            x = x + (x[0],)
            y = y + (y[0],)

        ax.scatter(x, y, marker='o', color='red', s=50)
        ax.plot(x, y, color='blue', linestyle='dashed', linewidth=2)

        ax.set_xlim(0, image.shape[1])
        ax.set_ylim(image.shape[0], 0)
        ax.axis('off')
        plt.show()

        # Clears the route for the next visualization
        self.route = {}

    def visualize_all_truck_routes(self):
        """
        Visualizes all the truck routes; overlay one image.

        Parameters:
        - None

        Returns:
        - None
        """
        image = plt.imread(self.image_path)
        fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        ax.imshow(image)

        x, y = zip(*self.route.values())

        ax.scatter(x, y, marker='o', color='red', s=50)
        ax.plot(x, y, color='blue', linestyle='dashed', linewidth=2)
        ax.axis('off')
        plt.show()


vis = Visualize()
trucks_list1 = [high_priority, medium_priority, low_priority]
vis.load_image('C:/Users/brand/IdeaProjects/Package_Delivery_Program_New/package_delivery/visualization/Picture1.jpg')
vis.get_all_trucks_routes(trucks_list1)
vis.visualize_all_truck_routes()
