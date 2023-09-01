import matplotlib.pyplot as plt


class Visualize:
    COLORS = ['red', 'blue', 'green']  # High Priority, Medium Priority, Low Priority
    LINE_STYLES = ['-', '--', ':']  # Solid, Dashed, Dotted line styles
    MARKERS = ['o', 's', '^']  # Circle, Square, Triangle markers

    def __init__(self, addresses, truck_id, truck_name):
        """
        Initialize the Visualize object
        """
        self.__IMAGE_PATH = ('C:/Users/brand/IdeaProjects/Package_Delivery_Program_New/package_delivery/visualization'
                             '/Picture1.jpg')
        self.route = {}
        self.addresses = addresses
        self.truck_id = truck_id
        self.truck_name = truck_name
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
        # Create a figure and axes
        self.fig, self.ax = None, None
        # Create a scatter plot
        self.scatter = None
        # Create a line plot
        self.line = None

    def _setup_figure(self):
        idx = (self.truck_id - 1) % 3
        # Read the image
        image = plt.imread(self.__IMAGE_PATH)
        # Create a figure with the original dimensions
        self.fig, self.ax = plt.subplots(figsize=(image.shape[1] / 100, image.shape[0] / 100))
        # Display the image
        self.ax.imshow(image)
        # Turn off axes
        self.ax.axis('off')
        # Set the scatter plot
        self.scatter = self.ax.scatter([], [], marker=self.MARKERS[idx], color=self.COLORS[idx], s=50)
        # Set the line plot
        self.line, = self.ax.plot([], [], color=self.COLORS[idx], linestyle=self.LINE_STYLES[idx], linewidth=2)

    # Get all coordinates from the addresses
    def _populate_route_dict(self):
        """
        Populates the route dictionary with the addresses and their corresponding coordinates.

        Parameters:
        - None

        Returns:
        - None
        """
        for address in self.addresses:
            if address in self.__ALL_COORDINATES:
                self.route[address] = self.__ALL_COORDINATES[address]

    # Update after two_opt_swap and load_packages_nearest_neighbor used
    def update_address(self, new_addresses):
        """
        Update the address attribute of the object.

        Args:
            new_addresses (str): The new addresses to be assigned to the address attribute.

        Returns:
            None
        """
        self.addresses = new_addresses

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

    # Visualize package locations
    def visualize_package_locations(self):
        # Set up the figure in a clean state
        self._setup_figure()
        # Overlay markers on the visualization
        self._populate_route_dict()
        # Get all the coordinates
        all_points = [(x, y) for x, y in self.route.values()]
        # Update the scatter plot with the new coordinates
        self.scatter.set_offsets(all_points)
        plt.title(f"{self.truck_name}, Package Locations")
        # Display the visualization with markers using SciView
        plt.show()

        # Clears the route for the next visualization
        self.route = {}

    def visualize_truck_route(self):
        # Set up the figure in a clean state
        self._setup_figure()

        self._populate_route_dict()

        x, y = self._get_coord_and_close_route()

        # Update the line plot
        self.line.set_data(x, y)

        plt.title(f'{self.truck_name} Truck Route')

        # Re-render the figure
        self.fig.canvas.draw_idle()
        plt.show()
        # Clears the figure to make sure start fresh for the next visualization
        plt.close(self.fig)

        # Clears the route for the next visualization
        self.route = {}

    def visualize_all_truck_routes(self, trucks_list):
        # Set up the figure in a clean state
        self._setup_figure()
        legend_labels = []
        line_objects = []

        # Collect all routes data
        all_routes = []
        for idx, truck in enumerate(trucks_list):
            route = {}
            for address in truck.route:
                route[address] = self.__ALL_COORDINATES[address]
            all_routes.append(route)

        for idx, route in enumerate(all_routes):
            # Reset the route for each truck
            self.route = route

            x, y = self._get_coord_and_close_route()

            # Update the line plot
            line, = self.ax.plot(x, y, color=self.COLORS[idx], linestyle=self.LINE_STYLES[idx],
                                 marker=self.MARKERS[idx], linewidth=2)
            line_objects.append(line)
            legend_labels.append(f"Truck {trucks_list[idx].truck_name}")

        self.ax.legend(handles=line_objects, labels=legend_labels, loc='upper right', shadow=True)

        # Draw the figure
        plt.draw()

        # Show the visualization
        plt.title('All Truck Routes')
        plt.show()
        # Clears the figure to make sure start fresh for the next visualization
        plt.close(self.fig)
        # Reset the route for the next visualization
        self.route = {}

    def visualize_pie_chart(self, filtered_packages):
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
        explode = tuple(0.1 for _ in range(len(labels)))  # Dynamically create explode tuple based on length of labels
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        plt.title(f'{self.truck_name} Package Status Distribution')
        plt.show()
