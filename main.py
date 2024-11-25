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
    city_name = "Varese, Italy"

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

    ox.plot.plot_graph_route(
        osm_street_graph.city_graph,
        best_route,
        route_color="green",
        route_linewidth=4,
        route_alpha=0.5,
        orig_dest_size=4,
        node_color=[
            "blue" if n == starting_node else "red" if n in delivery_nodes else "white"
            for n in osm_street_graph.city_graph.nodes()
        ],
        node_alpha=[
            1 if n in delivery_nodes else 0.5
            for n in osm_street_graph.city_graph.nodes()
        ],
        node_size=[
            100 if n == starting_node else 50 if n in delivery_nodes else 20
            for n in osm_street_graph.city_graph.nodes()
        ],
    )
