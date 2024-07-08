import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Build a class that contain 5 numbers in 5 variables D the duration of the simulator, I the number of intersections, S the number of streets , V the number of cars, F the bonus points for each car that reaches
class Simulator:
    """
    A class representing a traffic signal simulator.
    """
    def __init__(self, name: str, D: int, I: int, S: int, V: int, F: int, streets_desc: pd.DataFrame, car_paths_desc: pd.DataFrame) -> None:
        """
        Initializes the Simulator object with the given parameters.

        Parameters:
        - name (str): The name of the simulation.
        - D (int): The duration of the simulator.
        - I (int): The number of intersections.
        - S (int): The number of streets.
        - V (int): The number of cars.
        - F (int): The bonus points for each car that reaches its destination.
        - streets_desc (pd.DataFrame): A DataFrame of street descriptions.
        - car_paths_desc (pd.DataFrame): A DataFrame of car path descriptions.
        """
        self.simulation_name = name
        self.D = D
        self.I = I
        self.S = S
        self.V = V
        self.F = F

        self.streets_desc = streets_desc[0].apply(lambda x: pd.Series(x.split(' '), index=['from', 'to', 'street_name', 'duration']))
        self.streets_desc['from'] = self.streets_desc['from'].astype(int)
        self.streets_desc['to'] = self.streets_desc['to'].astype(int)
        self.streets_desc['duration'] = self.streets_desc['to'].astype(int)


        self.car_paths_desc =car_paths_desc[0].apply(lambda p:  pd.Series([p.split(' ')[0], p[len(p.split(' ')[0]):].strip()], index = ['number_of_streets','name_of_streets']))
        self.car_paths_desc['number_of_streets'] = self.car_paths_desc['number_of_streets'].astype(int)

        self.G = None

    def init_drected_graph(self) -> nx.DiGraph:
        """
        Initializes a directed graph from the street descriptions.
        """
        # Initialize a directed graph
        G = nx.DiGraph()

        # Add edges from the list of paths
        for i, street in self.streets_desc.iterrows():
            G.add_edge(street['from'], street['to'], name=street['street_name'], weight=street['duration'])

        self.G = G

    def __str__(self) -> str:
        """
        Returns a string representation of the Simulator object.
        """
        return f"Simulation Name: {self.simulation_name}\nDuration: {self.D}\nNumber of Intersections: {self.I}\nNumber of Streets: {self.S}\nNumber of Cars: {self.V}\nBonus Points: {self.F}"

    def __repr__(self) -> str:
        """
        Returns a string representation of the Simulator object.
        """
        return self.__str__()

    def show_subgraph(self, from_: int, to_: int, cutoff: int, show_labels: bool) -> None:
        """
        Shows a subgraph that connects between two nodes with a given cutoff.

        Parameters:
        - from_ (int): The starting node.
        - to_ (int): The target node.
        - cutoff (int): The maximum number of edges to traverse.
        """
        # Find simple paths between 'from_' and 'to_' with the given cutoff
        subset_ = nx.all_simple_paths(self.G, source=from_, target=to_, cutoff=cutoff)
        # Build a subgraph from the simple paths
        G_subset = self.G.subgraph([node for path in list(subset_) for node in path])

        # Plot the subgraph
        plt.figure(figsize=(20, 15))
        pos = nx.spring_layout(G_subset)
        nx.draw(G_subset, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color='gray', width=1, alpha=0.7)
        if show_labels:
            edge_labels = nx.get_edge_attributes(G_subset, 'name')
            nx.draw_networkx_edge_labels(G_subset, pos, edge_labels=edge_labels, font_color='red')

        plt.title(f"Subgraph from Node {from_} to Node {to_} with Cutoff {cutoff}")
        plt.show()





# Load the data
hash_path = 'hashcode.in'
data = pd.read_csv(hash_path, header=None)
D, I, S, V, F =  [int(num) for num in data.loc[0].values[0].split(' ')]
streets_desc = data.loc[1:S]
car_paths_desc = data.loc[S+1:]


simulator1 = Simulator('demo', 10, 5, 20, 100, 50, streets_desc, car_paths_desc)


# Initialize the graph
simulator1.init_drected_graph()

simulator1.show_subgraph(2, 4, 3, True)



# Show all subgraphs that are connected to one edge
# Show all subgraph that are connected to singl junction

# Find the degree (number of connections) of each node.
degrees = dict(simulator1.G.degree())

# Find the shortest path between two nodes.
shortest_path = nx.shortest_path(simulator1.G, source=1, target=4)
print("Shortest path:", shortest_path)

