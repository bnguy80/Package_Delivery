import csv
from package_delivery.datastructures.hash_map import package_hashmap


# The Graph class we will use to represent the delivery locations and distances associated with each package
# and creating associations between vertices and package objects stored in HashMap class
class Graph:
    """
    Class to represent the graph that will be used to represent the delivery locations and distances associated with
    each package.

    Attributes:
        vertices (dict): Dictionary of all vertices, which will be street address and their associated packages
        edge_weight (dict): Dictionary that will act as an adjacency list. Store edges and their weights between
        vertices
    """

    def __init__(self):
        """
        Initialize the graph object
        """
        self.vertices = {}  # Dictionary of all vertices, which will be street address and their associated packages
        self.edge_weight = {}  # Dictionary that will act as an adjacency list. Store edges and their weights between
        # vertices

    # Add new vertices to the graph.
    # Takes vertex(address) as parameter adds it to key 'vertices' dictionary with an empty list of values.
    # Prepares the vertex to have edges connected to it later
    def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.

        Parameters:
            vertex (str): The vertex to be added to the graph.

        """
        self.vertices[vertex] = []

    def get_all_vertices(self):
        """
        Get all vertices in the graph.

        Returns:
            A view object containing all the vertices in the graph.
        """
        return self.vertices.items()

    # Add edges between vertex1 and vertex2, and the weight between them
    # Creates dictionaries for vertex1 and vertex2 and inner dictionaries for vertex1 and vertex2
    def _add_edge(self, vertex1, vertex2, weight=1.0):
        """
        Adds an edge between two vertices in the graph with an optional weight.

        Parameters:
            vertex1 (str): The first vertex.
            vertex2 (str): The second vertex.
            weight (float, optional): The weight of the edge.
            Default to 1.0.

        Returns:
            bool: True if the edge is successfully added, False otherwise.
        """
        # self.edge_weight = [(edges)] = weight
        # Checks if vertex1 and vertex2 exist in the vertices dictionary
        if vertex1 in self.vertices and vertex2 in self.vertices:
            # If vertex1 not already in the dictionary, then create an empty inner dictionary for vertex1
            if vertex1 not in self.edge_weight:
                self.edge_weight[vertex1] = {}
            # If vertex2 not already in the dictionary, then create an empty inner dictionary for vertex2
            if vertex2 not in self.edge_weight:
                self.edge_weight[vertex2] = {}
            self.edge_weight[vertex1][
                # Add vertex2 as the key to the inner dictionary of vertex1 with weight as the value -> key-value pair
                vertex2] = weight
            # Add vertex1 as the key of the inner dictionary of vertex2 with weight as the
            # value -> key-value pair
            # if vertex1 != vertex2: # If vertex1 and vertex2 are not the same, add vertex1 as key of the inner
            # dictionary of vertex2 with weight as the value -> key-value pair self.edge_weight[vertex2][vertex1] =
            # weight
            self.edge_weight[vertex2][vertex1] = weight
            return True
        else:
            return False

    def insert_packages_vertex_associate(self, hashmap):
        """
        Inserts packages into the vertex associate.

        Parameters:
            hashmap (HashMap): A hashmap containing the packages to be inserted.

        Returns:
            None
        """
        for bucket in hashmap.map:
            for item in bucket:
                package_package = item[1].address
                package = item[1]
                if package_package in self.vertices:
                    self.vertices[package_package].append(package)
                else:
                    self.vertices[package_package] = [package]

        for address, packages in self.vertices.items():
            for package in packages:
                if package.address in self.edge_weight:
                    package.edge_weight = self.edge_weight[package.address]
                    break
            else:
                for vertex1, edges in self.edge_weight.items():
                    for vertex2, weight in edges.items():
                        if package.address == vertex1 or package.address == vertex2:
                            package.edge_weight = weight
                            break

    # Helper function to get data from WGUPS_distances in order to create edges between vertices
    @staticmethod
    def get_csv_vertex_distances(file_name):
        """
        Retrieves the vertex distances from a CSV file.

        Parameters:
            file_name (str): The name of the CSV file containing the vertex distances.

        Returns:
            list: A list of lists representing the vertex distances.
        """
        csv_distances = []  # To get all data from WGUPS_distances.csv
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None)  # Skip header
            for row in csv_reader:
                csv_distances.append(row)

        return csv_distances

    # Load graph with vertices and weights
    def load_graph(self, file_name):
        """
        Loads a graph from a CSV file.

        Parameters:
            file_name (str): The name of the CSV file.

        Returns:
            self (Graph): The updated graph object.
        """
        data = self.get_csv_vertex_distances(file_name)
        for row in data:
            self.add_vertex(row[1])  # Addresses will act as vertices
            for i in range(3, len(row)):  # 0-2 indexes are location_name, location_street, location_zip.
                vertex1 = row[1]
                vertex2 = data[i - 3][1]
                weight = float(row[i])
                self._add_edge(vertex1, vertex2, weight)
        return self

    # Print all vertices and weights in Edge: vertex1 -> vertex2, Weight: format
    # It iterates over the graph.edge_weight dictionary, which is functions like an adjacency list of the graph.
    def print_graph_edge_weight(self):
        """
        Prints the edges and their weights in the graph.

        This function iterates over each vertex in the graph and retrieves the edges and their weights associated
        with it.
        It then prints the source vertex, destination vertex, and weight of each edge.

        Returns:
            None
        """
        # Iterates over each vertex to retrieve edges and weights
        for vertex1, edges in self.edge_weight.items():
            # Inner loop, prints src vertex(vertex1),dest vertex(vertex2), and weight of the edge
            for vertex2, weight in edges.items():
                print(f"Edge: {vertex1} -> {vertex2}, Weight: {weight}")

    # Print edges in the graph and associated packages
    # Help visualize the edges in the graph along with the associated packages with each vertex
    def print_edges_packages_asc(self):
        """
        Prints the edges and associated packages in ascending order of weight.

        This function iterates over the edge_weight dictionary and prints each edge along with its weight.
        It then
        iterates over the same dictionary again and prints each edge along with its associated package,
        but only if
        the vertex1 is present in the vertices' dictionary.


        Returns:
            None
        """
        [print(f"Edge: {vertex1} -> {vertex2}, Weight: {weight}") for vertex1, edges in self.edge_weight.items() for
         vertex2, weight in edges.items()]
        [print(f"Edge: {vertex1} -> {vertex2}, Associated Package: {package}") for vertex1, edges in
         self.edge_weight.items() for vertex2, weight in edges.items() if vertex1 in
         self.vertices for package in self.vertices[vertex1]]
        print()

    # Print the vertices and associated packages in a human-readable format
    def print_vertices_packages_asc(self):
        """
        Prints the vertices and their associated packages in ascending order.

        Returns:
            None
        """
        for vertex, packages in self.vertices.items():
            print(f"Vertex: {vertex}")
            for package in packages:  # Key-value pair print
                print(f"  - Package ID: {package.package_id}")
                print(f"  - Value: {package}")
                print()

    # Print package with specified delivery deadline
    # For testing purposes
    def print_package_deadline_asc(self, delivery_deadline):
        """
        Print the details of all packages with a specified delivery deadline in ascending order.

        Parameters:
            delivery_deadline (str): The delivery deadline to search for.

        Returns:
            None
        """
        for vertex, packages in self.vertices.items():
            for package in packages:
                # Check if the package has the specified deadline in its
                # deadline attribute
                if delivery_deadline == package.delivery_deadline:
                    print(f"  - Package ID: {package.package_id}")
                    print(f"  - Value: {package}")
                    print()


graph_access = Graph()
graph_access.load_graph(r'C:\Users\brand\IdeaProjects\Package_Delivery_Program_New\package_delivery\datastructures'
                        r'\WGUPS_distances.csv')
graph_access.insert_packages_vertex_associate(package_hashmap)

# 7/25/23: All 40 packages associated correctly with their vertex(address)
