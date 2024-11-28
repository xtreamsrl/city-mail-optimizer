import logging

import networkx as nx

from src.city_mail.addresses_data_adapter import NominatimAddressesDataAdapter
from src.city_mail.osm_streets_graph_adapter import OsmStreetsGraphAdapter
from src.city_mail.path_optimizer_service import PathOptimizerApplication
from src.city_mail.visualization_utils import save_shortest_delivery_path_map

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8.8s] %(message)s",
)

def print_edges_between_nodes(graph: nx.Graph, nodes: list[int], delivery_nodes: dict[int, str]) -> None:
    # TODO: group same street in a single one
    for i in range(len(nodes)-1):
        edge_data = graph.get_edge_data(nodes[i], nodes[i+1])[0]
        if nodes[i] in delivery_nodes.keys():
            print(f"Deliver to {delivery_nodes[nodes[i]]}")
        print(f"Follow {edge_data['name']} for {edge_data['length']:.2f} meters")

if __name__ == "__main__":
    # TODO: add command line parameters
    city_name = "Varese, Varese, Italy"

    osm_street_graph = OsmStreetsGraphAdapter(city_name)
    path_optimizer = PathOptimizerApplication(
        streets_graph_adapter=osm_street_graph,
        address_data_adapter=NominatimAddressesDataAdapter(),
    )

    addresses = [
        "Piazzale Trento, Varese, Italy",
        "Piazza Monte Grappa, Varese, Italy",
        "Via Fratelli de Grandi 5, Varese, Italy",
    ]

    best_route, delivery_nodes, starting_node = path_optimizer.calculate_shortest_path(
        addresses
    )

    print_edges_between_nodes(osm_street_graph.city_graph, best_route, delivery_nodes)

    save_shortest_delivery_path_map(osm_street_graph.city_graph,
                                    best_route,
                                    starting_node,
                                    delivery_nodes.keys(), f"shortest_delivery_maps/{city_name}.png")
