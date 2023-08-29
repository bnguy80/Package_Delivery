import matplotlib.pyplot as plt


class Visualize:
    def __init__(self):
        self.__IMAGE_PATH = ('C:/Users/brand/IdeaProjects/Package_Delivery_Program_New/package_delivery/visualization'
                             '/Picture1.jpg')
        self.route = {}
        # All coordinates (x, y) dictionary; visualize a Picture1.jpg dimensions 672x756
        self.__ALL_COORDINATES = {
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
        if address in self.__ALL_COORDINATES:
            self.route[address] = self.__ALL_COORDINATES[address]
        else:
            print("Invalid address: ", {address})

    def _get_coord_and_close_route(self):
        """
        Get the coordinates and close the route.

        Returns:
            Tuple: The x and y coordinates of the route.
        """
        x, y = zip(*self.route.values())
        # Close the route by adding the first and last coordinates
        if x[0] != x[-1] or y[0] != y[-1]:
            x = x + (x[0],)
            y = y + (y[0],)
        return x, y

    def get_singe_truck_route(self, truck):
        if truck is not None:
            print(f"Fetching routes for truck {truck.get_truck_id}...")  # Debug line
            for route in truck.route:
                print(f"Adding route address: {route}")  # Debug line
                self.add_route_coord(route)
        else:
            print(f"Invalid truck: {truck}")  # Debug line

    # Visualize package locations
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
        image = plt.imread(self.__IMAGE_PATH)
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
        image = plt.imread(self.__IMAGE_PATH)
        fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        ax.imshow(image)

        x, y = self._get_coord_and_close_route()

        ax.scatter(x, y, marker='o', color='red', s=50)
        ax.plot(x, y, color='blue', linestyle='dashed', linewidth=2)

        ax.set_xlim(0, image.shape[1])
        ax.set_ylim(image.shape[0], 0)
        ax.axis('off')
        plt.show()

        # Clears the route for the next visualization
        self.route = {}

    def visualize_all_truck_routes(self, trucks_list):
        image = plt.imread(self.__IMAGE_PATH)
        fig, ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        ax.imshow(image)

        colors = ['red', 'blue', 'green']
        for idx, truck in enumerate(trucks_list):
            # Reset the route for each truck
            self.route = {}
            for route in truck.route:
                self.add_route_coord(route)

            x, y = self._get_coord_and_close_route()

            ax.scatter(x, y, marker='o', color=colors[idx], s=50, label=truck.get_truck_id)
            ax.plot(x, y, color=colors[idx], linestyle='dashed', linewidth=2)
        ax.legend(loc='upper right', shadow=True)
        ax.axis('off')
        plt.show()

    @staticmethod
    def visualize_pie_chart(filtered_packages, truck_title, start_interval, end_interval):
        # Status count of packages
        status_count = {'IN_TRANSIT': 0, 'AT_HUB': 0, 'DELIVERED': 0}
        for package, status_info in filtered_packages:
            current_status = status_info['status']
            if current_status in status_count:
                status_count[current_status] += 1

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = list(status_count.keys())
        sizes = list(status_count.values())
        colors = ['gold', 'red', 'green']
        explode = (0.1, 0.1, 0.1)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.title(f'{truck_title} Package Status Distribution, {start_interval} - {end_interval}')
        plt.show()
