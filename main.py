import logging

import osmnx as ox
from src.city_mail.addresses_data_adapter import NominatimAddressesDataAdapter
from src.city_mail.osm_streets_graph_adapter import OsmStreetsGraphAdapter
from src.city_mail.path_optimizer_service import PathOptimizerApplication

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8.8s] %(message)s",
)

if __name__ == "__main__":
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
