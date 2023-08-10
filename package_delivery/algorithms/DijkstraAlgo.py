import heapq
import math


# src-> Hub to start all deliveries from
# min_heap as priority queue to find minimum-distance neighbor, greedy approach: find min_distance
# visited_queue = [] node after find minimum-distance neighbor
# find path to from start_vertex to end_vertex pred_vertex, whenever comparison to assign distance, append pred_vertex
#
def dijkstra(graph1, src):
    distances: dict = {node: math.inf for node in graph1.vertices}  # Initialize distances to infinity
    # print("Initialized distances to infinity: ", distances)  # Add debug print
    pred_vertex: dict = {node: None for node in graph1.vertices}  # Initialize predecessor vertices to None
    # print("pred_vertex", pred_vertex)  # Add debug print
    distances[src] = 0  # Set source vertex distance to 0
    # The min-heap is used to prioritize processing vertices with the shortest known distance first,
    # ensuring that we find the shortest paths efficiently during the Dijkstra's algorithm execution.
    min_heap = [(0, src)]  # Create a min-heap queue of (distance, vertex) tuples
    # print("DISTANCES-BEFORE: ", edge_weights, "\n")  # Edge_weights before Dijkstra's algo
    # print(edge_weights[src])  # dict_items

    # for key, value in edge_weights.values():
    #     print(int(value))
    # for location, weight in edge_weights.values():
    #     print(f"{location}: {weight}")
    visited_queue = []  # Track visited vertices

    # Continue the loop until the min_heap is not empty.
    # The min_heap will be empty when all vertices have been visited and processed.
    while min_heap:
        # Pop the vertex with the smallest distance from the min_heap.
        # Will be src vertex initially
        # The heapq.heappop() function automatically selects the vertex with the smallest distance
        # due to the use of a min-heap.
        current_distance, current_vertex = heapq.heappop(min_heap)
        # print("Current_Distance: ", current_distance, "Current_Vertex: ", current_vertex)  # Add debug print
        # Skip if already in visited_queue and current_distance is currently stored distance
        if current_vertex in visited_queue and current_distance > distances[current_vertex]:
            continue
        visited_queue.append(current_vertex)  # Mark the vertex as visited
        # print("Edge_weights: ", edge_weights)
        # Iterate over the neighbors of the current_vertex and their corresponding weights
        for neighbor, weight in graph1.edge_weight[current_vertex].items():

            # print("edge_weights[current_vertex].values()== ", edge_weights[current_vertex].values())
            # print("Neighbor: ", neighbor)
            # Calculate the distance from the src vertex to this neighbor by adding the weight of the edge
            # connecting them to the current_distance
            distance = current_distance + weight
            # If the calculated distance is smaller than the current known distance to the neighbor,
            # update the distances dictionary with the new, smaller distance.
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # print("\n", "MINIMUM DISTANCE NEIGHBOR ", distances[neighbor],
                #       "\n")  # Add debug print, comparison between neighbors of current_vertex to choose minimum one
                # Update the predecessor vertex for the 'neighbor' vertex to be the 'current_vertex'.
                pred_vertex[neighbor] = current_vertex
                # Push the updated distance and 'neighbor' vertex as a tuple into the min-heap.
                # This ensures that the 'neighbor' vertex will be processed later with its updated distance.
                heapq.heappush(min_heap, (distance, neighbor))
    return distances, pred_vertex


def print_distances_and_pred_vertex(distances, pred_vertex):
    print("Distances:")
    for vertex, distance in distances.items():
        print(f"{vertex}: {distance}")

    print("\nPredecessor Vertices:")
    for vertex, predecessor in pred_vertex.items():
        print(f"{vertex}: {predecessor}")


# def build_path(pred_vertex, destination):
#     path = [destination]
#     print("Path: ", path)
#     while pred_vertex[destination] is not None:
#         destination = pred_vertex[destination]
#         path.insert(0, destination)
#     return path


# def print_distances_and_path(distances, pred_vertex, source_vertex):
#     print("Distances and Paths from Source Vertex:")
#     for vertex, distance in distances.items():
#         path = build_path(pred_vertex, vertex)
#         if distance != float('inf'):
#             print(f"{vertex}: {distance} (Path: {source_vertex} -> {' -> '.join(path)})")
#         else:
#             print(f"{vertex}: Not Reachable")

# def reconstruct_path(previous, target):
#     path = []
#     while target is not None:
#         path.insert(0, target)
#         target = previous[target]
#     return path


# target1 = '1060 Dalton Ave S'
# distances1, pred_vertex1 = dijkstra(graph_access, '4001 South 700 East', '5383 South 900 East #104')
# print("DISTANCES-DIJKSTRA, PRED_VERTEX == ", distances1, pred_vertex1)
# print(reconstruct_path(pred_vertex1,  target1))
# print_distances_and_path(distances1, pred_vertex1, '1060 Dalton Ave S')
# print(graph.vertices)