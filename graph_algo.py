from data import *
import networkx as nx
import shapely
import math

class PathSolver:
    def __init__(self, street, city, state):
        self.lat, self.lon = convert_address_to_latlong(street, city, state)

        self.search_radius = 0.5
    
    def find_nearest_shelter(self):
        self.shelter = get_shelters_data(self.lat, self.lon, self.search_radius).values.tolist()[:3]
        if len(self.shelter) == 0:
            self.search_radius *= 2
            self.find_nearest_shelter()
        sorted(self.shelter, key=lambda s: distance_between_latlong((self.lat, self.lon), (float(s[5]), float(s[4]))))
        return self.shelter
    
    @staticmethod
    def calculate_weight_of_edge(edge):
        try:
            speed = int(int(edge.maxspeed)*1.6)
        except:
            match edge.highway:
                case "motorway":
                    speed = 100
                case "motorway_link":
                    speed = 60
                case "primary":
                    speed = 70
                case "secondary":
                    speed = 50
                case "tertiary":
                    speed = 40
                case "residential":
                    speed = 30
                case _:
                    speed = 50 

        time = (edge.length/1000)/speed
        return time

        
    def build_network(self):
        self.search_radius *= 2
        
        self.nodes = get_points(self.lat, self.lon, self.search_radius)
       
        #building a forward & backward mapping to convert lat&long <=> node index
        self.forward_mapping = {}
        self.backward_mapping = {}
        for node in self.nodes[0].itertuples():
            lat_long = (float(node.y), float(node.x))
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
            
            if (start_node.y, start_node.x) in self.forward_mapping and (end_node.y, end_node.x) in self.forward_mapping:
                edge_weight = PathSolver.calculate_weight_of_edge(edge)
                self.graph.add_edge(self.forward_mapping[(start_node.y, start_node.x)], self.forward_mapping[(end_node.y, end_node.x)], weight=edge_weight)
                if not edge.oneway:
                    self.graph.add_edge(self.forward_mapping[(end_node.y, end_node.x)], self.forward_mapping[(start_node.y,start_node.x)], weight=edge_weight)
    
    def snap(self, point):
        closest = 0
        min_dist = 99999

        for (lat, lon), id in self.forward_mapping.items():
            if id not in self.graph:
                continue
            c_dist = distance_between_latlong((lat, lon), (point[0], point[1]))
            if c_dist < min_dist:
                min_dist = c_dist
                closest = id
        return closest, min_dist

    def solve(self, end):
        a = self.snap((self.lat, self.lon))

        reachable_nodes = nx.node_connected_component(self.graph.to_undirected(),a[0])
        self.graph = self.graph.subgraph(reachable_nodes).copy()
        b = self.snap(end)
        return nx.astar_path(
            self.graph,
            source=a[0],
            target=b[0]
        )

p = PathSolver("949 Avery Street", "South Windsor", "CT")
nearest = p.find_nearest_shelter()
p.build_network()

print([p.backward_mapping[i] for i in p.solve((nearest[0][4], nearest[0][5]))])

#address: 3690 east avenue rochester ny 14618
