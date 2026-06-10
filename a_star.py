from data import *
import networkx as nx
import shapely

class PathSolver:
    def __init__(self, street, city, state):
        self.lat, self.lon = convert_address_to_latlong(street, city, state)

        self.search_radius = 0.5
    
    def find_nearest_shelter(self):
        self.shelter = get_shelters_data(self.lat, self.lon, self.search_radius).values.tolist()[:3]
        if len(self.shelter) == 0:
            self.search_radius *= 2
            self.find_nearest_shelter(self.search_radius)
        sorted(self.shelter, key=lambda s: distance_between_latlong((self.lat, self.lon), (float(s[4]), float(s[5]))))
        return self.shelter
    def build_network(self):
        self.search_radius = max(self.search_radius, 1)
        self.search_radius *= 2
        
        #building a forward & backward mapping to convert lat&long <=> node index
        self.nodes = get_points(self.lat, self.lon, self.search_radius)
        
        self.forward_mapping = {}
        self.backward_mapping = {}
        for node in self.nodes[0].itertuples():
            lat_long = (float(node.x), float(node.y))
            if lat_long in self.forward_mapping.keys():
                continue
            c_index = len(self.forward_mapping)
            self.forward_mapping[lat_long] = c_index
            self.backward_mapping[c_index] = lat_long
        
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(len(self.forward_mapping)))
        
        #now, we use the mappings to easily build edges in our graph
        for edge in self.nodes[1].itertuples():
            if edge.reversed:
                start_node = shapely.get_point(edge.geometry, -1)
                end_node = shapely.get_point(edge.geometry, 0)
            else:
                start_node = shapely.get_point(edge.geometry, 0)
                end_node = shapely.get_point(edge.geometry, -1)
            
            if start_node in self.forward_mapping and end_node in self.forward_mapping:
                self.graph.add_edge(self.forward_mapping(start_node), self.forward_mapping(end_node))
                if not edge.oneway:
                    self.graph.add(self.forward_mapping(end_node), self.forward_mapping(start_node))
    def solve(self, end):
        return nx.astar_path(
            self.graph,
            source=(round(self.lat, 4),round(self.lon,4)),
            target=(round(end[4],4), round(end[5],4))
        )


p = PathSolver("360 East Ave", "Rochester", "NY")
nearest = p.find_nearest_shelter()
p.build_network()
print(p.solve(nearest[0]))

#address: 3690 east avenue rochester ny 14618
