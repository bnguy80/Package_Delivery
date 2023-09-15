import csv
from pathlib import Path

import matplotlib.pyplot as plt


class Visualize:
    _instance = None  # Single instance storage
    _initialized = False  # Initialization flag
    COLORS = ['red', 'blue', 'green']  # High Priority, Medium Priority, Low Priority
    LINE_STYLES = ['-', '--', ':']  # Solid, Dashed, Dotted line styles
    MARKERS = ['o', 's', '^']  # Circle, Square, Triangle markers

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Visualize, cls).__new__(cls)
        return cls._instance

    def __init__(self, truck_id):
        """
        Initialize the Visualize object
        """
        current_directory = Path(__file__).parent
        if not Visualize._initialized:
            self.__IMAGE_PATH = current_directory / "Picture1.jpg"
            # Create a figure and axes
            self.fig, self.ax = None, None
            # Create a scatter plot
            self.scatter = None
            # Create a line plot
            self.line = None
            self.route = {}
            self.address = {}
            # All coordinates (x, y) dictionary; visualize a Picture1.jpg dimensions 672x756
            self.__ALL_COORDINATES = self._load_coordinates_from_csv()
            Visualize._initialized = True

        if truck_id not in self.route:
            self.route[truck_id] = {}
        if truck_id not in self.address:
            self.address[truck_id] = {}

    def _setup_figure(self, truck_id):
        """
        Set up the figure for plotting the truck's data.

        Parameters:
            truck_id (int): The ID of the truck.

        Returns:
            None
        """
        idx = (truck_id - 1) % 3
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

    @classmethod
    def _load_coordinates_from_csv(cls):
        """
        Load the coordinates from a CSV file.
        """
        # Read the CSV file
        coordinates = {}
        current_directory = Path(__file__).parent
        csv_path = current_directory / 'address_coordinates.csv'
        with csv_path.open('r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                address = row[0]
                x = int(row[1])
                y = int(row[2])
                coordinates[address] = (x, y)
        return coordinates

    # Get all coordinates from the addresses
    def _populate_route_dict(self, truck_id):
        """
        Populates the route dictionary with the addresses and their corresponding coordinates.

        Parameters:
        - truck_id (int): The truck ID.

        Returns:
        - None
        """
        for address in self.address[truck_id]:
            if address in self.__ALL_COORDINATES:
                self.route[truck_id][address] = self.__ALL_COORDINATES[address]

    def populate_address(self, truck_id, address):
        """
        Populate the address attribute of the object.
        """
        self.address[truck_id] = address

    # Update after two_opt_swap and load_packages_nearest_neighbor used
    def update_address(self, new_addresses, truck_id):
        """
        Update the address attribute of the object.

        Args:
            new_addresses (any): The new addresses to be assigned to the address attribute.
            truck_id (int): The truck ID.

        Returns:
            None
        """
        self.address[truck_id] = new_addresses

    def _get_coord_and_close_route(self, truck_id):
        """
        Get the coordinates and close the route.

        Returns:
            Tuple: The x and y coordinates of the route.
        """
        x, y = zip(*self.route[truck_id].values())
        # Close the route by adding the first and last coordinates
        if x[0] != x[-1] or y[0] != y[-1]:
            x = x + (x[0],)
            y = y + (y[0],)
        return x, y

    # Visualize package locations
    def visualize_package_locations(self, truck_id, truck_name):
        """
        Visualize package locations for a given truck.

        Parameters:
            truck_id (int): The ID of the truck.
            truck_name (str): The name of the truck.

        Returns:
            None
        """
        # Set up the figure in a clean state
        self._setup_figure(truck_id)
        # Overlay markers on the visualization
        self._populate_route_dict(truck_id)
        # Get all the coordinates
        all_points = [(x, y) for x, y in self.route[truck_id]]
        # Update the scatter plot with the new coordinates
        self.scatter.set_offsets(all_points)
        plt.title(f"{truck_name}, Package Locations")
        # Display the visualization with markers using SciView
        plt.show()

        # Clears the route for the next visualization
        self.route = {}

    def visualize_truck_route(self, truck_id, truck_name):
        """
        Visualizes the route of a truck on a figure.

        Parameters:
            truck_id (int): The ID of the truck.
            truck_name (str): The name of the truck.

        Returns:
            None
        """
        # Set up the figure in a clean state
        self._setup_figure(truck_id)

        self._populate_route_dict(truck_id)

        x, y = self._get_coord_and_close_route(truck_id)

        # Update the line plot
        self.line.set_data(x, y)

        plt.title(f'{truck_name} Truck Route')

        # Re-render the figure
        self.fig.canvas.draw_idle()
        plt.show()
        # Clears the figure to make sure start fresh for the next visualization
        plt.close(self.fig)

        # Clears the route for the next visualization
        self.route[truck_id] = {}

    def dynamic_truck_route(self, truck_id, truck_name):

        self._setup_figure(truck_id)

        self._populate_route_dict(truck_id)

        x, y = self._get_coord_and_close_route(truck_id)

        plt.title(f'{truck_name} Truck Route')

        # Re-render the figure
        self.fig.canvas.draw_idle()
        plt.show()
        # Clears the figure to make sure start fresh for the next visualization
        plt.close(self.fig)

        # Clears the route for the next visualization
        self.route[truck_id] = {}

    def visualize_all_truck_routes(self, trucks_list, truck_id):
        """
        Visualizes all truck routes on a single plot.

        Parameters:
            trucks_list (list): A list of Truck objects representing the trucks whose routes will be visualized.
            truck_id (int): The ID of the truck to be able to set up the visualization.

        Returns:
            None
        """
        # Set up the figure in a clean state
        self._setup_figure(truck_id)
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
            self.route[truck_id] = route

            x, y = self._get_coord_and_close_route(truck_id)

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
        self.route[truck_id] = {}

    def visualize_pie_chart(self, filtered_packages, truck_name):
        """
        Visualizes a pie chart of the package status distribution for a given truck.

        Parameters:
            filtered_packages (list): A list of tuples containing package information and status.
            truck_name (str): The name of the truck.

        Returns:
            None
        """
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
        plt.title(f'{truck_name} Package Status Distribution')
        plt.show()
