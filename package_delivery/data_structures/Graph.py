import csv
from package_delivery.data_structures.HashMap import package_hashmap


# print(package_hashmap) # hashmap object printing correctly

class Graph:
    def __init__(self):
        self.vertices = {}  # Dictionary of all vertices, which will be street address and their associated packages
        self.edge_weight = {}  # Dictionary that will act as an adjacency list. Store edges and their weights between
        # vertices

    # Add new vertices to the graph.
    # Takes vertex(address) as parameter adds it to key 'vertices' dictionary with an empty list of values.
    # Prepares the vertex to have edges connected to it later
    def add_vertex(self, vertex):
        self.vertices[vertex] = []

    def get_all_vertices(self):
        return self.vertices.items()

    # Add edges between vertex1 and vertex2 and the weight between them
    # Creates dictionaries for vertex1 and vertex2 and inner dictionaries for vertex1 and vertex2
    def add_edge(self, vertex1, vertex2, weight=1.0):
        # self.edge_weight = [(edges)] = weight
        # Checks if vertex1 and vertex2 exist in the vertices dictionary
        if vertex1 in self.vertices and vertex2 in self.vertices:
            # If vertex1 not already in the dictionary then create an empty inner dictionary for vertex1
            if vertex1 not in self.edge_weight:
                self.edge_weight[vertex1] = {}
            # If vertex2 not already in the dictionary then create an empty inner dictionary for vertex2
            if vertex2 not in self.edge_weight:
                self.edge_weight[vertex2] = {}
            self.edge_weight[vertex1][
                # Add vertex2 as the key of the inner dictionary of vertex1 with weight as the value -> key-value pair
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

    # Still figuring out how to associate directly from HashMap object 7/19/23, Accomplished 7/19/23 4pm
    # def insert_packages_vertex_associate(self, hashmap):
    #     for bucket in hashmap.map:
    #         for item in bucket:
    #             vertex_key = item[1].address
    #             if vertex_key in self.vertices:
    #                 self.vertices[vertex_key].append(item)
    #             else:
    #                 self.vertices[vertex_key] = [item]
    #                 # Associate edge weight with each package
    #             for vertex1, edges in self.edge_weight.items():
    #                 for vertex2, weight in edges.items():
    #                     for package in self.vertices[vertex1]:
    #                         package[1].edge_weight = weight
    #                         print(package[1].edge_weight)
    def insert_packages_vertex_associate(self, hashmap):
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


# Get data from WGUPS_distances in order to create edges between vertices
def get_csv_vertex_distances(fileName):
    csv_distances = []  # To get all data from WGUPS_distances.csv
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  # Skip header
        for row in csv_reader:
            csv_distances.append(row)
        # for element in csv_distances: # To print single array into 2D column-row format
        #     print(element)
    return csv_distances


# Load graph with vertices and weights
def load_graph(fileName):
    data = get_csv_vertex_distances(fileName)
    graph = Graph()
    for row in data:
        graph.add_vertex(row[1])  # Addresses will act as vertices
        for i in range(3, len(row)):  # 0-2 indexes are location_name, location_street, location_zip.
            vertex1 = row[1]
            vertex2 = data[i - 3][1]
            weight = float(row[i])
            graph.add_edge(vertex1, vertex2, weight)
    return graph


# Print all vertices and weights in Edge: vertex1 -> vertex2, Weight: format
# It iterates over the graph.edge_weight dictionary, which is functions like an adjacency list of the graph.
def print_graph_edge_weight(graph):
    # Iterates over each vertex to retrieve edges and weights
    for vertex1, edges in graph.edge_weight.items():
        # Inner loop, prints src vertex(vertex1),dest vertex(vertex2), and weight of the edge
        for vertex2, weight in edges.items():
            print(f"Edge: {vertex1} -> {vertex2}, Weight: {weight}")


# Print edges in the graph and associated packages
# Help visualize the edges in the graph along with the associated packages with each vertex
def print_edges_packages_asc(graph):
    [print(f"Edge: {vertex1} -> {vertex2}, Weight: {weight}") for vertex1, edges in graph.edge_weight.items() for
     vertex2, weight in edges.items()]
    [print(f"Edge: {vertex1} -> {vertex2}, Associated Package: {package}") for vertex1, edges in
     graph.edge_weight.items() for vertex2, weight in edges.items() if vertex1 in
     graph.vertices for package in graph.vertices[vertex1]]
    print()


# Print the vertices and associated packages in a human-readable format
def print_vertices_packages_asc(graph):
    for vertex, packages in graph.vertices.items():
        print(f"Vertex: {vertex}")
        for package in packages:  # Key-value pair print
            print(f"  - Package ID: {package.package_id}")
            print(f"  - Value: {package}")
            print()


# def print_graph_packages(graph):
#     for vertex1, edges in graph.edge_weight.items():
#         for vertex2, weight in edges.items():
#             if vertex1 in graph.vertices:
#                 for package in graph.vertices[vertex1]:
#                     print(f"Edge: {vertex1} -> {vertex2}, Associated Package: {package}")
#         print()


# Print package with specified delivery deadline
# For testing purposes
def print_package_deadline_asc(graph, delivery_deadline):
    for vertex, packages in graph.vertices.items():
        # print(f"Vertex: {vertex}")
        for package in packages:
            # Check if the package has the specified deadline in its
            # deadline attribute
            if delivery_deadline == package.delivery_deadline:
                print(f"  - Package ID: {package.package_id}")
                print(f"  - Value: {package}")
                print()


graph_access = load_graph(r'C:\Users\brand\IdeaProjects\Package_Delivery_Program_New\package_delivery\data_structures'
                          r'\WGUPS_distances.csv')
# graph_access.insert_packages_vertex_associate(package_hashmap)
graph_access.insert_packages_vertex_associate(package_hashmap)


# print_vertex_packages_asc(graph_access)
# print_edge_packages_asc(graph_access)
# print(graph_access.edge_weight)
# print_vertices(graph)
# all_vertices = get_all_vertices(graph)
# print(all_vertices)
# print_graph(graph)
# print_graph_associations(graph)

# graph.print_graph_packages_asc()

# print(graph_access.get_all_vertices())
# print(graph_access.vertices)
# delivery_deadline1 = "9:00 AM"
# print_package_deadline_asc(graph_access, delivery_deadline1)

# get_edge_packages_asc(graph_access, '600 E 900 South')

# 7/25/23: All 40 packages associated correctly with their vertex(address)
# print(graph_access.edge_weight)

