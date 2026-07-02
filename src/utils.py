import numpy as np
import networkx as nx

from scipy.spatial import KDTree


def combine_near_nodes(g:nx.Graph, coordinates:dict|np.ndarray, threshold:float):
    """
    Combines nodes in a graph that are closer than a given distance threshold.

    Parameters
    ----------
        g : nx.Graph
            The original graph to be processed.
        coordinates : dict or np.ndarray
            Mapping of node IDs to their spatial coordinates, or an array of coordinates.
        threshold : float
            The maximum distance between nodes to be considered for combination.

    Returns
    -------
        g_combined : networkx.Graph
            A new graph with nearby nodes combined.
        coordinates : numpy.ndarray or dict
            The updated coordinates including the newly combined nodes.
    """
    nodes_to_remove, node_mapping, coordinates = remove_nodes(g, coordinates, threshold)

    # Create a new graph with combined nodes
    g_combined = nx.Graph()
    for node in g.nodes():
        if node not in nodes_to_remove:
            g_combined.add_node(node, pos=(coordinates[node][1], coordinates[node][0]))

    g_combined = combine_edges(g, node_mapping, g_combined)

    for new_node in set(node_mapping.values()):
        g_combined.add_node(new_node, pos=(coordinates[new_node][1], coordinates[new_node][0]))

    return g_combined, coordinates

def combine_edges(g:nx.Graph, node_mapping:dict, g_combined:nx.Graph):
    """
    Transfers edges from the original graph to the combined graph using a node mapping.

    Parameters
    ----------
        g : nx.Graph
            The original graph containing the original edges.
        node_mapping : dict
            Dictionary mapping original node IDs to their new combined node IDs.
        g_combined : nx.Graph
            The new graph where the updated edges will be added.

    Returns
    -------
        g_combined : nx.Graph
            The combined graph with fully updated edges.
    """

    for u, v in g.edges():
        if u == v:
            continue
        if u in node_mapping and v in node_mapping:
            if node_mapping[u] != node_mapping[v]:
                g_combined.add_edge(node_mapping[u], node_mapping[v])
        elif u in node_mapping:
            g_combined.add_edge(node_mapping[u], v)
        elif v in node_mapping:
            g_combined.add_edge(u, node_mapping[v])
        else:
            g_combined.add_edge(u, v)
    
    return g_combined

def remove_nodes(g:nx.Graph, coordinates:dict|np.ndarray, threshold:float):
    """
    Identifies nodes to combine based on distance, calculating new centroids and mappings.

    Parameters
    ----------
        g : nx.Graph
            The graph containing the nodes to evaluate.
        coordinates : dict or np.ndarray
            Spatial coordinates of the nodes.
        threshold : float
            The maximum distance radius to query for neighboring nodes.

    Returns
    -------
        nodes_to_remove : set
            A set of original node IDs that have been grouped and should be removed.
        node_mapping : dict
            Mapping of original node IDs to their newly assigned node IDs.
        final_coordinates : np.ndarray or dict
            The updated set of coordinates containing the new combined centroids.
    """    
    nodes_to_remove = set()
    node_mapping = {}
    n_nodes = len(g.nodes())
    coords = np.array([coordinates[node] for node in g.nodes()])
    node_list = list(g.nodes())

    if not coords.size:
        return nodes_to_remove, node_mapping, coordinates
    
    tree = KDTree(coords)
    processed = [False]*n_nodes

    new_coordinates = []
    
    for i in range(n_nodes):
        if processed[i]:
            continue

        near_indices = tree.query_ball_point(coords[i], r=threshold)
        near_nodes = {node_list[idx] for idx in near_indices}

        if len(near_nodes) > 1:
            near_coords = [coordinates[node] for node in near_nodes]
            combined_coords = np.mean(near_coords, axis=0)
            new_node_index = len(new_coordinates)
            new_coordinates.append(combined_coords)
            
            for node in near_nodes:
                node_mapping[node] = n_nodes + new_node_index 
                nodes_to_remove.add(node)
                processed[node_list.index(node)] = True
        else:
            new_coordinates.append(coords[i])
            if node_list[i] not in nodes_to_remove:
                node_mapping[node_list[i]] = i 
                processed[i] = True
    
    if new_coordinates:
        final_coordinates = update_coordinates(coordinates, new_coordinates)

    else:
        final_coordinates = coordinates
        
    return nodes_to_remove, node_mapping, final_coordinates


def update_coordinates(coordinates:np.ndarray, new_coordinates:list|np.ndarray):
    """
    Appends calculated centroid coordinates to the existing coordinates array.

    Parameters
    ----------
        coordinates : np.ndarray
            The original array of node coordinates.
        new_coordinates : list or np.ndarray
            A collection of newly generated coordinate points to be added.

    Returns
    -------
        updated_coordinates : np.ndarray
            A new array containing both the original and the newly added coordinates.
    """
    updated_coordinates = coordinates.copy()
    
    for _, coord in enumerate(new_coordinates):
        updated_coordinates = np.append(updated_coordinates, [coord],axis=0)

    return updated_coordinates
