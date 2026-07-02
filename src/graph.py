import skan
import numpy as np 
import networkx as nx 
from utils import combine_near_nodes


class Graph:
    """
    A class for manage the graph.

    Attributes
    ----------
    image : str
        skeleton image.
    digits : int
        digits used for parameter calculation.
    threshold_distance: int
        distance used for merging close nodes (in pixels).
    nodes : int 
        Number of nodes.
    edges : int
        Number of edges.
    is_connected : bool
        connection flag.
    average_degree : float
        graph average degree.
    density : float
        graph density.
    global efficiency : float
        graph global efficiency.
    clustering_coefficient : float
        graph clustering coefficient.
    average_closeness_centrality : float
        graph average closeness centrality.
    interconnection_probability : float
        graph interconnection probability.
    wiener_index : float
        graph wiener index.
    diameter : float
        graph diameter.
    beta_index : float
        graph beta index.
    
    Methods
    -------
    create:
        saves a given imagen in the main results folder.
    get_parameters:
        saves the graph parameters into a dictionary.
    
    """
    
    def __init__(self, image:np.array, threshold_distance:int=5, digits:int=5):
        """
        Constructs all the necessary attributes for obtaining the representative graph and parameter calculation.

        Parameters
        ----------
            image : np.array.
                skeleton representation.
            threshold_distance : int (5)
                distance used for merging close nodes (in pixels).
            digits : int (5)
                number of digits used for parameter calculation.
        """   

        self.image = image
        self._digits = digits
        self.threshold_distance = threshold_distance
        self.create()

    @property
    def nodes(self):
        return nx.number_of_nodes(self.graph_)
    
    @property
    def edges(self):
        return nx.number_of_edges(self.graph_)
    
    @property
    def is_connected(self):
        return nx.is_connected(self.graph_)

    @property
    def average_degree(self):
        degree_list = nx.degree(self.graph_)
        return round(sum(dict(degree_list).values()) / len(degree_list), self._digits)
    
    @property
    def density(self):
        return round(nx.density(self.graph_), self._digits)
    
    @property   
    def global_efficiency(self):
        return round(nx.global_efficiency(self.graph_), self._digits)
    
    @property    
    def clustering_coefficient(self):
        return round(nx.average_clustering(self.graph_), self._digits)

    @property
    def average_closeness_centrality(self):
        closeness = nx.closeness_centrality(self.graph_)
        return round(sum(closeness.values()) / len(closeness), self._digits)
    
    @property
    def interconnection_probability(self):
        return round(self.average_degree / self.nodes, self._digits)
    
    @property
    def wiener_index(self):
        if self.is_connected:
            return round(nx.wiener_index(self.graph_), self._digits)
        else:
            largest_cc = max(nx.connected_components(self.graph_), key=len)
            largest_sg = nx.subgraph(self.graph_, largest_cc)
            return round(nx.wiener_index(largest_sg), self._digits)
        
    @property
    def diameter(self):

        if self.is_connected:
            return round(nx.diameter(self.graph_), self._digits)
        else:
            largest_cc = max(nx.connected_components(self.graph_), key=len)
            largest_sg = nx.subgraph(self.graph_, largest_cc)
            return round(nx.diameter(largest_sg), self._digits)
    
    @property
    def beta_index(self):
        nodes = self.graph_.number_of_nodes()
        
        if nodes == 0:
            return 0.0
            
        edges = self.graph_.number_of_edges()
        beta = edges / nodes
        
        return round(beta, self._digits)

    def create(self):
        """
        creates the representative graph with a merging stage to combine near nodes.

        Parameters
        ----------
            None

        Returns
        -------
            None
        """

        skeleton_analysis = skan.Skeleton(self.image)
        
        graph_df = skan.summarize(skeleton_analysis, separator='-')
        g_full = nx.Graph(skeleton_analysis.graph)
        
        # 2. Identify Junctions based on Node Degree
        junction_nodes = [node for node, degree in g_full.degree() if degree > 2 or degree == 1]
        
        # 3. Create Junction Nodes Graph
        g_junctions = nx.Graph()

        for i, node_id in enumerate(junction_nodes):
            g_junctions.add_node(i, pos=(skeleton_analysis.coordinates[node_id][1], skeleton_analysis.coordinates[node_id][0]), original_id=node_id)

        # 4. Connect Junctions Based on Branches
        for index, row in graph_df.iterrows():
            node_0 = row['node-id-src']
            node_1 = row['node-id-dst']
            if node_0 in junction_nodes and node_1 in junction_nodes:
                junction_index_0 = list(junction_nodes).index(node_0)
                junction_index_1 = list(junction_nodes).index(node_1)
                g_junctions.add_edge(junction_index_0, junction_index_1)

        # 5. Combine Near Junction Nodes
        junction_coordinates = np.array([skeleton_analysis.coordinates[node] for node in junction_nodes])

        self.graph_, _ = combine_near_nodes(g_junctions.copy(), junction_coordinates.copy(), self.threshold_distance)
    
    def get_parameters(self):
        """
        populates a dictionary with the graph properties.

        Parameters
        ----------
            None

        Returns
        -------
            dict with graph parameters.
        """
        return {
            "Nodes": [self.nodes],
            "Edges": [self.edges],
            "Is connected": [self.is_connected],
            "Average degree": [self.average_degree],
            "Density": [self.density],
            "Gloabl efficiency": [self.global_efficiency],
            "Clustering coefficient": [self.clustering_coefficient],
            "Average closeness centrality": [self.average_closeness_centrality],
            "Interconnection probability": [self.interconnection_probability],
            "Wiener index": [self.wiener_index],
            "Diameter": [self.diameter],
            "Beta index": [self.beta_index]
        }

    