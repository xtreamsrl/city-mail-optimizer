import networkx
import osmnx as ox


class StreetsGraphPort:
    def get_city_graph(self, city_name: str) -> dict:
        pass

    def address_to_node_id(self, address: str) -> int:
        pass

    def node_id_to_address(self, node_id: int) -> str:
        pass


class OsmStreetsGraphAdapter:
    def download_city_graph(self, city_name: str) -> networkx.MultiDiGraph:
        G = ox.graph_from_place(city_name)
        return G


    def address_to_node_id(self, address: str) -> int:
        id = ox.geocode_to_gdf(address)
        return id['osmid'].values[0]

    def node_id_to_address(self, node_id: int) -> str:
        return ox.geocode_to_gdf(node_id, by_osmid=True)['name']

