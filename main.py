import logging

import networkx as nx

from src.city_mail.addresses_data_adapter import NominatimAddressesDataAdapter
from src.city_mail.navigation.graph_path_navigator import GraphPathNavigator
from src.city_mail.osm_streets_graph_adapter import OsmStreetsGraphAdapter
from src.city_mail.path_optimizer_service import PathOptimizerApplication
from src.city_mail.visualization_utils import save_shortest_delivery_path_map

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8.8s] %(message)s",
)

def print_edges_between_nodes(navigator: GraphPathNavigator, best_nodes: list[int], delivery_nodes: dict[int, str]) -> None:
    for street in navigator.navigate(best_nodes):

        if street.starting_node_id in delivery_nodes:
            print(f"Deliver to {street.name}")
        print(f"Follow {street.name} for {street.length:.2f} meters")

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

    print_edges_between_nodes(GraphPathNavigator(osm_street_graph.city_graph), best_route, delivery_nodes)

    save_shortest_delivery_path_map(osm_street_graph.city_graph,
                                    best_route,
                                    starting_node,
                                    delivery_nodes.keys(), f"shortest_delivery_maps/{city_name}.png")
