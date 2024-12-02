from typing import Annotated

import typer
from rich import print

from src.city_mail.addresses_data_adapter import NominatimAddressesDataAdapter
from src.city_mail.file_path_utils import urlify
from src.city_mail.navigation.graph_path_navigator import GraphPathNavigator
from src.city_mail.osm_streets_graph_adapter import OsmStreetsGraphAdapter
from src.city_mail.path_optimizer_service import PathOptimizerApplication
from src.city_mail.visualization_utils import save_shortest_delivery_path_map


def display_navigation(navigator: GraphPathNavigator, best_nodes: list[int], delivery_nodes: dict[int, str]) -> None:
    for street in navigator.navigate(best_nodes):
        if street.starting_node_id in delivery_nodes.keys():
            print(f":package: [green]Deliver to[/green] [italic]{delivery_nodes[street.starting_node_id]}[/italic]")
        else:
            print(f":right_arrow: Follow {street.name} for {street.length:.0f} meters")

def main(city: str,
         addresses_file_path: Annotated[str, typer.Option(
             help="File containing a list of addresses for the chosen city"
         )] = "addresses_files/varese.txt",
         best_route_folder: Annotated[str, typer.Option(
             help="Folder where save the maps with the optimized street path"
         )] = "shortest_delivery_maps") -> None:

    osm_street_graph = OsmStreetsGraphAdapter(city)
    path_optimizer = PathOptimizerApplication(
        streets_graph_adapter=osm_street_graph,
        address_data_adapter=NominatimAddressesDataAdapter(),
    )

    with open(addresses_file_path) as f:
        addresses = f.read().splitlines()

    print("[green]Calculating the shortest path for the provided deliveries addresses. Could take a while...[/green]")
    best_route, delivery_nodes, starting_node = path_optimizer.calculate_shortest_path(
        addresses
    )

    display_navigation(GraphPathNavigator(osm_street_graph.city_graph), best_route, delivery_nodes)

    save_shortest_delivery_path_map(osm_street_graph.city_graph,
                                    best_route,
                                    starting_node,
                                    delivery_nodes.keys(), f"{best_route_folder}/{urlify(city)}.png")

if __name__ == "__main__":
    typer.run(main)
